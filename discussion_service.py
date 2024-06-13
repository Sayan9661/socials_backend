# discussion_service.py
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from main import User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tmp/social.db'  # Use your own database URI
db = SQLAlchemy(app)

tags = db.Table('tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True),
    db.Column('discussion_id', db.Integer, db.ForeignKey('discussion.id'), primary_key=True)
)

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

class Discussion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(500), nullable=False)
    image = db.Column(db.String(500), nullable=True)
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    user_id = db.Column(db.Integer, ForeignKey(User.id))  
    tags = db.relationship('Tag', secondary=tags, lazy='subquery',
        backref=db.backref('discussions', lazy=True))
    
# create a new discussion/post
@app.route('/discussions', methods=['POST'])
def create_discussion():
    data = request.get_json()
    new_discussion = Discussion(text=data['text'], image=data['image'], user_id=data['user_id'])
    for tag in data['tags']:
        existing_tag = Tag.query.filter_by(name=tag).first()
        if existing_tag:
            new_discussion.tags.append(existing_tag)
        else:
            new_discussion.tags.append(Tag(name=tag))
    db.session.add(new_discussion)
    db.session.commit()
    return jsonify({'message': 'New discussion created!'})

# get the discussion based on id
@app.route('/discussions/<id>', methods=['GET'])
def get_discussion(id):
    discussion = Discussion.query.get(id)
    if not discussion:
        return jsonify({'message': 'Discussion not found!'})
    return jsonify({'discussion': discussion.text, 'image': discussion.image, 'user_id': discussion.user_id, 'tags': [tag.name for tag in discussion.tags]})

# update the discussion
@app.route('/discussions/<id>', methods=['PUT'])
def update_discussion(id):
    data = request.get_json()
    discussion = Discussion.query.get(id)
    if not discussion:
        return jsonify({'message': 'Discussion not found!'})
    discussion.text = data['text']
    discussion.image = data['image']
    discussion.user_id = data['user_id']
    discussion.tags.clear()
    for tag in data['tags']:
        existing_tag = Tag.query.filter_by(name=tag).first()
        if existing_tag:
            discussion.tags.append(existing_tag)
        else:
            discussion.tags.append(Tag(name=tag))
    db.session.commit()
    return jsonify({'message': 'Discussion updated!'})

# delete discussion
@app.route('/discussions/<id>', methods=['DELETE'])
def delete_discussion(id):
    discussion = Discussion.query.get(id)
    if not discussion:
        return jsonify({'message': 'Discussion not found!'})
    db.session.delete(discussion)
    db.session.commit()
    return jsonify({'message': 'Discussion deleted!'})

# search for the discussion based on the text or tags
@app.route('/discussions/search', methods=['GET'])
def search_discussions():
    tags = request.args.getlist('tags')
    text = request.args.get('text')
    query = db.session.query(Discussion)

    if tags:
        query = query.join(Discussion.tags).filter(Tag.name.in_(tags))

    if text:
        query = query.filter(Discussion.text.contains(text))

    discussions = query.all()

    return jsonify([{'discussion': discussion.text, 'image': discussion.image, 'user_id': discussion.user_id, 'tags': [tag.name for tag in discussion.tags]} for discussion in discussions])

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)