from main import db
from models.a_users import UserSQL

db.create_all()

db.session.add(UserSQL('dupa','dupa3'))
db.session.add(UserSQL('dupa2','dudp234'))

db.session.commit()