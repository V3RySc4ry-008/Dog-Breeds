import hashlib
from datetime import date
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import Breed, Fact, Like

main_bp = Blueprint('main', __name__)


def get_fact_of_the_day():
    facts = Fact.query.all()
    if not facts:
        return None
    today = date.today().isoformat()
    idx = int(hashlib.md5(today.encode()).hexdigest(), 16) % len(facts)
    return facts[idx]


@main_bp.route('/')
def index():
    breeds = Breed.query.all()
    fact_of_day = get_fact_of_the_day()
    return render_template('index.html', breeds=breeds, fact_of_day=fact_of_day, title='Факты о породах собак')


@main_bp.route('/breed/<int:breed_id>')
def breed_detail(breed_id):
    breed = Breed.query.get_or_404(breed_id)
    liked_fact_ids = set()
    if current_user.is_authenticated:
        liked_fact_ids = {
            like.fact_id for like in Like.query.filter_by(user_id=current_user.id).all()
        }
    return render_template(
        'breed_detail.html',
        breed=breed,
        liked_fact_ids=liked_fact_ids,
        title=f'{breed.name_ru} ({breed.name_en})'
    )


@main_bp.route('/like/<int:fact_id>', methods=['POST'])
@login_required
def toggle_like(fact_id):
    fact = Fact.query.get_or_404(fact_id)
    existing = Like.query.filter_by(user_id=current_user.id, fact_id=fact_id).first()
    if existing:
        db.session.delete(existing)
        db.session.commit()
        liked = False
    else:
        like = Like(user_id=current_user.id, fact_id=fact_id)
        db.session.add(like)
        db.session.commit()
        liked = True

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({'liked': liked, 'count': fact.like_count})

    return redirect(request.referrer or url_for('main.breed_detail', breed_id=fact.breed_id))
