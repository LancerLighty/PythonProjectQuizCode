from ext import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login  import UserMixin
class Score(db.Model):
    __tablename__ = "score"
    id = db.Column(db.Integer(), primary_key=True)
    quiz_id = db.Column(db.String(), nullable=False)
    quiz_name = db.Column(db.String(), nullable=False)
    user_id = db.Column(db.String(), nullable=False)
    score = db.Column(db.String(), nullable=False)
    max_score = db.Column(db.String(), nullable=False)
class Quiz(db.Model):

    __tablename__ = "quizzes"

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), nullable=False)

class Question(db.Model):

    __tablename__ = "questions"

    id = db.Column(db.Integer(), primary_key=True)
    quiz_id = db.Column(db.Integer, nullable=False)
    question = db.Column(db.String, nullable=False)
    correct_answer = db.Column(db.String, nullable=False)
    wrong_answer_one = db.Column(db.String, nullable=False)
    wrong_answer_two = db.Column(db.String, nullable=False)
    wrong_answer_three = db.Column(db.String, nullable=False)

class User(db.Model, UserMixin):

    __tablename__ = "user"
    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(), nullable=False)
    username = db.Column(db.String(), nullable=False)
    password = db.Column(db.String(), nullable=False)
    profile_img = db.Column(db.String(), default="default.jpg")
    role = db.Column(db.String(), default="Guest")

    def __init__(self, username, email, password, role="Guest"):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)
        self.role = role
    def check_password(self, password):
        return check_password_hash(self.password, password)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
