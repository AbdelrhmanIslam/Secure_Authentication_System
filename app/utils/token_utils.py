import jwt
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify, g, current_app

def generate_token(user_id, user_role, user_name, user_email):
    # purpose: after a user passes both password check and 2FA,
    # we mint a JWT that proves who they are for all future requests
    
    # set the token to expire 1 hour from the current time to limit the window of risk
    expiry = datetime.utcnow() + timedelta(hours=1)
    
    # build the payload dictionary containing the user's identity and permissions
    payload = {
        'user_id': user_id,
        'role': user_role,
        'name': user_name,
        'email': user_email,
        'exp': expiry
    }
    
    # sign the payload with our app's secret key using the HS256 algorithm to prevent tampering
    token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')
    
    # return the final minted token as a string
    return token

def token_required(route_function):
    # purpose: a decorator we place on any route that should only
    # be accessible to logged-in users — it reads the JWT from the
    # request cookie, validates it, and passes the decoded user info
    # into the route function
    
    @wraps(route_function)
    def wrapper(*args, **kwargs):
        # grab the JWT from the client's request cookies
        token = request.cookies.get('auth_token')
        
        # if the user didn't send a token, block the request and demand login
        if not token:
            return jsonify({'error': 'Login required — no token found'}), 401
            
        try:
            # attempt to decode and verify the token using our secret key
            decoded_payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            
            # store the verified user data in the Flask global object so the route can use it
            g.current_user = decoded_payload
            
        except Exception:
            # catch any decoding errors (like expired or tampered tokens) and reject the request
            return jsonify({'error': 'Token is invalid or has expired'}), 401
            
        # if the token is valid, proceed to execute the requested route function
        return route_function(*args, **kwargs)
        
    # return the wrapped function to the Flask router
    return wrapper
