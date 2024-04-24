from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_login import LoginManager, login_user, login_required, current_user, logout_user

from detection import detection_breed
from models import Animals, Users, db, Orders, Breeds
from werkzeug.security import generate_password_hash, check_password_hash
from PIL import Image
import os
from datetime import date

app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = 'secret-key-goes-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///animal.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# связываем приложение и экземпляр SQLAlchemy
db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    animal_help_img_list = ["1.png", "2.png", "3.png", "4.png", "5.png", "6.png"]
    animal_help_desc_list = [" Старушке Цыганке необходимо проверить здоровье!",
                             "Старичкам находящимся на постоянном обеспечении приюта нужна поддержка!",
                             "Серкан в беде!", "У Тузика рак, ему нужна помощь!",
                             "Друзья, срочно нужна помощь нашему старичку!", " КРУГЕТС НЕ МОЖЕТ ХОДИТЬ!"]
    return render_template('about.html', img=animal_help_img_list, desc=animal_help_desc_list)


@app.route('/cats')
def cats():
    # выборка кошек из бд животных
    cats_list = Animals.query.filter_by(kind='Кошка').all()
    return render_template('cats.html', cats_list=cats_list)


@app.route('/dogs')
def gods():
    # выборка собак из бд животных
    dogs_list = Animals.query.filter_by(kind='Собака').all()
    return render_template('dogs.html', dogs_list=dogs_list)


@app.route('/animal_cart/<int:animal_id>')
def animal_cart(animal_id):
    # выборка животного по его id
    single_animal = Animals.query.filter_by(id=animal_id).all()
    # проверка на авторизованного пользователя и его животных
    if current_user.is_authenticated:
        order_user_single_animal = Orders.query.filter_by(id_user=current_user.id, id_animal=animal_id).first()
    else:
        order_user_single_animal = "sorry"
    return render_template('animal_cart.html', single_animal=single_animal,
                           order_user_single_animal=order_user_single_animal)


@app.route('/care')
def care():
    return render_template('care.html')


@app.route('/form/<string:animal_name>')
@login_required
def form(animal_name):
    animal = Animals.query.filter_by(name=animal_name).first()
    gender = animal.gender
    today = date.today().day
    an_id = animal.id
    return render_template('form.html', animal_name=animal_name, gender=gender, today=today, anim_id=animal.id)


@app.route('/submit_form', methods=['POST'])
def submit_form():
    if request.method == 'POST':
        count = request.form['amount']  # Получаем данные из формы
        description = request.form['purpose']
        email = request.form['email']
        date_now = date.today()
        animal_id = request.form['animal_id']  # Получаем идентификатор животного из формы
        user_id = request.form['user_id']

        # Создаем новую запись в базе данных
        new_order = Orders(id_user=user_id, id_animal=animal_id, count=count, description=description, date=date_now,
                           email=email)

        # Добавляем новую запись в сессию и сохраняем ее в базе данных
        db.session.add(new_order)
        db.session.commit()

        return redirect(url_for('user_cabinet'))  # Перенаправляем пользователя на страницу успеха


@app.route('/user_cabinet')
@login_required
def user_cabinet():
    animals_users = []
    orders = Orders.query.filter_by(id_user=current_user.id).all()
    for i in range(len(orders)):
        animal = Animals.query.filter_by(id=orders[i].id_animal).all()
        animals_users.append(animal[0])
    return render_template('user_cabinet.html', name=current_user.name, animals_users=animals_users, orders=orders)


@app.route('/admin_cabinet')
@login_required
def admin_cabinet():
    all_orders = Orders.query.all()
    all_users = Users.query.filter_by(role=0).all()
    users_animals = {}
    for i in range(len(all_users)):
        id_user = all_users[i].id
        users_animals[str(id_user)] = ''
        for j in range(len(all_orders)):
            if all_orders[j].id_user == id_user:
                name_animal = Animals.query.filter_by(id=all_orders[j].id_animal).first()
                users_animals[str(id_user)] += name_animal.name + " "
    print(users_animals)

    return render_template('admin_cabinet.html', name=current_user.name, all_users=all_users,
                           users_animals=users_animals)


@app.route('/delete_animal/<int:animal_id>', methods=['GET'])
def delete_animal(animal_id):
    print(animal_id)
    order = Orders.query.filter_by(id_user=current_user.id, id_animal=animal_id).first_or_404()
    db.session.delete(order)
    db.session.commit()
    return redirect(url_for('user_cabinet'))


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login_post():
    login = request.form.get('login')
    password = request.form.get('password')
    user = Users.query.filter_by(login=login).first()
    if not user or user.password != password:
        return redirect(url_for('login'))

    if user.role == 0:
        login_user(user)  # вход пользователя
        return redirect(url_for('user_cabinet'))
    else:
        login_user(user)
        return redirect(url_for('admin_cabinet'))


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route('/register', methods=['GET'])
def register():
    return render_template('register.html')


@app.route('/register', methods=['POST'])
def register_post():
    # получение данных с формы
    login = request.form.get('login')
    surname = request.form.get('surname')
    name = request.form.get('name')
    name2 = request.form.get('name')
    number = request.form.get('number')
    email = request.form.get('email')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')
    # проверка, что такого пользователя еще нет
    user = Users.query.filter_by(
        login=login).first()  # if this returns a user, then the email already exists in database
    if user or password != confirm_password:
        return redirect(url_for('register'))
    # создание нового пользователя
    new_user = Users(name=name, surname=surname, name2=name2, number=number, email=email, login=login,
                     password=password, role=0)
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('login'))


@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return Users.query.get(int(user_id))


@app.route('/breed')
def breed():
    return render_template('breed.html', breed_detected=session.pop('breed_detected', None),
                           breed_health=session.pop('breed_health', None),
                           breed_activity=session.pop('breed_activity', None),
                           breed_nutrition=session.pop('breed_nutrition', None),
                           breed_grooming=session.pop('breed_grooming', None))


@app.route('/upload', methods=['POST'])
def upload():
    # чтение загруженного файла
    file = request.files['file']
    img = file.read()
    with open('image.jpg', 'wb') as f:
        f.write(img)
    # детекция породы
    name_breed = detection_breed('image.jpg')
    care_breed = Breeds.query.filter_by(animal_breed=name_breed).first()
    # определение переменных сессии для последующей рекомендации
    if name_breed == 'Ой, неудалось узнать породу вашего животного, попробуйте другую фотографию':
        session['breed_detected'] = 'Ой, неудалось узнать породу вашего животного, попробуйте другую фотографию'
        session['breed_health'] = ''
        session['breed_activity'] = ''
        session['breed_nutrition'] = ''
        session['breed_grooming'] = ''
    else:
        session['breed_detected'] = name_breed
        session['breed_health'] = care_breed.health
        session['breed_activity'] = care_breed.activity
        session['breed_nutrition'] = care_breed.nutrition
        session['breed_grooming'] = care_breed.grooming

    if os.path.exists("image.jpg"):
        os.remove('image.jpg')
    else:
        print("The file does not exist")
    return redirect(url_for('breed'))


if __name__ == "__main__":
    app.run(debug=True)
