from django import forms
from .models import CustomUser

# User profile form functions for validating user data
class ProfileForm(forms.ModelForm):
    # Meta data to attach the right model to the forms
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email']
    
    # Function to clean and validate the user email input
    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Check the email is unique to the current user
        if (
            CustomUser.objects.filter(email=email)
                .exclude(pk=self.instance.pk)
                .exists()
        ):
            raise forms.ValidationError("A user with this email already exists.")
        return email