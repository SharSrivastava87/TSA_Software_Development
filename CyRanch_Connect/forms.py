from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class CreateStudentForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password1"].widget.attrs['class'] = "form-control rounded-0 shadow-none"
        self.fields["password2"].widget.attrs['class'] = "form-control rounded-0 shadow-none"
        self.fields["password1"].widget.attrs['name'] = "password"
        self.fields["password2"].widget.attrs['name'] = "password-confirm"
        self.fields["password1"].widget.attrs['id'] = "password"
        self.fields["password2"].widget.attrs['id'] = "password-confirm"

        self.fields['username'].label = 'Community ID'
        self.fields['username'].help_text = 'Required. 6 digits only.'

    def clean_username(self):
        username = self.cleaned_data.get('username')

        if not username.isdigit() or len(username) != 6:
            raise ValidationError("Please enter your 6 digit community code only.")

        return username

    def clean_grade_number(self):
        grade_number = self.cleaned_data.get('grade_number')

        if grade_number and (grade_number < 1 or grade_number > 12):
            raise forms.ValidationError("Grade number must be between 1 and 12.")

        return grade_number

    grade_number = forms.IntegerField(required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2', 'grade_number']
        widgets = {
            'username': forms.TextInput(attrs={'name': "username", 'id': "username", 'class': "form-control rounded-0 shadow-none", 'type': "text"}),
            'first_name': forms.TextInput(attrs={'name': "firstName", 'id': "firstName", 'class': "form-control rounded-0 shadow-none", 'type': "text"}),
            'last_name': forms.TextInput(attrs={'name': "lastname", 'id': "lastname", 'class': "form-control rounded-0 shadow-none", 'type': "text"}),
            'email': forms.EmailInput(attrs={'name': "email", 'id': "email", 'class': "form-control rounded-0 shadow-none ", 'type': "email"}),
            'grade_number': forms.TextInput(attrs={'name': "grade_number", 'id': "grade_number", 'class': "form-control rounded-0 shadow-none", 'type': "text"}),
        }


# A modified version of the default Django PasswordChangeForm
class ChangePasswordForm(PasswordChangeForm):
    # Adding custom styling to the default form elements created by Django
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["old_password"].widget.attrs['class'] = "form-control rounded-0 shadow-none"
        self.fields["new_password1"].widget.attrs['class'] = "form-control rounded-0 shadow-none"
        self.fields["new_password2"].widget.attrs['class'] = "form-control rounded-0 shadow-none"
        self.fields["old_password"].widget.attrs['name'] = "old-password"
        self.fields["new_password1"].widget.attrs['name'] = "new-password"
        self.fields["new_password2"].widget.attrs['name'] = "new-password-confirm"
        self.fields["old_password"].widget.attrs['id'] = "old-password"
        self.fields["new_password1"].widget.attrs['id'] = "new-password"
        self.fields["new_password2"].widget.attrs['id'] = "new-password-confirm"
