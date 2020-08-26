from app import db
from _datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login
from hashlib import md5

# a model is typically a python class with attributes that match the columns of
# a corresponding database table


followers = db.Table(
    'followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)

# User class inherits from db.Model
# this class defines several fields as class variables
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    # db.realtionship to define relationship in the model class
    # User: is the right side entity, left side is the parent class
    # secondary: configures the association table that is used for this relationship
    # primaryjoin: indicates condition that links the left side entity (follower) with the association table
    # secondaryjoin: indicates the condition that links the right side entity (followed) w/ the association table
    # backref: defines how the relationship will be accessed from the right side entity
    # lazy: 
    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'),
        lazy='dynamic'
    )

    # high level overview of the relationship b/w users and posts
    # one-to-many relationship
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    # generate hash from given password
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # check if password and hash match
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # return the URL of the user's avatar image, scaled to the requested size in pixels
    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    # issues a query on the followed relationship to check if a link b/w users already exists
    def is_following(self, user):
        # filter() can include arbitrary filtering conditions
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0

    # join: yields a list of all post that are followed by some users
    # filter: filter the posts based on the current user_id
    # order_by: sort by timestamp in descending order
    # union: include own posts
    def followed_posts(self):
        followed = Post.query.join(
            followers,
            (followers.c.followed_id==Post.user_id)
        ).filter(
            followers.c.follower_id == self.id
        )
        own = Post.query.filter_by(user_id=self.id)
        return followed.union(own).order_by(Post.timestamp.desc())

    # tells Python how to pront objects of this class
    # useful for debugging
    def __repr__(self):
        return '<User {}>'.format(self.username)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    # tells Python how to pront objects of this class
    # useful for debugging
    def __repr__(self):
        return '<Post {}>'.format(self.body)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))