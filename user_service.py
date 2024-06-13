# user_service.py
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os
# from flask_sqlalchemy import relationship


app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tmp/social.db' 
db = SQLAlchemy(app)

followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    mobile_no = db.Column(db.String(15), unique=True, nullable=False)
    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')
    # Children = relationship("Child")

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='scrypt')
    new_user = User(name=data['name'], email=data['email'], password=hashed_password, mobile_no=data['mobile_no'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'New user created!'})

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if not user or not check_password_hash(user.password, data['password']):
        return jsonify({'message': 'Login failed!'})
    return jsonify({'message': 'Logged in successfully!'})


@app.route('/follow', methods=['POST'])
def follow():
    data = request.get_json()
    follower = User.query.get(data['follower_id'])
    followed = User.query.get(data['followed_id'])
    if follower is None or followed is None:
        return jsonify({'message': 'User not found!'})
    if follower == followed:
        return jsonify({'message': 'You can\'t follow yourself!'})
    if followed in follower.followed.all():
        return jsonify({'message': 'You are already following this user!'})
    follower.followed.append(followed)
    db.session.commit()
    return jsonify({'message': 'You are now following ' + followed.name})

@app.route('/unfollow', methods=['POST'])
def unfollow():
    data = request.get_json()
    follower = User.query.get(data['follower_id'])
    followed = User.query.get(data['followed_id'])
    if follower is None or followed is None:
        return jsonify({'message': 'User not found!'})
    if follower == followed:
        return jsonify({'message': 'You can\'t unfollow yourself!'})
    if followed not in follower.followed.all():
        return jsonify({'message': 'You are not following this user!'})
    follower.followed.remove(followed)
    db.session.commit()
    return jsonify({'message': 'You are no longer following ' + followed.name})

@app.route('/search/users', methods=['GET'])
def search_users():
    name = request.args.get('name')
    users = User.query.filter(User.name.contains(name)).all()
    return jsonify({'users': [user.name for user in users]})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
    
    
