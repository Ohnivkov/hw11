import cloudinary
import cloudinary.uploader
from fastapi import Depends, HTTPException, status, APIRouter, Security, BackgroundTasks, Request, UploadFile, File
from fastapi.security import OAuth2PasswordRequestForm, HTTPAuthorizationCredentials, HTTPBearer
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.orm import Session
from src.conf.config import config
from src.database.auth import auth_service
from src.database.db import get_db
from src.database.models import User
from src.repository import users as repository_users
from src.schemas import UserModel, RequestEmail
from src.services.email import send_email

router = APIRouter(prefix="/users", tags=['users'])
security = HTTPBearer()


@router.get("/me/")
async def read_users_me(current_user: User = Depends(auth_service.get_current_user)):
    """
       Get a user that authenticated

       :param current_user: The user to get.
       :type current_user: User
       :return: The User, or None if it does not exist.
       :rtype: User | None
       """
    return current_user


@router.patch('/avatar')
async def update_avatar_user(file: UploadFile = File(), current_user: User = Depends(auth_service.get_current_user),
                             db: Session = Depends(get_db)):
    """
                Update user avatar

                :param file: The photo to udpate.
                :type file: str
                :param current_user: User that update avatar for.
                :type current_user: User
                :param db: The database session.
                :type db: Session
                :return: User
                :rtype: User | None
                """
    cloudinary.config(
        cloud_name=config.CLD_NAME,
        api_key=config.CLD_API_KEY,
        api_secret=config.CLD_API_SECRET,
        secure=True,
    )
    r = cloudinary.uploader.upload(file.file, public_id=f'NotesApp/{current_user.username}', overwrite=True)
    src_url = cloudinary.CloudinaryImage(f'NotesApp/{current_user.username}') \
        .build_url(width=250, height=250, crop='fill', version=r.get('version'))

    await repository_users.update_avatar(current_user.email, src_url, db)
    user = await repository_users.find_user_by_email(current_user.email, db)
    return {"user": user}


@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(body: UserModel, bt: BackgroundTasks, request: Request, db: Session = Depends(get_db)):
    """
                Sign up

                :param body: detail of user.
                :type body: UserModel
                :param bt: additional tasks.
                :type bt: BackgroundTasks
                :param request: request.
                :type request: Request
                :param db: The database session.
                :type db: Session
                :return: user that sign up.
                :rtype: User | None
                """
    exist_user = await repository_users.check_exist_user(body.email, db)
    if exist_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Account already exists")
    body.password = auth_service.get_password_hash(body.password)
    new_user = await repository_users.create_new_user(body, db)
    bt.add_task(send_email, new_user.email, new_user.username, str(request.base_url))
    return {"new_user": new_user}


@router.post("/login", status_code=status.HTTP_201_CREATED)
async def login(body: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
                    Login

                    :param body: detail of user.
                    :type body: OAuth2PasswordRequestForm
                    :param db: The database session.
                    :type db: Session
                    :return: user that login.
                    :rtype: dict | None
                    """
    user = await repository_users.check_exist_user(body.username, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email")
    if not user.confirmed:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Email not confirmed")
    if not auth_service.verify_password(body.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password")
    # Generate JWT
    access_token = await auth_service.create_access_token(data={"sub": user.email})
    refresh_token = await auth_service.create_refresh_token(data={"sub": user.email})
    user.refresh_token = await repository_users.token_to_db(user, refresh_token, db)
    return {"access_token": access_token, "token_type": "bearer", "refresh": user.refresh_token}


@router.get('/refresh_token', dependencies=[Depends(RateLimiter(times=2, seconds=5))])
async def refresh_token(credentials: HTTPAuthorizationCredentials = Security(security), db: Session = Depends(get_db)):
    """
                    Get a refresh token

                    :param credentials: detail of user.
                    :type credentials: HTTPAuthorizationCredentials
                    :param db: The database session.
                    :type db: Session
                    :return: access_token, refresh_token, token_type.
                    :rtype: dict | None
                    """
    token = credentials.credentials
    email = await auth_service.decode_refresh_token(token)
    user = await repository_users.find_user_by_email(email, db)
    if user.refresh_token != token:
        user.refresh_token = await repository_users.token_to_db(user, None, db)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

    access_token = await auth_service.create_access_token(data={"sub": email})
    refresh_token = await auth_service.create_refresh_token(data={"sub": email})
    user.refresh_token = await repository_users.token_to_db(user, refresh_token, db)
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@router.get('/confirmed_email/{token}')
async def confirmed_email(token: str, db: Session = Depends(get_db)):
    """
                    Check confirmed email

                    :param token: user token.
                    :type token: str
                    :param db: The database session.
                    :type db: Session
                    :return: The status of confirmation.
                    :rtype: dict | None
                    """
    email = await auth_service.get_email_from_token(token)
    user = await repository_users.find_user_by_email(email, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Verification error")
    if user.confirmed:
        return {"message": "Your email is already confirmed"}
    await repository_users.confirmed_email(email, db)
    return {"message": "Email confirmed"}


@router.post('/request_email')
async def request_email(body: RequestEmail, bt: BackgroundTasks, request: Request,
                        db: Session = Depends(get_db)):
    """
                Check confirmed email

                :param body: email of user.
                :type body: RequestEmail
                :param bt: additional tasks.
                :type bt: BackgroundTasks
                :param request: request.
                :type request: Request
                :param db: The database session.
                :type db: Session
                :return: user that sign up.
                :rtype: dict | None
                """
    user = await repository_users.find_user_by_email(body.email, db)

    if user.confirmed:
        return {"message": "Your email is already confirmed"}
    if user:
        bt.add_task(send_email, user.email, user.username, str(request.base_url))
        return {"message": "Check your email for confirmation."}
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email")
