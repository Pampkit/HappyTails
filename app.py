from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_login import LoginManager, login_user, login_required, current_user

from models import Animals, Users, db
from werkzeug.security import generate_password_hash, check_password_hash

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
    cats_list = Animals.query.filter_by(kind='Кошка').all()
    if current_user.is_authenticated:
        print('cats', current_user.name)
    else:
        print('no')
    return render_template('cats.html', cats_list=cats_list)


@app.route('/dogs')
def gods():
    dogs_list = Animals.query.filter_by(kind='Собака').all()
    return render_template('dogs.html', dogs_list=dogs_list)


@app.route('/animal_cart/<int:animal_id>')
def animal_cart(animal_id):
    single_animal = Animals.query.filter_by(id=animal_id).all()
    print(single_animal)
    return render_template('animal_cart.html', single_animal=single_animal)


@app.route('/help')
def help():
    return render_template('help.html')


@app.route('/form')
def form():
    return render_template('form.html')


@app.route('/user_cabinet')
@login_required
def user_cabinet():
    return render_template('user_cabinet.html', name=current_user.name)


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

    # if the above check passes, then we know the user has the right credentials
    login_user(user)
    return redirect(url_for('user_cabinet'))


@app.route('/register', methods=['GET'])
def register():
    return render_template('register.html')


@app.route('/register', methods=['POST'])
def register_post():
    login = request.form.get('login')
    name = request.form.get('name')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')

    user = Users.query.filter_by(
        login=login).first()  # if this returns a user, then the email already exists in database
    print(user)
    if user or password != confirm_password:  # if a user is found or password != confirm_password, we want to redirect back to signup page so user can try again
        return redirect(url_for('register'))

    new_user = Users(name=name, login=login, password=password, role=0)
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('login'))


@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return Users.query.get(int(user_id))


if __name__ == "__main__":
    app.run(debug=True)
