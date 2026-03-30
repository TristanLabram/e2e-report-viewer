from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ProfileForm, UserCreateForm, UserEditForm
from .models import CustomUser
from .decorators import admin_required

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

#Admin only, display all users
@admin_required
def user_list(request):
    users = CustomUser.objects.all().order_by('last_name', 'first_name')
    return render(request, 'accounts/user_list.html', {'users': users})

#Admin only, add new user
@admin_required
def user_create(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'User created successfully')
            return redirect('user_list')
    else:
        form = UserCreateForm()

    return render(request, 'accounts/user_form.html', {
        'form': form,
        'form_title': 'Create User',
    })

#Admin only, user edit
@admin_required
def user_edit(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)

    # Detect self editing to prevent admins from changing their own role
    # Otherwise you could get to no admins and be unable to change anything
    editing_self = request.user.pk == user.pk

    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            if editing_self and form.cleaned_data['role'] != 'admin':
                messages.error(request, 'You cannot change your own role.')
                return redirect('user_edit', pk=pk)
            form.save()
            messages.success(request, f'User "{user}" updated successfully.')
            return redirect('user_list')
    else:
        form = UserEditForm(instance=user)

    return render(request, 'accounts/user_form.html', {
        'form': form,
        'form_title': f'Edit User - {user.first_name} {user.last_name}',
        'editing_self': editing_self,
    })

#Admin only, delete user
@admin_required
def user_delete(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)

    #Prevent self deletion
    if request.user.pk == user.pk:
        messages.error(request, 'You cannot delete your own account.')
        return redirect('user_list')
    
    if request.method == 'POST':
        user_name = str(user)
        user.delete()
        messages.success(request, f'User "{user_name}" has been deleted.')
        return redirect('user_list')
    
    return render (request, 'accounts/user_confirm_delete.html', {'user': user})