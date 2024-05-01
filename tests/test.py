import pytest
from datetime import date
from models import Users, Applications, Animals


def test_new_user():
    """
    Дано: модель бд User
    Когда: создание нового пользователя
    Проверяется: поля модели заполняются корректно
    """
    user = Users(name="Ольга", surname="Воронова", name2="Александровна", number='89134562323',
                 email="olya2004@gmail.com", login="olyka", password="olya12345", role=0)
    assert user.name == "Ольга"
    assert user.surname == "Воронова"
    assert user.name2 == "Александровна"
    assert user.number == "89134562323"
    assert user.email == "olya2004@gmail.com"
    assert user.login == "olyka"
    assert user.password == "olya12345"
    assert user.role == 0


def test_new_app():
    """
    Дано: модель бд Applications
    Когда: создание новой заявки
    Проверяется: поля модели заполняются корректно
    """
    a = date.today()
    app = Applications(name="Дмитрий Иванов", animal="Кузя", number="+79159444720", date=a)
    assert app.name == "Дмитрий Иванов"
    assert app.animal == "Кузя"
    assert app.number == "+79159444720"
    assert app.date == a


def test_new_animal():
    """
    Дано: модель бд Animals
    Когда: создание нового животного
    Проверяется: поля модели заполняются корректно
    """
    app = Animals(name="Лапа", description="Моя любимая кошка", photo="lapa.jpg", kind='Кошка', age=7, gender='female')
    assert app.name == "Лапа"
    assert app.description == "Моя любимая кошка"
    assert app.photo == "lapa.jpg"
    assert app.kind == 'Кошка'
    assert app.age == 7
    assert app.gender == 'female'