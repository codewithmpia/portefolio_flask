from flask_wtf import FlaskForm
from wtforms.fields import StringField, EmailField, TextAreaField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email


class ContactForm(FlaskForm):
    name = StringField(
        label="Votre nom",
        validators=[DataRequired(message="Le champ nom est requis.")],)
    email = EmailField(
        label="Votre adresse email",
        validators=[
            DataRequired(message="Le champ email est requis."), 
            Email(message="Adresse email invalide.")],)
    message = TextAreaField(
        label="Votre message",
        validators=[DataRequired(message="Le champ message est requis.")],)
    submit = SubmitField(label="Envoyer")


class LoginForm(FlaskForm):
    username = StringField(
        label="Nom d'utilisateur",
        validators=[DataRequired(message="Le champ nom d'utilisateur est requis.")],)
    password = PasswordField(
        label="Mot de passe",
        validators=[DataRequired(message="Le champ mot de passe est requis.")],)
    submit = SubmitField(label="Se connecter")