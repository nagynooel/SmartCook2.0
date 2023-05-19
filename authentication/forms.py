"""
    Form classes for authentication and profile related pages
    @package smartcook
    @author Noel Nagy
    @website: https://github.com/nagynooel
    ©2023 Noel Nagy - All rights reserved.
"""

from django.urls import reverse
from django import forms
from django.forms import ModelForm, ImageField, FileInput, HiddenInput
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset, Field, Div, Hidden, HTML
from crispy_bootstrap5.bootstrap5 import FloatingField

from django.contrib.auth.models import User
from .models import Profile, PasswordResetToken

from django.template.loader import render_to_string
import re
from . import utils

global_password_regex = "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[   ?!@$%^&*-]).{8,}$"

# Form for registering a new user
class RegistrationForm(UserCreationForm):

    # Regex to use on front- and backend
    username_regex = "[a-z,A-Z,0-9]{6,150}"
    password_regex = global_password_regex


    class Meta(UserCreationForm.Meta):
        model = User
        fields = ["first_name", "last_name","username", "email", "password1", "password2"]


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Initialize crispy forms form helper and set basic styling
        self.helper = FormHelper()
        self.helper.form_id = "registration-form"
        self.helper.form_class = "full_page_form container needs-validation shadow-lg"
        self.helper.form_method = "POST"
        self.helper.form_action = reverse("register")
        self.helper.attrs = {"novalidate":""}
        self.helper.label_class = "form-label"

        # Remove default helper texts
        self.fields["username"].help_text = ""
        self.fields["password1"].help_text = ""
        self.fields["password2"].help_text = ""

        # Make all fields required
        self.fields["first_name"].required = True
        self.fields["last_name"].required = True
        self.fields["email"].required = True

        # Make first name field focused instead of username
        self.fields["username"].widget.attrs.update(autofocus = "False")
        self.fields["first_name"].widget.attrs.update(autofocus = "True")

        # Create form layout and styling
        self.helper.layout = Layout(
            Hidden("next", "{{ next }}"),
            Fieldset(
                "Register",
                Div(
                    FloatingField("first_name", wrapper_class="col-6 col-sm-6"),
                    FloatingField("last_name", wrapper_class="col-6 col-sm-6"),
                    css_class="row",
                ),
                Div(
                    FloatingField("username", css_class="text-nowrap",pattern=self.username_regex,
                        data_bs_toggle="tooltip", data_bs_placement="bottom",
                        data_bs_title="Username can only contain letters and digits and must be at least 6 characters long."),
                    css_class="input-group"
                ),
                FloatingField("email"),
                FloatingField("password1", css_class="text-nowrap", pattern=self.password_regex,
                data_bs_toggle="tooltip", data_bs_placement="bottom", data_bs_html="true",
                data_bs_title="""
                    Your password must be at least 8 characters long.<br>
                    Must contain at least 1 lower and 1 uppercase letter.<br>
                    Must contain at least 1 digit.<br>
                    Must contain at least 1 special character.
                    """),
                FloatingField("password2", css_class="text-nowrap", pattern=self.password_regex,
                data_bs_toggle="tooltip", data_bs_placement="bottom",
                data_bs_title="Enter the same password as before, for verification."),
                Submit("submit", "Register")
            )
        )


    # Validate username
    def clean_username(self):
        username = self.cleaned_data["username"].lower()

        # Username matches regex
        if not re.match(self.username_regex, username):
            raise ValidationError("Username does not match the requirements!")

        # Username not already registered
        new = User.objects.filter(username=username)

        if new.count():
            raise ValidationError("User already exists!")

        return username


    # Validate email
    def clean_email(self):
        email = self.cleaned_data["email"].lower()

        # Email not already registered
        new = User.objects.filter(email=email)

        if new.count():
            raise ValidationError("Email already exists!")

        return email


    # Validate password and confirm password
    def clean_password2(self):
        password1 = self.cleaned_data["password1"]
        password2 = self.cleaned_data["password2"]

        # Password matches regex
        if not re.match(self.password_regex, password1):
            raise ValidationError("Password does not match the requirements!")

        # Password and confirm password matches
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords do not match!")

        return password2


    # Create the user with the validated information
    def save(self):
        user = User.objects.create_user(
            self.cleaned_data["username"],
            self.cleaned_data["email"],
            self.cleaned_data["password1"]
        )

        user.first_name = self.cleaned_data["first_name"].capitalize()
        user.last_name = self.cleaned_data["last_name"].capitalize()

        user.save()

        return user


# Form for authenticating user
class LoginForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Initialize crispy forms form helper and set basic styling
        self.helper = FormHelper()
        self.helper.form_id = "login-form"
        self.helper.form_class = "full_page_form container shadow-lg"
        self.helper.form_method = "POST"
        self.helper.form_action = reverse("login")
        self.helper.label_class = "form-label"

        self.helper.layout = Layout(
            Hidden("next", "{{ next }}"),
            Fieldset(
                "Login",
                FloatingField("username"),
                FloatingField("password"),
                Div(
                    HTML("<a href='{% url 'forgotten_password' %}'>Forgot password?</a>"),
                    css_class="mb-3"
                ),
                Submit("submit", "Login")
            )
        )


# Form for updating account information
class UpdateProfileForm(forms.ModelForm):
    
    picture = forms.ImageField(widget=FileInput)
    reset_pfp = forms.CharField(widget=HiddenInput, required=False)
    
    class Meta:
        model = Profile
        fields = ["picture"]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Initialize crispy forms form helper and set basic styling
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_show_labels = False
        self.helper.disable_csrf = True
        
        self.helper.layout = Layout(
            Field("reset_pfp", css_class="reset-field"),
            HTML("""
                <label for="profile-picture">
                    <img class="image-preview" src="{{ request.user.profile.picture.url }}" alt="{{ user.get_username }}'s profile picture">
                </label>
            """),
            Field("picture", css_class="image-input", id="profile-picture"),
            HTML("""<a class="btn btn-danger remove-image-file-btn" id="remove-profile-picture-btn">Remove Picture</a>""")
        )


# Form for changing account information
class UpdateAccountForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email"]
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(UpdateAccountForm, self).__init__(*args, **kwargs)

        # Initialize crispy forms form helper and set basic styling
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.label_class = "form-label"
        self.helper.disable_csrf = True
        
        # Make all fields required
        self.fields["first_name"].required = True
        self.fields["last_name"].required = True
        self.fields["username"].required = True
        self.fields["email"].required = True
        
        # Remove default helper text
        self.fields["username"].help_text = ""
        
        # Disable username field
        self.fields["username"].disabled = True

        self.helper.layout = Layout(
            Fieldset(
                "General information",
                Div(
                    Div(
                        FloatingField("first_name"),
                        css_class="col-md-6"
                    ),
                    Div(
                        FloatingField("last_name"),
                        css_class="col-md-6"
                    ),
                    css_class="row"
                ),
                Div(
                    Div(
                        FloatingField("username", template="crispy_forms/no_margin_floating_input.html"),
                        data_bs_toggle="tooltip", data_bs_placement="bottom", data_bs_title="Username can not be changed.",
                        css_class="col-md-6 mb-3"
                    ),
                    Div(
                        FloatingField("email"),
                        css_class="col-md-6"
                    ),
                    css_class="row"
                ),
            )
        )
    
    # Validate email
    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        
        # Return email if it stays the same
        if email == self.request.user.email:
            return email

        # Email not already registered
        new = User.objects.filter(email=email)

        if new.count():
            raise ValidationError("Email address is already in database!")

        return email


class ResetPasswordForm(forms.Form):
    
    password_regex = global_password_regex

    password1 = forms.CharField(widget=forms.PasswordInput, label="New Password")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm New Password")

    def __init__(self, *args, **kwargs):
        self.token = kwargs.pop('token')
        super().__init__(*args, **kwargs)

        # Initialize crispy forms form helper and set basic styling
        self.helper = FormHelper()
        self.helper.form_id = "reset-password-form"
        self.helper.form_class = "full_page_form container shadow-lg"
        self.helper.form_method = "POST"
        self.helper.form_action = reverse("reset_password", kwargs={"token":self.token})
        self.helper.label_class = "form-label"

        self.fields["password1"].required = True
        self.fields["password2"].required = True

        self.helper.layout = Layout(
            Fieldset(
                "Change Password",
                FloatingField("password1", pattern=self.password_regex),
                FloatingField("password2", pattern=self.password_regex),
                Submit("submit", "Save password")
            )
        )
    
    def clean_password2(self):
        # Get user input
        password1 = self.cleaned_data["password1"]
        password2 = self.cleaned_data["password2"]
        
        # Validate password matches requirements
        if not re.match(self.password_regex, password1):
            raise ValidationError("Password does not match the requirements!")

        # Validate passwords match
        if password1 != password2:
            raise ValidationError("Passwords do not match")
    
    def save(self):
        self.clean()
        token_obj = PasswordResetToken.objects.filter(token=self.token)
        user = token_obj.first().user

        # Set user password
        user.set_password(self.cleaned_data["password1"])
        user.save()

        # Set token to used
        token_obj.update(used=True)

        context = {
            "first_name": user.first_name
        }

        # Send an email to notify the user of a password change
        utils.send_smtp_email(user.email, "Account password changed", render_to_string("authentication/email/password_changed.html",context), render_to_string("authentication/email/password_changed.txt",context))


class ForgottenPasswordForm(forms.Form):
    
    email = forms.EmailField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Initialize crispy forms form helper and set basic styling
        self.helper = FormHelper()
        self.helper.form_id = "forgotten-password-form"
        self.helper.form_class = "full_page_form container shadow-lg"
        self.helper.form_method = "POST"
        self.helper.form_action = reverse("forgotten_password")
        self.helper.label_class = "form-label"

        self.helper.layout = Layout(
            Fieldset(
                "Forgotten Password",
                FloatingField("email"),
                Div(
                    HTML("<a href='{% url 'login' %}'>Login</a>"),
                    css_class="mb-3"
                ),
                Submit("submit", "Send Password Reset")
            )
        )
    
    def clean_email(self):
        # Validate user exist
        self.clean()

        email = self.cleaned_data["email"].lower()

        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            raise ValidationError("User does not exist")

        return email