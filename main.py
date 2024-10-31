from flask import Flask,redirect,render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)

# CONNECT TO DATABASE
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# Define the Users model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f'<User {self.email}>'
    
    def serialize(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email
        }

with app.app_context():
    db.create_all()

@app.route('/insert-user')
def insert_user():
# List of users to be added
    users_data = [
        {'first_name': 'Bob', 'last_name': 'Brown', 'email': 'bob@example.com', 'password': 'qwerty123'},
        {'first_name': 'Charlie', 'last_name': 'Black', 'email': 'charlie@example.com', 'password': 'letmein321'},
        {'first_name': 'willy', 'last_name': 'Akintunde', 'email': 'williamsolaolu28@gmail.com', 'password': '12345'},
        {'first_name': 'olaolu', 'last_name': 'williams', 'email': 'williamsolaolu2004@gmail.com', 'password': 'willy'},
    ]

    added_users = []
    with app.app_context(): # this help to work within the application context and not outside our app
        for user_data in users_data: # Loop over each user and add them to the database
            existing_user = Users.query.filter_by(email=user_data['email']).first()
            if existing_user:
                break
            else:
            # Add new user if no duplicate found
                new_user = Users(
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
                email=user_data['email'],
                password=user_data['password']
                )
                db.session.add(new_user)
                added_users.append(new_user)
        db.session.commit()

    serialized_users = [user.serialize() for user in added_users]

    return jsonify({"added_users": serialized_users})




@app.route('/')
def home_page():
    return render_template("login.html")

@app.route('/signup')
def signup_page():
    return render_template("signup.html")



if __name__ == '__main__':
    app.run(debug=True)