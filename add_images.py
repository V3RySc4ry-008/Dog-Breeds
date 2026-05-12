import os
import sys

# Добавляем путь к проекту
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import Breed

app = create_app()

def add_images():
    with app.app_context():
        # Словарь с русскими названиями и ссылками на картинки
        images = {
            "Мопс": "https://images.dog.ceo/breeds/pug/pug.jpg",
            "Бигль": "https://images.dog.ceo/breeds/beagle/beagle.jpg",
            "Шпиц": "https://images.dog.ceo/breeds/spitz/spitz.jpg",
            "Алабай": "https://images.dog.ceo/breeds/centralasian-1.jpg",
            "Чихуахуа": "https://images.dog.ceo/breeds/chihuahua/chihuahua.jpg"
        }
        
        # Получаем всех собак из БД
        breeds = Breed.query.all()
        
        updated = 0
        for breed in breeds:
            # Ищем по русскому названию
            if breed.name_ru in images:
                breed.image_url = images[breed.name_ru]
                print(f"✅ {breed.name_ru} — картинка добавлена")
                updated += 1
            else:
                print(f"⚠️ {breed.name_ru} — не найдено в словаре")
        
        db.session.commit()
        print(f"🎉")

if __name__ == "__main__":
    add_images() 
