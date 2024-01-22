from sqlalchemy.orm import Session
from src.database.models import User


async def check_exist_user(body,db):
    exist_user = db.query(User).filter(User.email == body.username).first()
    return exist_user
async def create_new_user(body,password, db):
    new_user = User(email=body.username, password=password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
async def token_to_db(user,token,db):
    user.refresh_token=token
    db.commit()
    return token
async def find_user_by_email(email,db):
    user = db.query(User).filter_by(email=email).first()
    return user
