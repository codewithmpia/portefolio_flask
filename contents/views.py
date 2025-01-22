from flask import render_template, send_file, redirect, url_for, flash
from flask.views import MethodView
from flask_login import login_user, logout_user, current_user

from .utils import BASE_DIR, get_form_errors
from .models import db, User, Project, Contact
from .forms import ContactForm, LoginForm


class IndexView(MethodView):
    template_name = "index.html"

    def get(self):
        projects = Project.query.filter_by(publish=True).order_by(Project.created_at.desc())
        
        if projects.count() == 0:
            flash("Aucun projet n'est disponible.", "info")
        return render_template(self.template_name, projects=projects)
    

class ProjectView(MethodView):
    template_name = "project.html"

    def get(self, slug):
        project = Project.query.get_or_404(slug)
        return render_template(self.template_name, project=project)
    

class ContactView(MethodView):
    template_name = "contact.html"
    form_class = ContactForm

    def get(self):
        form = self.form_class()
        return render_template(self.template_name, form=form)
    
    def post(self):
        form = self.form_class()

        if form.validate_on_submit():
            name = form.name.data
            email = form.email.data
            message = form.message.data

            new_contact = Contact(
                name=name,
                email=email,
                message=message
            )
            db.session.add(new_contact)
            db.session.commit()
            flash("Message envoyé avec succès.", "success")

            return redirect(url_for("contact"))
        
        elif form.errors:
            get_form_errors(form)

        return render_template(self.template_name, form=form)
    

class DownloadCVView(MethodView):
    cv = f"{BASE_DIR}/assets/static/cv.pdf"

    def get(self):
        return send_file(self.cv, as_attachment=True, mimetype="application/pdf")
    

class LoginView(MethodView):
    template_name = "login.html"
    form_class = LoginForm

    def get(self):
        if current_user.is_authenticated:
            if current_user.is_admin:
                return redirect(url_for("admin.index"))
            else:
                return redirect(url_for("index"))
            
        form = self.form_class()
        return render_template(self.template_name, form=form)
    
    def post(self):
        if current_user.is_authenticated:
            if current_user.is_admin:
                return redirect(url_for("admin.index"))
            else:
                return redirect(url_for("index"))
            
        form = self.form_class()

        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data

            user = User.query.filter_by(username=username).first()

            if not (user and user.check_password(password)):
                flash("Nom d'utilisateur ou mot de passe incorrect.", "danger")
                return redirect(url_for("login"))
            
            login_user(user)

            if user.is_admin:
                flash("Vous êtes connecté en tant qu'admin.", "success")
                return redirect(url_for("admin.index"))
            else:
                flash("Vous êtes connecté.", "info")
                return redirect(url_for("index"))
        
        elif form.errors:
            get_form_errors(form)

        return render_template(self.template_name, form=form)
    

class LogoutView(MethodView):
    def get(self):
        logout_user()
        flash("Vous êtes déconnecté.", "info")
        return redirect(url_for("index"))