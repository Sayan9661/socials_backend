# comment_service.py
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from discussion_service import Discussion
from sqlalchemy import ForeignKey

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tmp/social.db'  # Use your own database URI
db = SQLAlchemy(app)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    text = db.Column(db.String(500), nullable=False)
    post_id = db.Column(db.Integer, ForeignKey(Discussion.id))
    user_id = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, default=0)
    replies = db.relationship('Reply', backref='comment', lazy=True)

class Reply(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(500), nullable=False)
    comment_id = db.Column(db.Integer, db.ForeignKey('comment.id'), nullable=False)
    user_id = db.Column(db.Integer, nullable=False)

@app.route('/comments', methods=['POST'])
def create_comment():
    data = request.get_json()
    new_comment = Comment(text=data['text'], post_id=data['post_id'], user_id=data['user_id'])
    db.session.add(new_comment)
    db.session.commit()
    return jsonify({'message': 'New comment created!'})

@app.route('/comments/<id>/like', methods=['POST'])
def like_comment(id):
    comment = Comment.query.get(id)
    if not comment:
        return jsonify({'message': 'Comment not found!'})
    comment.likes += 1
    db.session.commit()
    return jsonify({'message': 'Comment liked!'})

@app.route('/comments/<id>/replies', methods=['POST'])
def reply_comment(id):
    data = request.get_json()
    new_reply = Reply(text=data['text'], comment_id=id, user_id=data['user_id'])
    db.session.add(new_reply)
    db.session.commit()
    return jsonify({'message': 'Reply created!'})

@app.route('/comments/<id>', methods=['GET'])
def get_comment(id):
    comment = Comment.query.get(id)
    if not comment:
        return jsonify({'message': 'Comment not found!'})
    return jsonify({'comment': comment.text})

@app.route('/comments/<id>', methods=['PUT'])
def update_comment(id):
    data = request.get_json()
    comment = Comment.query.get(id)
    if not comment:
        return jsonify({'message': 'Comment not found!'})
    comment.text = data['text']
    db.session.commit()
    return jsonify({'message': 'Comment updated!'})

@app.route('/comments/<id>', methods=['DELETE'])
def delete_comment(id):
    comment = Comment.query.get(id)
    if not comment:
        return jsonify({'message': 'Comment not found!'})
    db.session.delete(comment)
    db.session.commit()
    return jsonify({'message': 'Comment deleted!'})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)