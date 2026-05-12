import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import Breed

app = create_app()

with app.app_context():
    # Проверяем, есть ли поле image_url в таблице breeds
    from sqlalchemy import inspect
    inspector = inspect(db.engine)
    columns = [col['name'] for col in inspector.get_columns('breeds')]
    
    if 'image_url' not in columns:
        print("❌ Поле image_url отсутствует в таблице breeds!")
        print("Запусти сначала: flask db migrate -m 'add image_url' && flask db upgrade")
    else:
        # Словарь с прямыми ссылками на рабочие картинки
        images = {
            "Мопс": "https://upload.wikimedia.org/wikipedia/commons/f/f0/Pug_portrait.jpg",
            "Бигль": "https://upload.wikimedia.org/wikipedia/commons/5/55/Beagle_600.jpg",
            "Шпиц": "https://upload.wikimedia.org/wikipedia/commons/7/7e/German_Spitz.jpg",
            "Алабай": "https://upload.wikimedia.org/wikipedia/commons/8/8e/Central_Asian_Shepherd_Dog.jpg",
            "Чихуахуа": "https://upload.wikimedia.org/wikipedia/commons/3/34/Chihuahua_dog.jpg"
        }
        
        updated = 0
        for breed in Breed.query.all():
            if breed.name_ru in images:
                breed.image_url = images[breed.name_ru]
                print(f"✅ {breed.name_ru} — картинка добавлена")
                updated += 1
        
        db.session.commit()
        print(f"\n🎉 Обновлено {updated} пород!")
        print("Теперь обнови сайт — картинки появятся.")
