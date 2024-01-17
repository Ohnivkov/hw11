from fastapi import Depends, Query, APIRouter, Path, HTTPException
from sqlalchemy.orm import Session
from src.database.db import get_db
from src.repository import contacts as repository_contacts
from src.schemas import ContactModel, ResponseContactModel
from starlette import status

router = APIRouter(prefix="/contacts", tags=['contacts'])


@router.get("/")
async def get_contacts(limit: int = Query(10, le=100), offset: int = 0, db: Session = Depends(get_db)) -> list[
    ResponseContactModel]:
    contacts = await repository_contacts.get_contacts(limit, offset, db)
    return contacts


@router.get("/by_id/{contact_id}", response_model=ResponseContactModel)
async def get_contact(contact_id: int = Path(description="The ID of the contact to get", gt=0, le=10),
                      db: Session = Depends(get_db)):
    contact = await repository_contacts.get_contact(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not found')
    return contact


@router.get("/by_name/{contact_name}", response_model=ResponseContactModel)
async def get_contact_by_name(contact_name: str, db: Session = Depends(get_db)):
    contact = await repository_contacts.get_contact_by_name(contact_name, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not found')
    return contact


@router.get("/by_surname/{contact_surname}", response_model=ResponseContactModel)
async def get_contact_by_surname(contact_surname: str, db: Session = Depends(get_db)):
    contact = await repository_contacts.get_contact_by_surname(contact_surname, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not found')
    return contact


@router.get("/by_email/{contact_email}", response_model=ResponseContactModel)
async def get_contact_by_email(contact_email: str, db: Session = Depends(get_db)):
    contact = await repository_contacts.get_contact_by_email(contact_email, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not found')
    return contact


@router.get("/get_birthdays", response_model=list[ResponseContactModel])
async def get_birthdays(db: Session = Depends(get_db)):
    contact = await repository_contacts.get_birthdays(db)
    if contact is None or contact == []:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not found')
    return contact


@router.post("/contact")
async def create_contact(contact: ContactModel, db: Session = Depends(get_db)):
    new_contact = await repository_contacts.create_contacts(contact, db)
    return new_contact


@router.put("/{contact_id}", response_model=ResponseContactModel)
async def update_contact(body: ContactModel, contact_id: int, db: Session = Depends(get_db)):
    contact = await repository_contacts.update_contact(contact_id, body, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.delete("/{contact_id}", response_model=ResponseContactModel)
async def remove_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = await repository_contacts.remove_contact(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact
