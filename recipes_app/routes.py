import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from recipes_app import app, db, bcrypt
from recipes_app.forms import RegistrationForm, LoginForm, UpdateAccountForm, RecipeForm, SearchbarForm, FiltersForm
from recipes_app.models import User, Recipe, Tag
from flask_login import login_user, current_user, logout_user, login_required

'''Plik routes.py zawiera definicje funkcji wykorzystywanych do obsługi i nawigacji po aplikacji webowej we Flasku.'''


@app.route('/', endpoint='home')
@app.route("/home", endpoint='home')
def home():
    """Funkcja wyświetla główny widok aplikacji (widziany jako pierwszy przez użytkownika).
    Widok ten wyświetla listę przepisów z bazy danych posortowaną datą malejąco i z podziałem na strony. """

    page = request.args.get('page', 1, type=int)
    recipes = Recipe.query.filter_by(is_private=False).order_by(Recipe.date_posted.desc()).paginate(page=page,
                                                                                                    per_page=5)
    return render_template("home.html", recipes=recipes)


@app.route("/about", endpoint='about')
def about():
    """Funkcja wyświetla informacje o aplikacji."""

    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'], endpoint='register')
def register():
    """Funkcja służy do obsługi procesu zakładania konta. Zawiera walidację podanych danych, nie pozwala na założenie
    konta zalogowanemu już użytkownikowi."""

    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RegistrationForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('UTF-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created successfully. You can now log in.', 'success')

        return redirect(url_for('login'))

    return render_template("register.html", title="Sign up", form=form)


@app.route("/login", methods=['GET', 'POST'], endpoint='login')
def login():
    """Funkcja służy do obsługi procesu logowania. Zawiera walidację podanych danych, nie pozwala na logowanie
    zalogowanemu już użytkownikowi."""

    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get('next')

            return redirect(next_page) if next_page else redirect(url_for('home'))

        else:
            flash('Unsuccessful login.', 'danger')

    return render_template("login.html", title="Login", form=form)


@app.route("/logout", endpoint='logout')
def logout():
    """Funkcja służy do obsługi procesu wylogowania."""

    logout_user()
    return redirect(url_for('home'))


def save_picture(picture, path):
    """Funkcja pobiera obraz oraz docelowy folder. Zmienia nazwę obrazu szyfrowaniem, standaryzuje jego rozmiar
    oraz zapisuje do wskazanej lokalizacji. Zwraca nową nazwę pliku wraz z rozszerzeniem."""

    random_hex = secrets.token_hex(8)
    _, file_extension = os.path.splitext(picture.filename)
    picture_filename = random_hex + file_extension
    picture_path = os.path.join(path, picture_filename)

    output_picture_size = (300, 300)
    image = Image.open(picture)
    image.thumbnail(output_picture_size)

    image.save(picture_path)

    return picture_filename


@app.route("/account", methods=['GET', 'POST'], endpoint='account')
@login_required
def account():
    """Funkcja służy do wyświetlania informacji o koncie użytkownika. Jest również formularzem pozwalającym na ich
    zmianę przez właściciela konta. Zmienione dane są nadpisywane w bazie danych."""

    form = UpdateAccountForm()

    if form.validate_on_submit():

        if form.profile_picture.data:
            picture_path = os.path.join(app.root_path, 'static/profile_pictures')
            picture_file = save_picture(form.profile_picture.data, picture_path)
            current_user.profile_picture = picture_file

        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Account Info have been updated successfully.', 'success')

        return redirect(url_for('account'))

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    profile_picture = url_for('static', filename='profile_pictures/' + current_user.profile_picture)

    return render_template("account.html", title="Account", profile_picture=profile_picture, form=form)


@app.route("/new_recipe", methods=['GET', 'POST'], endpoint='add_recipe')
@login_required
def add_recipe():
    """Funkcja służy do obsługi formularza dodania przepisu do bazy danych."""

    form = RecipeForm()

    if form.validate_on_submit():
        form.tags.checked = [(tag.id, tag.tag) for tag in Tag.query.all()]
        available_tags = Tag.query.all()
        chosen_tags = []

        for tag in available_tags:
            if tag.tag in form.tags.data:
                chosen_tags.append(tag)

        new_recipe = Recipe(recipe_name=form.recipe_name.data, description=form.description.data, author=current_user,
                            recipe_tags=chosen_tags)
        if form.food_image.data:
            picture_path = os.path.join(app.root_path, 'static/food_images')
            picture_file = save_picture(form.food_image.data, picture_path)
            new_recipe.food_image = picture_file

        db.session.add(new_recipe)
        db.session.commit()
        flash('Your recipe has been uploaded.', 'success')

        return redirect(url_for('home'))

    return render_template("upload_recipe.html", title="New Recipe", form=form, legend="Add recipe")


@app.route("/recipes/<int:recipe_id>", endpoint='show_recipe')
def show_recipe(recipe_id):
    """Funkcja służy do wyświetlania wybranego przepisu wraz ze wszystkimi informacjami. W razie braku przepisu
    o podanym id w bazie danych wyrzucany jest komunikat o błędzie."""

    recipe = Recipe.query.get_or_404(recipe_id)

    if not recipe.is_private or recipe.author == current_user:

        if current_user.is_authenticated:
            icon = '../static/star2.png' if recipe.recipe_name in current_user.favourites else '../static/star.png'

        else:
            icon = '../static/star2.png'

        return render_template("recipe.html", title=recipe.recipe_name, recipe=recipe, icon=icon)

    return render_template("error_message.html", message='Access denied. You are not authorized to do this action.')


@app.route("/recipes/<int:recipe_id>/modify", methods=['GET', 'POST'], endpoint='modify_recipe')
@login_required
def modify_recipe(recipe_id):
    """Funkcja służy do obsługi formularza modyfikacji przepisu. Wyświetla w formularzu do modyfikacji obecne dane
    przepisu, zapisuje zmiany do bazy danych. W razie braku przepisu o podanym id w bazie danych lub jeżeli
    użytkownik, który nie jest autorem przepisu, próbuje wykonać tę akcję, wyrzucany jest komunikat o błędzie. """

    recipe = Recipe.query.get_or_404(recipe_id)

    if recipe.author != current_user:
        abort(403)

    form = RecipeForm()

    if form.validate_on_submit():
        form.tags.checked = [(tag.id, tag.tag) for tag in Tag.query.all()]
        available_tags = Tag.query.all()
        chosen_tags = []

        for tag in available_tags:
            if tag.tag in form.tags.data:
                chosen_tags.append(tag)

        recipe.recipe_tags = chosen_tags

        if form.food_image.data:
            picture_path = os.path.join(app.root_path, 'static/food_images')
            picture_file = save_picture(form.food_image.data, picture_path)
            recipe.food_image = picture_file

        recipe.recipe_name = form.recipe_name.data
        recipe.description = form.description.data
        recipe.is_private = form.is_private.data
        db.session.commit()
        flash('The recipe has been modified.', 'success')

        return redirect(url_for('show_recipe', recipe_id=recipe.id))

    elif request.method == 'GET':
        form.recipe_name.data = recipe.recipe_name
        form.description.data = recipe.description
        form.is_private.data = recipe.is_private
        form.tags.data = recipe.tags

    return render_template("upload_recipe.html", title="Modify Recipe", form=form, legend="Modify recipe")


@app.route("/recipes/<int:recipe_id>/delete", methods=['POST'], endpoint='delete_recipe')
@login_required
def delete_recipe(recipe_id):
    """Funkcja zajmuje się usunięciem przepisu z bazy danych. W razie braku przepisu o podanym id w bazie danych lub
    jeżeli użytkownik, który nie jest autorem przepisu, próbuje wykonać tę akcję, wyrzucany jest komunikat o błędzie.
    """

    recipe = Recipe.query.get_or_404(recipe_id)

    if recipe.author != current_user:
        abort(403)

    db.session.delete(recipe)
    db.session.commit()
    flash('The recipe has been deleted.', 'success')

    return redirect(url_for('home'))


@app.route("/recipes/<int:recipe_id>/manage_favourite", methods=['GET', 'POST'], endpoint='favourite_recipe')
@login_required
def favourite_recipe(recipe_id):
    """Funkcja obsługuje system dodania i usuwania przepisu z ulubionych. Wykonuje odpowiednie operacje na bazie
    danych. W razie braku przepisu o podanym id w bazie danych wyrzucany jest komunikat o błędzie. """

    recipe = Recipe.query.get_or_404(recipe_id)

    if recipe.recipe_name in current_user.favourites:
        current_user.favourite_recipes.remove(recipe)
        flash('The recipe has been removed from favourites.', 'success')

    else:
        current_user.favourite_recipes.append(recipe)
        flash('The recipe has been added to favourites.', 'success')

    db.session.commit()

    return redirect(url_for('show_recipe', recipe_id=recipe.id))


@app.route("/favourite_recipes", endpoint='show_favourite_recipes')
@login_required
def show_favourite_recipes():
    """Funkcja służy do wyświetlania przepisów oznaczonych przez użytkownika zalogowanego jako ulubione."""

    page = request.args.get('page', 1, type=int)
    recipes = Recipe.query.filter(Recipe.recipe_name.in_(current_user.favourites) | (not Recipe.is_private)) \
        .order_by(Recipe.date_posted.desc()).paginate(page=page, per_page=5)

    return render_template("filtered_recipes.html", recipes=recipes, user=current_user,
                           next_page='show_favourite_recipes', title='Favourite recipes')


@app.route("/user/<string:username>", endpoint='show_user_recipes')
def show_user_recipes(username):
    """Funkcja służy do wyświetlania przepisów, których autorem jest użytkownik o podanej nazwie użytkownika. W razie
    nieznalezienia takiego użytkownika w bazie danych zwraca komunikat o błędzie."""

    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    recipes = Recipe.query.filter_by(author=user, is_private=False).order_by(Recipe.date_posted.desc()).paginate(
        page=page, per_page=5)

    return render_template("filtered_recipes.html", recipes=recipes, user=user, next_page='show_user_recipes',
                           title=f'Recipes uploaded by {username}')


@app.route("/my_recipes", endpoint='my_recipes')
@login_required
def my_recipes():
    """Funkcja służy do wyświetlania przepisów, których autorem jest obecny zalogowany użytkownik."""

    page = request.args.get('page', 1, type=int)
    recipes = Recipe.query.filter_by(author=current_user).order_by(Recipe.date_posted.desc()).paginate(
        page=page, per_page=5)

    return render_template("filtered_recipes.html", recipes=recipes, user=current_user, next_page='my_recipes',
                           title='My recipes')


@app.context_processor
def base():
    """Funkcja umożliwia wykorzystanie pola do wyszukiwania przepisu przez użytkownika."""

    form = SearchbarForm()
    return dict(form=form)


@app.route("/search", methods=['POST'], endpoint='search_for_recipe')
def search_for_recipe():
    """Funkcja służy do wyświetlania przepisów, których nazwy zawierają podaną przez użytkownika sekwencję znaków.
    W razie niepoprawnego zapytania lub jego braku zwraca komunikat o błędzie."""

    form = SearchbarForm()

    if form.validate_on_submit():
        search_question = form.search.data
        page = request.args.get('page', 1, type=int)
        recipes = db.session.query(Recipe).filter(
            (Recipe.recipe_name.contains(search_question)) | (not Recipe.is_private)) \
            .order_by(Recipe.date_posted.desc()).paginate(page=page, per_page=5)

        return render_template("filtered_recipes.html", recipes=recipes, user=current_user, form=form,
                               next_page='search_for_recipe', title=f'Search results for "{search_question}"')

    return render_template("error_message.html", message='Your search question was invalid or empty.'
                                                         ' Please try searching for something else.')


@app.route("/filtered_recipes", methods=['POST', 'GET'], endpoint='filter_recipes')
def filter_recipes():
    """Funkcja służy do wyświetlania przepisów, których tagi opisujące zawierają podane przez użytkownika tagi."""

    form = FiltersForm()

    if request.method == 'POST':
        page = request.args.get('page', 1, type=int)
        recipes = Recipe.query.filter_by(is_private=False)

        for tag in form.filters.data:
            recipes = recipes.filter(Recipe.tags.any(Tag.tag == tag))

        recipes = recipes.order_by(Recipe.date_posted.desc()).paginate(page=page, per_page=5)

        return render_template("filtered_recipes.html", recipes=recipes, user=current_user, form=form,
                               next_page='search_for_recipe', title=f'Recipes found')

    elif request.method == 'GET':
        return render_template("filter_recipes.html", form=form)
