from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages

# Admin accessor, allows '@admin_required' tag to be added to admin only pages
# Think Blazor: [Authorize(Roles = "Admin")], these work as wrappers to any
# associated functions to provide the authentication
def admin_required(view_func):
    #Use functools @wraps to preserve the wrapped functions name and docstring
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        # Args captures postional args as a tuple
        #kwargs is a dict of keyword args
        if not request.user.is_authenticated:
            return redirect('login')
        if not request.user.is_admin:
            messages.error(request, 'You do not have the required permissions to access this page.')
            return redirect('report_list')
        return view_func(request, *args, **kwargs)
    return wrapper