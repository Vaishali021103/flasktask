from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
# from passlib.hash import sha256_crypt
# import bcrypt


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///main_dbs1.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SECURITY_PASSWORD_HASH'] = 'bcrypt'
# app.config['SECURITY_PASSWORD_SALT'] = b'$2b$12$wqKlYjmOfXPghx3FuC3Pu.'

db = SQLAlchemy(app)

class Register(db.Model):
    regno = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    contactno = db.Column(db.Unicode(20))
    password_hash = db.Column(db.String(100),nullable=False)
    # c_pass = db.Column(db.String(100),nullable=False)

    @property
    def password(self):
        raise AttributeError('password is not found')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    


@app.route("/", methods=['Get', 'POST'])
def index():

    if request.method =="POST":
       fullname = request.form['fullname']
       username = request.form['username']
       email = request.form['email']
       contactno = request.form['contactno']
       set_password = request.form['password']
    #    c_pass = request.form['c_pass']
    
       register = Register(fullname=fullname,username=username,
    email=email,
    password=set_password,
    contactno=contactno)
       db.session.add(register)
       db.session.commit()
    return render_template("register.html")

@app.route("/login", methods=['Get', 'POST'])
def login():
    if request.method=='POST':
        username = request.form['username']
        password = request.form['password']
        user = Register.query.filter_by(username = username).first()
        password_hash=user.password
        if(check_password_hash(password,password_hash)):
            return render_template("home.html")
        else:
            return render_template("login.html")
    return render_template("login.html")

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)