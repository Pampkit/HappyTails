from ultralytics import YOLO
import os
import shutil

ru_en_names = {'cat-Abyssinian': 'Абиссинская кошка', 'cat-Bengal': 'Бенгальская кошка', 'cat-Bombay': 'Бомбейская кошка',
               'cat-British_Shorthair': 'Британская короткошерстная кошка', 'cat-Egyptian_Mau':'Египетский мау',
               'cat-Maine_Coon':'Мейн-кун', 'cat-Persian':'Персидская кошка', 'cat-Ragdoll':'Рэгдолл',
               'cat-Russian_Blue':'Русская голубая кошка', 'cat-Siamese':'Сиамская кошка', 'cat-Sphynx':'Сфинкс',
               'dog-american_bulldog':'Американский бульдог', 'dog-american_pit_bull_terrier':'Американский питбультерьер',
               'dog-basset_hound':'Бассет-хаунд', 'dog-beagle':'Бигль', 'dog-boxer':'Боксер', 'dog-chihuahua':'Чихуахуа',
               'dog-english_cocker_spaniel':'Английский кокер-спаниель', 'dog-english_setter':'Английский сеттер',
               'dog-german_shorthaired':'Курцхаар', 'dog-great_pyrenees':'Пиренейская горная', 'dog-havanese':'Гаванский бишон',
               'dog-japanese_chin':'Японский хин', 'dog-keeshond':'Кеесхонд', 'dog-leonberger':'Леонбергер',
               'dog-miniature_pinscher':'Карликовый пинчер', 'dog-newfoundland':'Ньюфаундленд', 'dog-pomeranian':'Померанский шпиц',
               'dog-pug':'Мопс', 'dog-saint_bernard':'Сенбернар', 'dog-samoyed':'Самоед', 'dog-scottish_terrier':'Шотландский терьер',
               'dog-shiba_inu':'Сиба-ину', 'dog-staffordshire_bull_terrier':'Стаффордширский бультерьер',
               'dog-wheaten_terrier':'Ирландский мягкошерстный пшеничный терьер', 'dog-yorkshire_terrier':'Йоркширский терьер'}

def detection_breed(img):
    # определение модели
    model = YOLO('model/best.pt')
    breed_animal = model.names
    # прогонка изображения через модель
    results = model(source=img, show=True, conf=0.1, save_txt=True, save_conf=True)
    txt_file = 'runs/detect/predict/labels/image.txt'
    add_text = ''
    if os.path.exists(txt_file):
        with open(txt_file, 'r') as f:
            data = f.read()
        breed_id = data.split(' ')[0]
        breed_name = breed_animal[int(breed_id)]
        ru_breed_name = ru_en_names[breed_name]
        breed_conf = data.split(' ')[5]
        # проверка на породистость
        if float(breed_conf[:5]) <= 0.80:
            add_text = "Похоже ваш питомец метис, порода, которую удалось обнаружить - "
        if os.path.exists("runs/"):
            shutil.rmtree('runs/')
        else:
            print("The file does not exist")
        return add_text, ru_breed_name
    else:
        if os.path.exists("runs/"):
            shutil.rmtree('runs/')
        else:
            print("The file does not exist")
        return add_text, "Ой, неудалось узнать породу вашего животного, попробуйте другую фотографию"


