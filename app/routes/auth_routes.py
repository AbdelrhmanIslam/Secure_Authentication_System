# from flask import Blueprint, request, jsonify
# from app.services.auth_service import register_user, login_user
# from app.services.twofa_service import generate_qr_code, verify_2fa

# auth_bp = Blueprint('auth', __name__)

# # Register
# @auth_bp.route('/register', methods=['POST'])
# def register():
#     data = request.json

#     user = register_user(
#         data['name'],
#         data['email'],
#         data['password'],
#         data['role']
#     )

#     qr = generate_qr_code(user.email, user.twofa_secret)

#     return jsonify({
#         "message": "User registered",
#         "qr_code": qr
#     })


# # Login Step 1 (Password)
# @auth_bp.route('/login', methods=['POST'])
# def login():
#     data = request.json

#     user = login_user(data['email'], data['password'])

#     if not user:
#         return jsonify({"error": "Invalid credentials"}), 401

#     return jsonify({
#         "message": "Enter 2FA code",
#         "user_id": user.id
#     })


# # Login Step 2 (2FA)
# @auth_bp.route('/verify-2fa', methods=['POST'])
# def verify_2fa_route():
#     data = request.json

#     from app.models.user_model import User
#     user = User.query.get(data['user_id'])

#     if not verify_2fa(user.twofa_secret, data['code']):
#         return jsonify({"error": "Invalid 2FA"}), 401

#     return jsonify({
#         "message": "Login successful"
#     })




from flask import Blueprint, render_template, request, redirect, url_for
from app.services.auth_service import register_user, login_user
from app.services.twofa_service import generate_qr_code, verify_2fa
from app.models.user_model import User

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

    return render_template('dashboard.html', user=user)