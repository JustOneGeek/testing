from app import db
from datetime import datetime as dt

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    description = db.Column(db.Text)
    price= db.Column(db.Float)
    img = db.Column(db.String)
    category_id = db.Column(db.ForeignKey('category.id'))
    created_on = db.Column(db.DateTime, index=True, default=dt.utcnow)
    
    def __repr__(self):
        return f'<Item: {self.id} | {self.name}...>'
                  
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def from_dict(self, data):
        for field in ['name', 'description', 'price', 'img', 'category_id']:
            if field in data: # checks againt the keys of a dict`
                setattr(self, field, data[field])

    def to_dict(self):
        data = {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "img": self.img,
            "category_id": self.category_id,
            "created_on": self.created_on
        }
        return data



class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    products = db.relationship('Item', cascade='all, delete-orphan', backref='category',lazy=True)

    def __repr__(self):
        return f'<Category: {self.id} | {self.name}>'

    def to_dict(self):
        data={
            "id":self.id,
            "name":self.name,
        }
        return data

    def from_dict(self, data):
        self.name=data['name']

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()