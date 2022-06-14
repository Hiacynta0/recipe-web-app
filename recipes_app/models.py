from datetime import datetime
from flask_login import UserMixin
from recipes_app import db, login_manager
from sqlalchemy.ext.associationproxy import association_proxy

'''Plik models.py zawiera komponenty na podstawie, których tworzona jest baza danych, z której korzysta reszta plików
z aplikacji.'''


@login_manager.user_loader
def load_user(user_id):
    """Funkcja bierze jako argument id użytkownika i zwraca użytkownika o tym id."""
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    """Klasa jest modelem użytkownika, wykorzystywanym do przechowywania informacji o użytkownikach w bazie danych."""

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    profile_picture = db.Column(db.String(20), nullable=False, default='default_profile_picture.jpg')
    password = db.Column(db.String(60), nullable=False)
    uploaded_recipes = db.relationship('Recipe', backref='author', lazy=True)
    favourite_recipes = db.relationship('Recipe', secondary=lambda: users_favourites_table)

    favourites = association_proxy("favourite_recipes", "recipe_name")

    def __repr__(self):
        return f'({self.username}, {self.email})'


class Recipe(db.Model):
    """Klasa jest modelem przepisu, wykorzystywanym do przechowywania informacji o przepisach w bazie danych."""

    id = db.Column(db.Integer, primary_key=True)
    recipe_name = db.Column(db.String(60), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    food_image = db.Column(db.String(20), nullable=False, default='default_food_image.jpg')
    description = db.Column(db.String(500), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    is_private = db.Column(db.Boolean, nullable=False, default=False)
    recipe_tags = db.relationship("Tag", secondary=lambda: recipes_tags_table)

    tags = association_proxy("recipe_tags", "tag")

    def __repr__(self):
        return f'({self.recipe_name}, {self.author})'


class Tag(db.Model):
    """Klasa jest modelem tagu, wykorzystywanym do przechowywania informacji o tagach w bazie danych."""

    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(30))

    def __repr__(self):
        return self.tag


recipes_tags_table = db.Table(
    'recipes_tags_table',
    db.Model.metadata,
    db.Column("recipe.id", db.Integer, db.ForeignKey("recipe.id"), primary_key=True),
    db.Column("tag.id", db.Integer, db.ForeignKey("tag.id"), primary_key=True),
)

users_favourites_table = db.Table(
    'recipes_favourites_table',
    db.Model.metadata,
    db.Column("user.id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
    db.Column("recipe.id", db.Integer, db.ForeignKey("recipe.id"), primary_key=True),
)

