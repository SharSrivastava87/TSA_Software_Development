import datetime
import random

from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone
from django.db.models import Avg
from django.db.models.aggregates import StdDev
from django.contrib.auth.decorators import user_passes_test
from django.utils.http import urlencode

from .forms import CreateStudentForm, ChangePasswordForm
from .models import Student, Event, Prize


# Homepage
def index(request):
    return render(request, 'CyRanch_Connect/index.html')


# Events page, only displays events that have not happened yet and events are ordered by date
def events(request):
    events = Event.objects.all().filter(date__gte=timezone.now()).order_by('date')
    return render(request, 'CyRanch_Connect/events.html', {'events': events})


# Shows the prizes that are available each quarter (sorted by number of points needed), prizes can be added through the admin panel
def prizes(request):
    prizes = Prize.objects.all().order_by('price')
    return render(request, 'CyRanch_Connect/prizes.html', {'prizes': prizes})


# A login page, that authenticates a user that is related to a student object in the database.
def login(request):
    if request.method == "POST":
        student_id = request.POST.get('student_id')
        password = request.POST.get('password')

        user = authenticate(request, username=student_id, password=password)

        # Check if a user with provided credentials exists and authenticate them if so
        if user:
            auth_login(request, user)
            messages.success(request, 'Logged in successfully!')
            if request.GET.get('next'):
                return HttpResponseRedirect(request.get('next'))
            else:
                return HttpResponseRedirect(reverse('CyRanch_Connect:index'))
        else:
            messages.error(request, 'Invalid student ID or password')
            return render(request, 'CyRanch_Connect/login.html', {'error': 'Invalid login'})
    else:
        return render(request, 'CyRanch_Connect/login.html')


# An endpoint to log users out
def logout(request):
    auth_logout(request)
    messages.success(request, 'Logged out successfully!')
    return HttpResponseRedirect(reverse('CyRanch_Connect:login'))


# A leaderboard for each grade sorted by the number of points each student has accumulated
def leaderboard(request):
    grade_nine = Student.objects.all().filter(grade=9).order_by('-points')
    grade_ten = Student.objects.all().filter(grade=10).order_by('-points')
    grade_eleven = Student.objects.all().filter(grade=11).order_by('-points')
    grade_twelve = Student.objects.all().filter(grade=12).order_by('-points')

    return render(request, 'CyRanch_Connect/leaderboard.html',
                  {'grade_nine': grade_nine, 'grade_ten': grade_ten, 'grade_eleven': grade_eleven,
                   'grade_twelve': grade_twelve})


# Only for staff members, shows all data and provides useful statistics
def generate_report(request):
    if request.user.is_staff:
        # Data customization for the report
        orderby = request.GET.get('orderby', '-points')
        if orderby not in ['points', '-points', 'first_name', '-first_name', 'last_name', '-last_name']:
            return HttpResponse(status=404)

        # Get all students
        grade_nine = Student.objects.all().filter(grade=9).order_by(orderby)
        grade_ten = Student.objects.all().filter(grade=10).order_by(orderby)
        grade_eleven = Student.objects.all().filter(grade=11).order_by(orderby)
        grade_twelve = Student.objects.all().filter(grade=12).order_by(orderby)

        # Select winners for each grade
        random_winner_nine = random.choice(grade_nine) if grade_nine else "None"
        random_winner_ten = random.choice(grade_ten) if grade_ten else "None"
        random_winner_eleven = random.choice(grade_eleven) if grade_eleven else "None"
        random_winner_twelve = random.choice(grade_twelve) if grade_twelve else "None"

        # Since the latest is set to the points field, calling latest will return the student with the most points
        most_points = Student.objects.latest()

        # Get and format the date
        date = str(datetime.date.today())

        # Generate Statistics
        average = Student.objects.all().aggregate(Avg('points'))['points__avg']
        stddev = Student.objects.all().aggregate(StdDev('points'))['points__stddev']

        return render(request, 'CyRanch_Connect/report.html',
                      {'grade_nine': grade_nine, 'grade_ten': grade_ten, 'grade_eleven': grade_eleven,
                       'grade_twelve': grade_twelve, 'random_winner_nine': random_winner_nine,
                       'random_winner_ten': random_winner_ten, 'random_winner_eleven': random_winner_eleven,
                       'random_winner_twelve': random_winner_twelve, 'most_points': most_points, 'date': date,
                       'average': average, 'stddev': stddev})
    else:
        # Handle a non-staff user attempting to access this page
        messages.error(request, 'You do not have permission to view this page')
        return HttpResponseRedirect(reverse('CyRanch_Connect:index'))


# Interactive help page
def help(request):
    return render(request, 'CyRanch_Connect/help.html')


# Generate QR codes for events, this page may only be accessed by staff members
@user_passes_test(lambda u: u.is_superuser)
def event_qr(request, event_id):
    event = get_object_or_404(Event, event_id=event_id)
    # Creating a random token for the event so that the URL cannot be shared
    event.token = random.randint(100000, 999999)
    event.save()
    qr_url = request.build_absolute_uri(
        f"{reverse('CyRanch_Connect:event_checkin', args={event_id})}?{urlencode({'token': event.token})}")
    return render(request, 'CyRanch_Connect/event_qr.html', {'qr_url': qr_url})


# The page the QR code links to allowing users to claim their points
def event_checkin(request, event_id):
    event = get_object_or_404(Event, event_id=event_id)
    # Ensure the user is logged in, the token is valid, and the user has not already claimed points for this event
    if request.user.is_authenticated:
        if event.token == int(request.GET.get('token')):
            if request.user.student not in event.attendees.all():
                event.attendees.add(request.user.student)
                request.user.student.points += event.points
                request.user.student.save()
                messages.success(request,
                                 f'You have checked in for {event.name} and have earned {event.points} point{"s" if event.points > 1 else ""}!')
                return HttpResponseRedirect(reverse('CyRanch_Connect:index'))
            else:
                messages.error(request, 'You have already checked in to this event')
                return HttpResponseRedirect(reverse('CyRanch_Connect:index'))
        else:
            messages.error(request, 'This QR code has expired, please try again')
            return HttpResponseRedirect(reverse('CyRanch_Connect:index'))
    else:
        messages.error(request, 'You must be logged in to check in to an event')
        return HttpResponseRedirect(reverse('CyRanch_Connect:login'))


from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateStudentForm

from .models import Student

def register(request):
    if request.method == 'POST':
        form = CreateStudentForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the User instance and get the saved object
            # Create a new Student instance and associate it with the User instance

            student = Student.objects.create(
                user=user,
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                email=form.cleaned_data['email'],
                student_id=int(user.username),
                points=0,
                grade=form.cleaned_data['grade_number']

            )
            return redirect('/login')
    else:
        form = CreateStudentForm()

    return render(request, 'CyRanch_Connect/register.html', {'form': form})



def terms(request):
    return render(request, 'CyRanch_Connect/Terms&Conditions.html')

def donate(request):
    return render(request, 'CyRanch_Connect/donate.html')