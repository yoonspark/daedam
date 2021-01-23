import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


db = SQLAlchemy()


def setup_db(app):
    """Bind a flask application and a SQLAlchemy service"""
    db.app = app
    db.init_app(app)
    migrate = Migrate(app, db, compare_type=True)


# Create association tables
offer_panelist = db.Table('offer_panelist',
    db.Column('offer_id', db.Integer, db.ForeignKey('Offer.id'), primary_key=True),
    db.Column('panelist_id', db.Integer, db.ForeignKey('Panelist.id'), primary_key=True),
)
call_topic = db.Table('call_topic',
    db.Column('call_id', db.Integer, db.ForeignKey('Call.id'), primary_key=True),
    db.Column('topic_id', db.Integer, db.ForeignKey('Topic.id'), primary_key=True),
)
offer_topic = db.Table('offer_topic',
    db.Column('offer_id', db.Integer, db.ForeignKey('Offer.id'), primary_key=True),
    db.Column('topic_id', db.Integer, db.ForeignKey('Topic.id'), primary_key=True),
)
panelist_topic = db.Table('panelist_topic',
    db.Column('panelist_id', db.Integer, db.ForeignKey('Panelist.id'), primary_key=True),
    db.Column('topic_id', db.Integer, db.ForeignKey('Topic.id'), primary_key=True),
)


class Call(db.Model):
    """Audience's individual request for desired discussion contents"""

    __tablename__ = 'Call'

    # Specify native field(s)
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(1000))
    description = db.Column(db.String())

    def __repr__(self):
        return f'<Call ID: {self.id}>'

    def format(self):
        return {
            'id': self.id,
            'question': self.question,
            'description': self.description,
            'topics': [t.name for t in self.topics],
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()


class Offer(db.Model):
    """Organized (discussion) event based on moderators’ synthesis of audience requests"""

    __tablename__ = 'Offer'

    # Specify native field(s)
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300))
    contents = db.Column(db.String())
    event_time = db.Column(db.DateTime)
    finalized = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Offer ID: {self.id}, title: {self.title}>'

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'contents': self.contents,
            'event_time': self.event_time,
            'finalized': self.finalized,
            'topics': [t.name for t in self.topics],
            'panelists': [p.name for p in self.panelists],
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()


class Panelist(db.Model):
    """Panelist with distinctive experience/expertise"""

    __tablename__ = 'Panelist'

    # Specify native field(s)
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(120))

    # Specify relational field(s)
    offers = db.relationship('Offer', secondary=offer_panelist, backref='panelists', lazy=True)

    def __repr__(self):
        return f'<Panelist ID: {self.id}, name: {self.name}>'

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'city': self.city,
            'state': self.state,
            'phone': self.phone,
            'image_link': self.image_link,
            'facebook_link': self.facebook_link,
            'website': self.website,
            'topics': [t.name for t in self.topics],
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()


class Topic(db.Model):
    """Discussion topic categories"""

    __tablename__ = 'Topic'

    # Specify native field(s)
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    db.UniqueConstraint(name)

    # Specify relational field(s)
    calls = db.relationship('Call', secondary=call_topic, backref='topics', lazy=True)
    offers = db.relationship('Offer', secondary=offer_topic, backref='topics', lazy=True)
    panelists = db.relationship('Panelist', secondary=panelist_topic, backref='topics', lazy=True)

    def __repr__(self):
        return f'<Topic ID: {self.id}, name: {self.name}>'

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()
