from app import db
import datetime

class Order(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  order_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
  customer_id = db.Column(db.Integer, index=True)
  customer_name = db.Column(db.String(100), index=True)
  customer_address = db.Column(db.String(100), index=True)

  def __repr__(self):
    return '<Order %r>' % (self.id)
    
