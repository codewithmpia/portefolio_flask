from flask import redirect, url_for, flash
from flask_admin.form import FileUploadField
from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView, expose
from flask_login import current_user


from .utils import BASE_DIR


class CustomAdminIndexView(AdminIndexView):
    """
        - Restrict access to the Admin 
        - Customize the administration homepage.
    """
    @expose("/")
    def index(self):
        if current_user.is_authenticated and current_user.is_admin:
            return super(CustomAdminIndexView, self).index()
        flash("Une connexion est requise pour accéder à cette page.", "danger")
        return redirect(url_for("login"))


class BaseModelMixin:
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin
    
    def inaccessible_callback(self, *args):
        return redirect(url_for('login'))


class ProjectAdminView(BaseModelMixin, ModelView):
    form_extra_fields = {
        "image": FileUploadField(
            label="Image",
            base_path=str(BASE_DIR / "assets"),
            relative_path="static/images/projects/"
        )
    }
    column_list = ("title", "created_at", "publish")

    def on_model_change(self, form, model, is_created):
        if is_created:
            model.generate_slug()
        return super().on_model_change(form, model, is_created)
    

class ContactAdminView(BaseModelMixin, ModelView):
    column_list = ("name", "email", "created_at")