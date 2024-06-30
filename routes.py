from flask import Flask, render_template, redirect
from os import path
from forms import RegisterForm, QuizForm, QuestionForm, LoginForm,editProfieForm, StartQuizForm, DeleteUserFrom
from ext import app
from models import User, Quiz, Question, db, Score
from flask_login import login_user, logout_user, login_required, current_user
import random
from sqlalchemy import and_, or_
from decorators import role_required, logout_required
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
@logout_required(redirect_to='home')
def login():
    forms = LoginForm()
    if forms.validate_on_submit():

        user = User.query.filter(or_(User.username == forms.username_email.data, User.email == forms.username_email.data)).first()
        if user and user.check_password(forms.password.data):
            login_user(user)
            return redirect("/")
    print(forms.errors)
    return render_template("login.html", form=forms)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/login")
@app.route("/register", methods=["GET", "POST"])
@logout_required(redirect_to='home')
def register():
    forms = RegisterForm()
    if forms.validate_on_submit():
        new_user = User(
            username=forms.username.data,
            email=forms.email.data,
            password=forms.password.data
        );
        image = forms.profile_img.data
        if image != None:
            directory = path.join(app.root_path, "static", "images", image.filename)
            image.save(directory)
            new_user.profile_img = image.filename

        db.session.add(new_user)
        db.session.commit()
        return redirect("/login")
    return render_template("register.html", form=forms)


@app.route("/quizzes")
def quizzeslist():
    quizzes = Quiz.query.all()
    return render_template("quizzes.html", quizzes=quizzes)


@app.route("/quizzes/add_quiz", methods=["GET", "POST"])
@role_required('Admin')
def new_quiz():
    forms = QuizForm()
    if forms.validate_on_submit():
        new_quiz = Quiz(name=forms.name.data)
        db.session.add(new_quiz)
        db.session.commit()
        return redirect("/quizzes")
    return render_template("add_quiz.html", form=forms)
@app.errorhandler(403)
def forbidden(e):
    return render_template('index.html')


@app.route("/quizzes/edit_quiz/<int:quiz_id>", methods=["GET", "POST"])
@role_required('Admin')
def edit_quiz(quiz_id):
    quiz = Quiz.query.get(quiz_id)
    forms = QuizForm(name=quiz.name)
    if forms.validate_on_submit():
        quiz.name = forms.name.data
        db.session.commit()
        return redirect("/quizzes")
    return render_template("add_quiz.html", form=forms)


@app.route("/quizzes/edit_questions/<int:quiz_id>", methods=["GET", "POST"])
@role_required('Admin')
def edit_questions(quiz_id):
    questions = Question.query.filter(Question.quiz_id == quiz_id).all()
    quiz = Quiz.query.get(quiz_id)
    forms = QuestionForm()
    if forms.validate_on_submit():
        new_question = Question(question=forms.question.data,
                                quiz_id=quiz_id,
                                correct_answer=forms.correct_answer.data,
                                wrong_answer_one=forms.wrong_answer_one.data,
                                wrong_answer_two=forms.wrong_answer_two.data,
                                wrong_answer_three=forms.wrong_answer_three.data)
        db.session.add(new_question)
        db.session.commit()
        return redirect(f"/quizzes/edit_questions/{quiz_id}")
    return render_template("edit_questions.html", form=forms, quiz=quiz.name, questions=questions, role="admin")




@app.route("/quizzes/delete_quiz/<int:quiz_id>", methods=["GET", "POST"])
@role_required('Admin')
def delete_quiz(quiz_id):
    quiz = Quiz.query.get(quiz_id)
    db.session.delete(quiz)
    db.session.commit()
    return redirect("/quizzes")

@app.route("/quizzes/delete_questions/<int:question_id>", methods=["GET", "POST"])
@role_required('Admin')
def delete_question(question_id):
    question = Question.query.get(question_id)
    quiz_id= question.quiz_id
    db.session.delete(question)
    db.session.commit()
    return redirect(f"/quizzes/edit_questions/{quiz_id}")


@app.route("/quizzes/<int:quiz_id>/<int:question_id>/<int:score>", methods=["GET", "POST"])
def quiz(quiz_id,question_id,score):

    quiz = Quiz.query.get(quiz_id)
    questions = Question.query.all()
    questions = [question for question in questions if question.quiz_id == quiz_id]
    qustions_count = len(questions)
    question = questions[question_id]
    answers = [
        question.correct_answer,
        question.wrong_answer_one,
        question.wrong_answer_two,
        question.wrong_answer_three
    ]
    shuffled_answers = random.sample(answers, len(answers))
    forms = StartQuizForm()
    forms.answer.choices = shuffled_answers
    quiz_not_finished = True
    you_need_to_log_in = False
    new_score_added = False
    old_score_updated = False
    if forms.validate_on_submit():
        if(forms.answer.data == question.correct_answer):
            score +=1
        if(question_id + 1 != qustions_count):
            return redirect(f"/quizzes/{quiz_id}/{question_id + 1}/{score}")
        else:
            quiz_not_finished = False;
            if current_user:
                print("user found.")
                user_score = Score.query.filter(and_(Score.user_id == current_user.id, Score.quiz_id == quiz_id)).first()
                if user_score:
                    user_score.score = score
                    db.session.commit()
                    print("score found.")
                    old_score_updated = True
                else:
                    print("score not found.")
                    quiz_name = Quiz.query.get(quiz_id).name
                    new_quiz_score = Score(quiz_id = quiz_id,
                                            score = score,
                                           user_id = current_user.id,
                                           quiz_name = quiz_name,
                                           max_score = qustions_count)
                    db.session.add(new_quiz_score)
                    db.session.commit()
                    new_score_added = True
            else:
                print("user not found.")
                you_need_to_log_in = True

    return render_template("quiz.html",old_score_updated=old_score_updated,new_score_added=new_score_added,you_need_to_log_in=you_need_to_log_in,form=forms,score=score,quiz_not_finished=quiz_not_finished, qustions_count=qustions_count, quiz=quiz, questions=questions, index=question_id)

@app.route("/profile_settings", methods=["GET", "POST"])
@login_required
def profile_settings():
    user = User.query.get(current_user.id)
    form = editProfieForm(email = user.email,
                          username=user.username,
                          profile_img=user.profile_img,
                          new_password= user.password)
    if form.validate_on_submit():
        image = form.profile_img.data
        print(user.profile_img)
        directory = path.join(app.root_path, "static", "images", image.filename)
        image.save(directory)
        user.profile_img = image.filename
        user.username = form.username.data
        user.email = form.email.data
        print("changed")
        db.session.commit()
    return render_template("profile_settings.html", form=form)
@app.route("/delete_account", methods=["GET", "POST"])
@login_required
def delete_account():
    delete_account = DeleteUserFrom()
    passwords_match = False
    if delete_account.validate_on_submit():
        print("delete")
        user = User.query.filter(User.id == current_user.id).first()
        if user and user.check_password(delete_account.password.data):
            db.session.delete(user)
            db.session.commit()
            return redirect("/")
        else:
            passwords_match = True
    return render_template("delete_user.html",passwords_match=passwords_match, delete_account=delete_account)
@app.route("/myscore", methods=["GET", "POST"])
@login_required
def my_score():
    scores = Score.query.filter(Score.user_id == current_user.id ).all()
    no_scores = False
    if len(scores) == 0:
        no_scores = True
    return render_template("my_score.html", no_scores=no_scores, scores=scores)