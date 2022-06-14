from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, BooleanField, SelectMultipleField, widgets
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from recipes_app.database_functions import get_available_tags
from recipes_app.models import User

'''Plik forms.py zawiera formy wykorzystywane w aplikacji do pobierania danych od użytkownika.'''


class RegistrationForm(FlaskForm):
    """Klasa służy do pobierania i walidacji danych podanych przez użytkownika przy rejestracji konta."""

    username = StringField('Username', validators=[DataRequired(), Length(min=6, max=15)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Create account')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username with that name already exists. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Username with that email already exists. Please choose a different one.')


class LoginForm(FlaskForm):
    """Klasa służy do pobierania i walidacji danych podanych przez użytkownika przy logowaniu do konta."""

    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    """Klasa służy do pobierania i walidacji danych podanych przez użytkownika przy aktualizacji danych konta."""

    username = StringField('Username', validators=[DataRequired(), Length(min=6, max=15)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    profile_picture = FileField('Change profile picture', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Username with that name already exists. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Username with that email already exists. Please choose a different one.')


class MultiCheckboxField(SelectMultipleField):
    """Klasa zmienia pole wielokrotnego wyboru do postaci checkboxów."""

    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class RecipeForm(FlaskForm):
    """Klasa służy do pobierania i walidacji danych podanych przez użytkownika przy dodaniu przepisu do bazy danych."""

    recipe_name = StringField('Recipe name', validators=[DataRequired(), Length(max=100)])
    food_image = FileField('Choose picture', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    description = TextAreaField('Description', validators=[DataRequired()])
    is_private = BooleanField('Set as private')
    tags = MultiCheckboxField('Select tags',
                              choices=get_available_tags())
    submit = SubmitField('Add recipe')


class SearchbarForm(FlaskForm):
    """Klasa służy do pobierania i walidacji danych podanych przez użytkownika przy wyszukiwaniu przepisu w pasku
     wyszukiwania."""

    search = StringField("Search", validators=[DataRequired()])
    submit = SubmitField('Submit')


class FiltersForm(FlaskForm):
    """Klasa służy do pobierania danych podanych przez użytkownika przy wyborze filtrów."""

    filters = MultiCheckboxField("Filter recipes with tags: ", choices=get_available_tags())
    submit = SubmitField('Submit')
