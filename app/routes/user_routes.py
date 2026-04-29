from flask import Blueprint, render_template, g, jsonify
from functools import wraps
from app.utils.token_utils import token_required

user_bp = Blueprint('user', __name__)

def role_required(*allowed_roles):
    # purpose: a decorator factory — takes one or more role names and returns
    # a decorator that blocks the route if the logged-in user's role
    # isn't in the allowed list
    
    def decorator(route_function):
        @wraps(route_function)
        def wrapper(*args, **kwargs):
            # grab the currently authenticated user's role from the flask global object
            user_role = g.current_user.get('role')
            
            # check if their role exists within the permitted list for this route
            if user_role not in allowed_roles:
                # if not, return a 403 Forbidden JSON response
                return jsonify({'error': 'Access denied — your role does not have permission for this page'}), 403
                
            # if they are allowed, continue executing the protected route
            return route_function(*args, **kwargs)
        return wrapper
    return decorator


@user_bp.route('/dashboard')
@token_required
def show_dashboard():
    """Renders the main dashboard for any authenticated user."""
    # render the dashboard html page and pass the user details into the template
    return render_template('dashboard.html', user=g.current_user)


@user_bp.route('/profile')
@token_required
def show_profile():
    """Renders the user profile page for any authenticated user."""
    # render the profile html page and pass the user details into the template
    return render_template('profile.html', user=g.current_user)


@user_bp.route('/manager')
@token_required
@role_required('Manager', 'Admin')
def show_manager_panel():
    """Renders the manager panel, accessible only to Managers and Admins."""
    # render the manager html page and pass the user details into the template
    return render_template('manager.html', user=g.current_user)


@user_bp.route('/admin')
@token_required
@role_required('Admin')
def show_admin_panel():
    """Renders the admin panel, accessible only to Admins."""
    # render the admin html page and pass the user details into the template
    return render_template('admin.html', user=g.current_user)
