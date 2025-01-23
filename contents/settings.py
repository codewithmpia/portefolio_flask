from flask import Flask, g, flash, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_login import LoginManager, current_user
from flask_vite import Vite

from . import utils

# Flask app configuration
app = Flask(
    __name__,
    template_folder=str(utils.BASE_DIR / "assets/templates"),
    static_folder=str(utils.BASE_DIR / "assets/static"),
)
app.config["SECRET_KEY"] = utils.get_env_vars("SECRET_KEY", "top secret")

# Database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = utils.get_env_vars(
    "DATABASE_URL", 
    f"sqlite:///{utils.BASE_DIR}/db.sqlite3"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# Vite configuration
app.config["VITE_AUTO_INSERT"] = True
vite = Vite(app)

# Template filters
app.add_template_filter(utils.format_markdown, "md")

from .models import User, Project, Contact
from .admin import CustomAdminIndexView, ProjectAdminView, ContactAdminView
from .views import IndexView, ProjectView, ContactView, DownloadCVView, LoginView, LogoutView

# Error handlers
@app.errorhandler(404)
def page_not_found(e):
    e.description = "La page que vous recherchez n'existe pas."
    flash(e.description, "danger")
    projects = Project.query.filter_by(publish=True).order_by(Project.created_at.desc()).limit(4)
    return render_template("404.html", projects=projects)

# Admin setup
admin = Admin(
    app, 
    name="Portfolio", 
    index_view=CustomAdminIndexView(
        name="Tableau de bord",
        template="admin/index.html",
    )
)
admin.add_view(ProjectAdminView(Project, db.session))
admin.add_view(ContactAdminView(Contact, db.session))

# Flask-Login setup
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message = "La connexion est requise."

@login_manager.user_loader
def load_user(id):
    return User.query.get(id)

@app.before_request
def get_current_user():
    g.user = current_user

# URL rules for views
app.add_url_rule("/", view_func=IndexView.as_view("index"))
app.add_url_rule("/<string:slug>/", view_func=ProjectView.as_view("project"))
app.add_url_rule("/contact/", view_func=ContactView.as_view("contact"))
app.add_url_rule("/download/", view_func=DownloadCVView.as_view("download"))
app.add_url_rule("/login/", view_func=LoginView.as_view("login"))
app.add_url_rule("/logout/", view_func=LogoutView.as_view("logout"))