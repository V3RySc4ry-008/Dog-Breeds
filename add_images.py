import os
import sys

# Добавляем путь к проекту
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import Breed

app = create_app()

def add_images():
    with app.app_context():
        # Задаём соответствие: русское название породы → имя файла картинки
        # ТЫ МОЖЕШЬ МЕНЯТЬ ЭТИ ИМЕНА ФАЙЛОВ НА СВОИ!
        images_map = {
            "Мопс": "pug.jpg",
            "Бигль": "beagle.jpg",
            "Шпиц": "spitz.jpg",
            "Алабай": "alabai.jpg",
            "Чихуахуа": "chihuahua.jpg"
        }
        
        breeds = Breed.query.all()
        updated = 0
        
        for breed in breeds:
            if breed.name_ru in images_map:
                # Формируем путь: /static/images/breeds/имя_файла
                breed.image_url = f"/static/images/breeds/{images_map[breed.name_ru]}"
                print(f"✅ {breed.name_ru} → {breed.image_url}")
                updated += 1
            else:
                print(f"⚠️ {breed.name_ru} — не найдено в словаре")
        
        db.session.commit()
        print(f"\n🎉 Обновлено {updated} пород.")
        print("📁 Теперь загрузи свои картинки в папку: app/static/images/breeds/")
        print("   Имена файлов должны соответствовать указанным выше:")

if __name__ == "__main__":
    add_images()
