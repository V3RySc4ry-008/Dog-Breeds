from app import create_app, db
from app.models import Breed

app = create_app()

with app.app_context():
    images = {
        "Pug": "https://images.dog.ceo/breeds/pug/pug.jpg",
        "Beagle": "https://images.dog.ceo/breeds/beagle/beagle.jpg",
        "Spitz": "https://images.dog.ceo/breeds/spitz/spitz.jpg",
        "Alabai": "https://images.dog.ceo/breeds/centralasian-1.jpg",
        "Chihuahua": "https://images.dog.ceo/breeds/chihuahua/chihuahua.jpg"
    }
    
    for breed in Breed.query.all():
        if breed.name_en in images:
            breed.image_url = images[breed.name_en]
            print(f"✅ {breed.name_ru} — картинка добавлена")
    
    db.session.commit()
    print("🎉") 
