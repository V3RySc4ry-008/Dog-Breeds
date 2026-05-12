from app import create_app, db
from app.models import Breed, Fact

app = create_app()

def seed():
    with app.app_context():
        # Создаём таблицы, если их нет
        db.create_all()
        
        # Проверяем, есть ли уже данные
        if Breed.query.count() > 0:
            print("Данные уже есть в базе. Пропускаем seed.")
            return
        
        print("Добавляем породы и факты...")
        
        breeds_data = [
            {
                "name_en": "Pug",
                "name_ru": "Мопс",
                "description": "Маленькая китайская порода с плоской мордой и морщинами. Мопсы дружелюбны, любят внимание и много спят.",
                "origin": "Китай",
                "size": "Маленькая",
                "lifespan": "12–15 лет"
            },
            {
                "name_en": "Beagle",
                "name_ru": "Бигль",
                "description": "Английская охотничья гончая с отличным нюхом. Бигли энергичны, любознательны и очень дружелюбны.",
                "origin": "Великобритания",
                "size": "Маленькая/Средняя",
                "lifespan": "12–15 лет"
            },
            {
                "name_en": "Spitz",
                "name_ru": "Шпиц",
                "description": "Пушистая немецкая порода с острой мордой и пышным хвостом. Шпицы умны, преданны и очень энергичны.",
                "origin": "Германия",
                "size": "Маленькая/Средняя",
                "lifespan": "13–15 лет"
            },
            {
                "name_en": "Alabai",
                "name_ru": "Алабай",
                "description": "Среднеазиатская овчарка. Мощная, независимая порода, выведенная для охраны скота и жилья.",
                "origin": "Центральная Азия",
                "size": "Очень крупная",
                "lifespan": "12–15 лет"
            },
            {
                "name_en": "Chihuahua",
                "name_ru": "Чихуахуа",
                "description": "Самая маленькая порода в мире из Мексики. Чихуахуа смелые, преданные хозяину и иногда упрямые.",
                "origin": "Мексика",
                "size": "Очень маленькая",
                "lifespan": "14–16 лет"
            }
        ]
        
        facts_data = {
            "Pug": [
                "Мопсы были любимцами китайских императоров.",
                "Название породы происходит от латинского 'pugnus' — кулак.",
                "Мопсы громко храпят из-за строения морды."
            ],
            "Beagle": [
                "Бигль — одна из древнейших пород гончих.",
                "У бигля отличное обоняние — их используют в аэропортах.",
                "Бигли могут есть почти всё, что найдут."
            ],
            "Spitz": [
                "Шпицы были собаками королевы Виктории.",
                "У них двойная шерсть, которая почти не линяет.",
                "Шпицы очень громко лают и любят 'поговорить'."
            ],
            "Alabai": [
                "Алабай способен в одиночку справиться с волком.",
                "Порода формировалась естественным отбором без человека.",
                "Алабаи очень независимы и требуют твёрдой руки."
            ],
            "Chihuahua": [
                "Чихуахуа — собака с самым большим мозгом относительно размеров тела.",
                "Их предки жили в древней Мексике ещё до ацтеков.",
                "Чихуахуа живут до 16-18 лет."
            ]
        }
        
        # Создаём породы
        breeds = {}
        for data in breeds_data:
            breed = Breed(
                name_en=data["name_en"],
                name_ru=data["name_ru"],
                description=data["description"],
                origin=data["origin"],
                size=data["size"],
                lifespan=data["lifespan"]
            )
            db.session.add(breed)
            db.session.flush()
            breeds[data["name_en"]] = breed
        
        db.session.commit()
        
        # Добавляем факты
        for name_en, fact_list in facts_data.items():
            breed = breeds.get(name_en)
            if breed:
                for fact_text in fact_list:
                    fact = Fact(content=fact_text, breed_id=breed.id)
                    db.session.add(fact)
        
        db.session.commit()
        print(f"✅ Добавлено {len(breeds_data)} пород и факты к ним!")

if __name__ == "__main__":
    seed() 
