from flask import Blueprint, render_template, request, redirect, url_for
from app.services.auth_service import register_user, login_user
from app.services.twofa_service import generate_qr_code, verify_2fa
from app.models.user_model import User
from app.utils.token_utils import generate_token

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
def home():
    from flask import render_template_string
    return render_template_string("""
    {% extends 'base.html' %}
    {% block content %}
    <h2>Welcome</h2>
    <p style='margin-bottom:20px'>Please login or register to continue.</p>
    <a href='/login' class='btn' style='margin-bottom:10px'>Login</a>
    <a href='/register' class='btn btn-secondary'>Register</a>
    {% endblock %}
    """)

# ---------------- REGISTER ----------------
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user = register_user(
            request.form['name'],
            request.form['email'],
            request.form['password'],
            request.form['role']
        )

        qr = generate_qr_code(user.email, user.twofa_secret)

        return render_template('qr.html', qr=qr)

    return render_template('register.html')


# ---------------- LOGIN ----------------
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = login_user(
            request.form['email'],
            request.form['password']
        )

        if not user:
            return "Invalid credentials"

        return render_template('verify_2fa.html', user_id=user.id)

    return render_template('login.html')


# ---------------- VERIFY 2FA ----------------
@auth_bp.route('/verify-2fa', methods=['POST'])
def verify_2fa_route():
    user = User.query.get(request.form['user_id'])

    if not verify_2fa(user.twofa_secret, request.form['code']):
        return "Invalid 2FA Code"

    # generate a new JWT containing the user's ID and role
    token = generate_token(user.id, user.role, user.name, user.email)
    
    # create a redirect response pointing to the user dashboard
    response = redirect(url_for('user.show_dashboard'))
    
    # attach the token as a secure, HTTP-only cookie to the response
    response.set_cookie(
        'auth_token',        # cookie name — must match what token_required reads
        token,               # the JWT string from generate_token()
        httponly=True,       # prevents JavaScript from reading the cookie (XSS protection)
        samesite='Lax',      # prevents the cookie from being sent on cross-site requests
        max_age=3600         # cookie lives for 1 hour — matches the token expiry
    )
    
    # return the redirect response so the browser navigates to the dashboard
    return response

# ---------------- LOGOUT ----------------
@auth_bp.route('/logout')
def logout():
    # redirect to the home page
    response = redirect(url_for('auth.home'))
    
    # clear the auth cookie to end the session
    response.delete_cookie('auth_token')
    
    return response