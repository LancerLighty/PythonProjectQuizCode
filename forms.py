from flask_wtf import FlaskForm
from wtforms.fields import StringField, EmailField, PasswordField, SubmitField, IntegerField, RadioField
from wtforms.validators import DataRequired, length, equal_to, ValidationError
from flask_wtf.file import FileField, FileRequired, FileSize, FileAllowed
from models import User


class RegisterForm(FlaskForm):
    profile_img = FileField("Upload your profile picture:", validators=[FileAllowed(["jpg", "png"])])
    username = StringField("Enter Username", validators=[DataRequired(), length(min=8)])
    email = EmailField("Enter Email address", validators=[DataRequired()])
    password = PasswordField("Enter Password", validators=[DataRequired(), length(min=8,
                                                                                  message="Password must have at least 8 characters")])
    repeat_password = PasswordField("Repeat Password", validators=[DataRequired(), length(min=8), equal_to('password',
                                                                                                           message='Passwords must match')])
    submit = SubmitField("Register")

    def validate_passwerd(self, field):
        number = True
        capitalLetters = True
        smallLetters = True
        simbols = True
        for field_letter in field.data:
            if field_letter in "qwertyuiopasdfghjklzxcvbnm":
                smallLetters = False
            if field_letter in "QWERTYUIOPASDFGHJKLZXCVBNM":
                capitalLetters = False
            if field_letter in "1234567890":
                number = False
            if field_letter in "!@#$%&*":
                simbols = False
        if smallLetters:
            raise ValidationError("Password must have at least one small letter")
        if capitalLetters:
            raise ValidationError("Password must have at least one capital letter")
        if number:
            raise ValidationError("Password must have at least one number")
        if simbols:
            raise ValidationError("Password must have at least one of these simbols: !@#$%&*")

    def validate_username(self, field):
        user = User.query.filter(User.username == field.data).first()
        if user != None:
            raise ValidationError("User with this Username already exists")

    def validate_username(self, field):
        for field_letter in field.data:
            if not field_letter.lower() in "qwertyuiopasdfghjklzxcvbnm1234567890":
                raise ValidationError("Username can contain only letters")

    def validate_email(self, field):
        user = User.query.filter(User.email == field.data).first()
        if user != None:
            raise ValidationError("User with this Email already exists")

    def validate_email(self, field):
        if not field.data.endswith("@gmail.com"):
            raise ValidationError("You must enter Google Account Email")


class QuizForm(FlaskForm):
    name = StringField("Enter Name:", validators=[DataRequired()])
    submit = SubmitField("Save")


class QuestionForm(FlaskForm):
    quiz_id = IntegerField()
    question = StringField(validators=[DataRequired()])
    correct_answer = StringField(validators=[DataRequired()])
    wrong_answer_one = StringField(validators=[DataRequired()])
    wrong_answer_two = StringField(validators=[DataRequired()])
    wrong_answer_three = StringField(validators=[DataRequired()])
    submit = SubmitField("Save")


class LoginForm(FlaskForm):
    username_email = StringField("Enter your Username or Email:", validators=[DataRequired()])
    password = StringField("Enter password:", validators=[DataRequired()])
    submit = SubmitField("Login")


class editProfieForm(FlaskForm):
    profile_img = FileField("Upload your profile picture:", validators=[FileAllowed(["jpg", "png"])])
    username = StringField("Username:", validators=[DataRequired()])
    email = StringField("Email:", validators=[DataRequired()])
    new_password = StringField("Password:", validators=[DataRequired()])
    submit = SubmitField("Save")


class StartQuizForm(FlaskForm):
    answer = RadioField('Your Answer', choices=[], coerce=str)
    submit = SubmitField("Next")


class DeleteUserFrom(FlaskForm):
    password = StringField("Password:", validators=[DataRequired()])
    submit = SubmitField("Delete Account")
