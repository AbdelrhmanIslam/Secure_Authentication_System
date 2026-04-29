# Secure Authentication System

A comprehensive, modular Flask-based secure authentication system. It demonstrates best practices for user authentication, password security, session management using JSON Web Tokens (JWT), two-factor authentication (2FA), and Role-Based Access Control (RBAC).

---

## Features

### 1. User Registration & Login
*   Users can register with Name, Email, Password, and Role (`User`, `Manager`, `Admin`).
*   Secure validation of credentials during the login process.
*   Data is stored securely in an SQLite database using `Flask-SQLAlchemy`.

### 2. Robust Password Security
*   Passwords are never stored in plain text.
*   Cryptographically secure hashing is implemented using `bcrypt` to prevent unauthorized access even if the database is compromised.

### 3. Two-Factor Authentication (2FA)
*   Integrates `pyotp` for Time-Based One-Time Passwords (TOTP).
*   Generates a unique secure 2FA secret for each newly registered user.
*   A QR code is generated using `qrcode` for users to scan with an authenticator app (like Google Authenticator or Authy).
*   Mandatory 2FA code verification required before granting access to the system.

### 4. JWT Session Management
*   Employs `PyJWT` for stateless authentication tokens.
*   After successful 2FA verification, a JWT is minted containing the user's ID, Role, Name, and Email.
*   Tokens are set to expire securely (e.g., in 1 hour).
*   **Security First:** The token is sent to the client as an `HttpOnly`, `Lax` cookie. This mitigates Cross-Site Scripting (XSS) and Cross-Site Request Forgery (CSRF) attacks by keeping the token inaccessible to frontend JavaScript and preventing it from being sent on cross-site requests.

### 5. Role-Based Access Control (RBAC)
*   A custom `@role_required` decorator restricts access to specific routes based on the JWT payload.
*   Dedicated views for different privilege levels:
    *   **User Dashboard:** Accessible by any authenticated user.
    *   **Manager Panel:** Accessible only by `Manager` and `Admin` roles.
    *   **Admin Panel:** Accessible exclusively by `Admin` roles.

---

## Project Structure

The project follows a clean, modular Blueprint architecture with separation of concerns:

```text
secure-auth/
│
├── app/
│   ├── models/           # Database models (User schema)
│   ├── routes/           # Application endpoints (Blueprints)
│   │   ├── auth_routes.py    # Login, Register, 2FA, Logout
│   │   └── user_routes.py    # Protected Dashboards (User, Manager, Admin)
│   ├── services/         # Core business logic
│   │   ├── auth_service.py   # Registration/Login logic
│   │   └── twofa_service.py  # 2FA code generation & verification
│   ├── utils/            # Helper functions & decorators
│   │   ├── hash_utils.py     # Password hashing & checking
│   │   └── token_utils.py    # JWT minting & @token_required decorator
│   ├── templates/        # HTML templates for rendering
│   └── static/           # CSS stylesheets
│
├── config.py             # Application configuration (Secret keys, DB URI)
├── run.py                # Application entry point
└── requirements.txt      # Python dependencies
```

---

## Application Flow

1.  **Registration:** User creates an account. The password is hashed, a 2FA secret is generated, and a QR code is displayed to the user.
2.  **Login:** User enters their email and password.
3.  **Password Verification:** The system verifies the credentials against the hashed password in the database.
4.  **2FA Prompt:** If credentials are valid, the user is redirected to the 2FA verification screen.
5.  **2FA Verification:** The user inputs the 6-digit code from their authenticator app.
6.  **Token Issuance:** Upon successful verification, the backend generates a JWT and sets it as an `HttpOnly` cookie.
7.  **Access Granted:** The user is redirected to their personalized dashboard, passing through the `@token_required` guard.
8.  **Role Verification:** If the user attempts to access elevated areas (e.g., Admin panel), the `@role_required` decorator parses the JWT to ensure they have the proper authorization.
9.  **Logout:** The authentication cookie is cleared.

---

## Installation & Setup

### Prerequisites
*   Python 3.8+
*   An Authenticator App (Google Authenticator, Authy, etc.)

### Steps

1.  **Create and Activate a Virtual Environment:**
    ```bash
    python -m venv venv
    
    # On Windows:
    venv\Scripts\activate
    
    # On macOS/Linux:
    source venv/bin/activate
    ```

2.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the Application:**
    ```bash
    python run.py
    ```
    *Note: The SQLite database (`instance/secure_auth.db`) will be created automatically upon the first run.*

4.  **Access the App:**
    *   Open your browser and navigate to `http://127.0.0.1:5000/`.
