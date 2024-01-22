from fastapi import Depends, HTTPException, status, APIRouter, Security
from fastapi.security import OAuth2PasswordRequestForm, HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session
from src.database.auth import auth_service
from src.database.db import get_db
from src.repository import users as repository_users
from src.schemas import UserModel
router = APIRouter(prefix="/users", tags=['users'])
security = HTTPBearer()

@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(body: UserModel, db: Session = Depends(get_db)):
    exist_user = await repository_users.check_exist_user(body, db)
    if exist_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Account already exists")
    new_user = await repository_users.create_new_user(body, auth_service.get_password_hash(body.password), db)
    return {"new_user": new_user}


@router.post("/login", status_code=status.HTTP_201_CREATED)
async def login(body: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = await repository_users.check_exist_user(body, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email")
    if not auth_service.verify_password(body.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password")
    # Generate JWT
    access_token = await auth_service.create_access_token(data={"sub": user.email})
    refresh_token = await auth_service.create_refresh_token(data={"sub": user.email})
    user.refresh_token = await repository_users.token_to_db(user, refresh_token, db)
    return {"access_token": access_token, "token_type": "bearer", "refresh":user.refresh_token}

@router.get('/refresh_token')
async def refresh_token(credentials: HTTPAuthorizationCredentials = Security(security), db: Session = Depends(get_db)):
    token = credentials.credentials
    email = await auth_service.decode_refresh_token(token)
    user = await repository_users.find_user_by_email(email,db)
    if user.refresh_token != token:
         user.refresh_token = await repository_users.token_to_db(user, None, db)
         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

    access_token = await auth_service.create_access_token(data={"sub": email})
    refresh_token = await auth_service.create_refresh_token(data={"sub": email})
    user.refresh_token = await repository_users.token_to_db(user, refresh_token, db)
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}