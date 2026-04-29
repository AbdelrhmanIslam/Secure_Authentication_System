from flask import Flask
from app.models.user_model import db
from app.routes.auth_routes import auth_bp
from config import Config

def create_app():
    app = Flask(__name__, template_folder='app/templates', static_folder='app/static')
    app.config.from_object(Config)

    # Initialize DB
    db.init_app(app)

    # Register Blueprints
    app.register_blueprint(auth_bp)
    
    # import and register the user routes blueprint for all protected app pages
    from app.routes.user_routes import user_bp
    app.register_blueprint(user_bp)

    return app


app = create_app()

# Create tables automatically
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)