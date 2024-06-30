from flask import Flask


from ext import app
if __name__ == "__main__":
    from routes import home, quizzeslist, login, register, quiz
app.run(debug=True)