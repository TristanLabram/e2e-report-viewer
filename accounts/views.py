from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import is_valid_path
from .forms import ProfileForm

# View and edit user profile information, requires logon ([Authorize] in C#)
@login_required
def profile_view(request):
    #Post request for form submission
    if request.method == 'POST':
        #Binds the form to the data in the request and the sending user
        form = ProfileForm(request.POST, instance=request.user)

        #Validates, saves and redirects the user to the view form
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('profile')
    
    # Get request - show the form with pre-populated values
    else: 
        #Attach current user model to form
        form = ProfileForm(instance=request.user)
    
    # Render the profile template, passing in the form object as 'View/FormModel'
    return render(request, 'accounts/profile.html', {'form': form})
