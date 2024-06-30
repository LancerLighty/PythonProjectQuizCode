from functools import wraps
from flask import abort, redirect, url_for
from flask_login import current_user

def role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated or current_user.role != role:
                abort(403)  # Forbidden
            return f(*args, **kwargs)
        return decorated_function
    return decorator
def logout_required(redirect_to='index'):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if current_user.is_authenticated:
                return redirect(url_for(redirect_to))
            return f(*args, **kwargs)
        return decorated_function
    return decorator