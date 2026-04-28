# Secure Authentication System 

## Project Structure

```
secure-auth/
│
├── app/
│   ├── models/
│   │   └── user_model.py
│   │
│   ├── routes/
│   │   ├── auth_routes.py
│   │   └── user_routes.py
│   │
│   ├── services/
│   │   ├── auth_service.py
│   │   └── twofa_service.py
│   │
│   ├── utils/
│   │   ├── hash_utils.py
│   │   └── token_utils.py
│   │
│   ├── templates/
│   │   ├── base.html
│   │   ├── register.html
│   │   ├── login.html
│   │   ├── qr.html
│   │   ├── verify_2fa.html
│   │   └── dashboard.html
│   │
│   ├── static/
│   │   └── css/
│   │       ├── base.css
│   │       ├── register.css
│   │       ├── login.css
│   │       ├── qr.css
│   │       ├── verify.css
│   │       └── dashboard.css
│
├── config.py
├── run.py
├── requirements.txt
```

---

## Implemented Features

### 1. User Registration

* Users can create an account using:

  * Name
  * Email
  * Password
  * Role
* User data is stored in the database
* A unique 2FA secret is generated for each user

---

### 2. Password Hashing

* Passwords are not stored as plain text
* Hashing is implemented using:

  * `generate_password_hash`
* Verification is done using:

  * `check_password_hash`

---

### 3. Login System

* Users log in using:

  * Email
  * Password
* Credentials are validated
* If correct, the system proceeds to 2FA verification

---

### 4. Two-Factor Authentication (2FA)

* A secret key is generated for each user
* A QR code is created and displayed
* The user scans it using an authenticator app
* The user enters a 6-digit code
* The code is verified using `pyotp`

---

## Application Flow

1. User registers a new account
2. Password is hashed and stored
3. 2FA secret is generated
4. QR code is displayed
5. User logs in
6. Password is verified
7. User enters 2FA code
8. Code is verified
9. Login is successful
10. Dashboard is displayed

---

## Notes

* The project is modular and organized into:

  * models
  * routes
  * services
  * utils
* No code duplication
* Clear separation of concerns
* Templates and static files are used to separate frontend and backend logic
