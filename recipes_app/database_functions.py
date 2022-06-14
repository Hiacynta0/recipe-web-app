from recipes_app import db
from recipes_app.models import Tag


def upload_tags_to_database():
    """Funkcja przechowuje jako zmienną listę tagów. Na podstawie tej listy dodawane są tagi do bazy danych."""

    available_tags = ['breakfast', 'dinner', 'supper', 'dessert', 'vegetarian', 'vegan', 'ketogenic', 'gluten free',
                      'lactose free']

    for tag in available_tags:
        db.session.add(Tag(tag=tag))
    db.session.commit()


def get_available_tags():
    """Funkcja zwraca zapisane w bazie danych tagi."""
    return [tag.tag for tag in Tag.query.all()]
