from django import forms
from .models import CustomUser

def clean_email_helper(email, pk):
    if (
        CustomUser.objects.filter(email=email)
            .exclude(pk=pk)
            .exists()
    ):
        raise forms.ValidationError("A user with this email already exists.")
    return email

def clean_password2_helper(p1, p2):
    if p1 and p2 and p1 != p2:
        raise forms.ValidationError('Passwords do not match.')
    return p2

# User profile form for editing own user profile
class ProfileForm(forms.ModelForm):
    # Meta data to attach the right model to the forms
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email']
    
    # Function to clean and validate the user email input
    def clean_email(self):
        return clean_email_helper(self.cleaned_data.get('email'), self.instance.pk)
    
#Form for admins to create new users
class UserCreateForm(forms.ModelForm):
    #Define custom password fields to avoid django's built in UserCreationForm which requires a username
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput,
        help_text="Must be at least 8 characters",
    )
    password2 = forms.CharField(
        label="Confirm password",
        widget=forms.PasswordInput,
    )

    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'role']

    def clean_email(self):
        return clean_email_helper(self.cleaned_data.get('email'), self.instance.pk)
    
    def clean_password2(self):
        return clean_password2_helper(self.cleaned_data.get('password1'), self.cleaned_data.get('password2'))
    
    #Override the inherited Django save method to force password hashing
    def save(self, commit=True):
        #Create the new user without saving
        user = super().save(commit=False)

        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user
    
# Form to edit existing users
class UserEditForm(forms.ModelForm):
    password1 = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput,
        required=False,
        help_text="Leave blank to keep the current password.",
    )
    password2 = forms.CharField(
        label="Confirm new password",
        widget=forms.PasswordInput,
        required=False,
    )

    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'role']

    def clean_email(self):
        return clean_email_helper(self.cleaned_data.get('email'), self.instance.pk)
    
    def clean_password2(self):
        return clean_password2_helper(self.cleaned_data.get('password1'), self.cleaned_data.get('password2'))
    
    #Override the inherited Django save method to force password hashing
    def save(self, commit=True):
        user = super().save(commit=False)
        #Only update password if a new one was entered
        p1 = self.cleaned_data.get('password1')
        if p1:
            user.set_password(p1)
        if commit:
            user.save()
        return user
    
# Public registration form
class RegistrationForm(forms.ModelForm):
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput,
        help_text='Must be at least 8 characters.',
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput,
    )
    is_admin = forms.BooleanField(
        label='Admin account',
        required=False,
        help_text='Check this to create an admin account.',
    )

    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name']

    def clean_email(self):
        return clean_email_helper(self.cleaned_data.get('email'), self.instance.pk)
    
    def clean_password2(self):
        return clean_password2_helper(
            self.cleaned_data.get('password1'),
            self.cleaned_data.get('password2'),
        )
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.role = 'admin' if self.cleaned_data.get('is_admin') else 'viewer'
        if commit:
            user.save()
        return user