from fastapi import Depends, Query, APIRouter, Path, HTTPException
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.orm import Session
from src.database.auth import auth_service
from src.database.db import get_db
from src.database.models import User
from src.repository import contacts as repository_contacts
from src.schemas import ContactModel, ResponseContactModel
from starlette import status

router = APIRouter(prefix="/contacts", tags=['contacts'])


@router.get("/")
async def get_contacts(limit: int = Query(10, le=100), offset: int = 0, db: Session = Depends(get_db),
                       current_user: User = Depends(auth_service.get_current_user)) -> list[
    ResponseContactModel]:
    contacts = await repository_contacts.get_contacts(limit, offset, db, current_user)
    return contacts


@router.get("/by_id/{contact_id}", response_model=ResponseContactModel)
async def get_contact(contact_id: int = Path(description="The ID of the contact to get", gt=0, le=10),
                      db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.get_contact(contact_id, db, current_user)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not found')
    return contact


@router.get("/by_name/{contact_name}", response_model=ResponseContactModel)
async def get_contact_by_name(contact_name: str, db: Session = Depends(get_db),
                              current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.get_contact_by_name(contact_name, db, current_user)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not found')
    return contact


@router.get("/by_surname/{contact_surname}")
async def get_contact_by_surname(contact_surname: str, db: Session = Depends(get_db),
                                 current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.get_contact_by_surname(contact_surname, db, current_user)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not found')
    return contact


@router.get("/by_email/{contact_email}", dependencies=[Depends(RateLimiter(times=2, seconds=5))],
            response_model=ResponseContactModel)
async def get_contact_by_email(contact_email: str, db: Session = Depends(get_db),
                               current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.get_contact_by_email(contact_email, db, current_user)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not found')
    return contact


@router.get("/get_birthdays")
async def get_birthdays(db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.get_birthdays(db, current_user)
    if contact is None or contact == []:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not found')
    return contact


@router.post("/contact", response_model=ResponseContactModel, status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(RateLimiter(times=2, seconds=5))])
async def create_contact(contact: ContactModel, db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    new_contact = await repository_contacts.create_contacts(contact, db, current_user)

    return new_contact


@router.put("/{contact_id}", response_model=ResponseContactModel)
async def update_contact(body: ContactModel, contact_id: int, db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.update_contact(contact_id, body, db, current_user)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.delete("/{contact_id}", response_model=ResponseContactModel)
async def remove_contact(contact_id: int, db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.remove_contact(contact_id, db, current_user)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact
