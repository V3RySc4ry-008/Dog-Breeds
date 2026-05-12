"""One-off script to update breed image URLs to verified working ones."""
from app import create_app, db
from app.models import Breed

IMAGES = {
    'Pug':       'https://images.dog.ceo/breeds/pug/n02110958_13721.jpg',
    'Beagle':    'https://images.dog.ceo/breeds/beagle/n02088364_10108.jpg',
    'Spitz':     'https://images.dog.ceo/breeds/pomeranian/n02112018_1495.jpg',
    'Alabai':    'https://images.dog.ceo/breeds/mastiff-tibetan/n02108551_658.jpg',
    'Chihuahua': 'https://images.dog.ceo/breeds/chihuahua/n02085620_7613.jpg',
}

app = create_app()
with app.app_context():
    for name_en, url in IMAGES.items():
        breed = Breed.query.filter_by(name_en=name_en).first()
        if breed:
            breed.image_url = url
            print(f'✓ {name_en}: {url}')
        else:
            print(f'✗ Not found: {name_en}')
    db.session.commit()
    print('Done.')
