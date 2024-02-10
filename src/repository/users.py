from libgravatar import Gravatar
from src.database.models import User


async def check_exist_user(email, db):
    """
                check exist user

                :param email: the email to check user for.
                :type email: str
                :param db: The database session.
                :type db: Session
                :return: The user with the specified email, or None if it does not exist.
                :rtype: User | None
                """
    exist_user = db.query(User).filter(User.email == email).first()
    return exist_user


async def create_new_user(body, db):
    """
                Create a new user

                :param body: The detail of user.
                :type body: UserModel
                :param db: The database session.
                :type db: Session
                :return: The new user.
                :rtype: User | None
                """
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
    """
            put refresh token to db

            :param token: the refresh token for user.
            :type token: str
            :param db: The database session.
            :type db: Session
            :param user: The user to put refresh token to db for
            :type user: User
            :return: The user with the specified email, or None if it does not exist.
            :rtype: User | None
            """
    user.refresh_token = token
    db.commit()
    return token


async def find_user_by_email(email, db):
    """
        Get contact with the specified email for a specific user

        :param email: the email of user.
        :type email: str
        :param db: The database session.
        :type db: Session
        :return: The user with the specified email, or None if it does not exist.
        :rtype: User | None
        """
    user = db.query(User).filter(User.email == email).first()
    return user


async def confirmed_email(email: str, db) -> None:
    """
        Confirmation of email

        :param email: the email of user.
        :type email: str
        :param db: The database session.
        :type db: Session
        :return: Nothing.
        :rtype: None
        """
    user = await find_user_by_email(email, db)
    user.confirmed = True
    db.commit()


async def update_avatar(email, url: str, db) -> User:
    """
            Update user avatar

            :param url: The photo to udpate.
            :type url: str
            :param email: the email of user.
            :type email: str
            :param db: The database session.
            :type db: Session
            :return: Nothing.
            :rtype: None
            """
    user = await find_user_by_email(email, db)
    user.avatar = url
    db.commit()
