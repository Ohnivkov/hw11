from libgravatar import Gravatar
from src.database.models import User


async def check_exist_user(email, db):
    exist_user = db.query(User).filter(User.email == email).first()
    return exist_user


async def create_new_user(body, db):
    avatar = None
    try:
        g = Gravatar(body.email)
        avatar = g.get_image()
    except Exception as err:
        print(err)
    new_user = User(**body.model_dump(), avatar=avatar)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


async def token_to_db(user, token, db):
    user.refresh_token = token
    db.commit()
    return token


async def find_user_by_email(email, db):
    user = db.query(User).filter(User.email == email).first()
    return user


async def confirmed_email(email: str, db) -> None:
    user = await find_user_by_email(email, db)
    user.confirmed = True
    db.commit()


async def update_avatar(email, url: str, db) -> User:
    user = await find_user_by_email(email, db)
    user.avatar = url
    db.commit()
