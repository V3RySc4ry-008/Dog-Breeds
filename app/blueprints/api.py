import random
from flask import Blueprint, jsonify, current_app
from app.models import Breed, Fact

api_bp = Blueprint('api', __name__)


def make_json(data, status=200):
    import json
    from flask import Response
    payload = json.dumps(data, ensure_ascii=False, indent=2)
    return Response(payload, status=status, mimetype='application/json; charset=utf-8')


@api_bp.route('/breeds', methods=['GET'])
def get_breeds():
    breeds = Breed.query.all()
    return make_json([b.to_dict() for b in breeds])


@api_bp.route('/breeds/<int:breed_id>', methods=['GET'])
def get_breed(breed_id):
    breed = Breed.query.get_or_404(breed_id)
    data = breed.to_dict()
    data['facts'] = [f.to_dict() for f in breed.facts]
    return make_json(data)


@api_bp.route('/random_fact', methods=['GET'])
def random_fact():
    facts = Fact.query.all()
    if not facts:
        return make_json({'error': 'No facts available'}, 404)
    fact = random.choice(facts)
    data = fact.to_dict()
    data['breed_name_ru'] = fact.breed.name_ru
    data['breed_name_en'] = fact.breed.name_en
    return make_json(data)
