from datetime import datetime, timezone
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    avatar = db.Column(db.String(256), nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    likes = db.relationship('Like', back_populates='user', cascade='all, delete-orphan')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def has_liked(self, fact_id):
        return Like.query.filter_by(user_id=self.id, fact_id=fact_id).first() is not None

    def __repr__(self):
        return f'<User {self.username}>'


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


class Breed(db.Model):
    __tablename__ = 'breeds'

    id = db.Column(db.Integer, primary_key=True)
    name_en = db.Column(db.String(100), nullable=False)
    name_ru = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    origin = db.Column(db.String(100), nullable=True)
    size = db.Column(db.String(50), nullable=True)
    lifespan = db.Column(db.String(50), nullable=True)
    image_url = db.Column(db.String(256), nullable=True)

    facts = db.relationship('Fact', back_populates='breed', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'name_en': self.name_en,
            'name_ru': self.name_ru,
            'description': self.description,
            'origin': self.origin,
            'size': self.size,
            'lifespan': self.lifespan,
        }

    def __repr__(self):
        return f'<Breed {self.name_en}>'


class Fact(db.Model):
    __tablename__ = 'facts'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    breed_id = db.Column(db.Integer, db.ForeignKey('breeds.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    breed = db.relationship('Breed', back_populates='facts')
    likes = db.relationship('Like', back_populates='fact', cascade='all, delete-orphan')

    @property
    def like_count(self):
        return len(self.likes)

    def to_dict(self):
        return {
            'id': self.id,
            'content': self.content,
            'breed_id': self.breed_id,
            'like_count': self.like_count,
        }

    def __repr__(self):
        return f'<Fact {self.id}>'


class Like(db.Model):
    __tablename__ = 'likes'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    fact_id = db.Column(db.Integer, db.ForeignKey('facts.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    user = db.relationship('User', back_populates='likes')
    fact = db.relationship('Fact', back_populates='likes')

    __table_args__ = (
        db.UniqueConstraint('user_id', 'fact_id', name='unique_user_fact_like'),
    )

    def __repr__(self):
        return f'<Like user={self.user_id} fact={self.fact_id}>'
