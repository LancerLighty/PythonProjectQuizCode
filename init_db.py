from ext import app, db
from models import Quiz, User
#db reset
with app.app_context():

    db.drop_all()
    db.create_all()

    admin_user = User(username="LancerLighty", email="teklamamphoria4@gmail.com", password="AdminPass123", role="Admin")
    db.session.add(admin_user)
    db.session.commit()