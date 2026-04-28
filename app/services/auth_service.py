from app.models.user_model import User, db
from app.utils.hash_utils import hash_password, verify_password
from app.services.twofa_service import generate_2fa_secret

def register_user(name, email, password, role):
    hashed = hash_password(password)
    secret = generate_2fa_secret()

    user = User(
        name=name,
        email=email,
        password=hashed,
        role=role,
        twofa_secret=secret
    )

    db.session.add(user)
    db.session.commit()

    return user


def login_user(email, password):
    user = User.query.filter_by(email=email).first()

    if not user:
        return None

    if not verify_password(password, user.password):
        return None

    return user