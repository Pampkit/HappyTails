from flask import Flask, render_template

from models import Animals,Users, db
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///animal.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# связываем приложение и экземпляр SQLAlchemy
db.init_app(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    animal_help_img_list = ["1.png","2.png","3.png","4.png","5.png","6.png"]
    animal_help_desc_list = [" Старушке Цыганке необходимо проверить здоровье!", "Старичкам находящимся на постоянном обеспечении приюта нужна поддержка!", "Серкан в беде!", "У Тузика рак, ему нужна помощь!", "Друзья, срочно нужна помощь нашему старичку!", " КРУГЕТС НЕ МОЖЕТ ХОДИТЬ!"]
    return render_template('about.html',img=animal_help_img_list,desc=animal_help_desc_list)

if __name__ == "__main__":
    app.run(debug=True)
