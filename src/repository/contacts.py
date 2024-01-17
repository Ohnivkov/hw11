from datetime import datetime, timedelta

from sqlalchemy import extract
from sqlalchemy.orm import Session
from src.database.models import Contact
from src.schemas import ContactModel


async def get_contacts(limit, offset, db: Session):
    contacts = db.query(Contact).limit(limit).offset(offset).all()
    return contacts


async def create_contacts(contact, db: Session):
    new_contact = Contact(name=contact.name,
                          surname=contact.surname,
                          email=contact.email,
                          phone=contact.phone,
                          birth_date=contact.birth_date,
                          description=contact.description)
    db.add(new_contact)
    db.commit()
    db.refresh(new_contact)
    return new_contact


async def get_contact(contact_id, db):
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    return contact


async def get_contact_by_name(contact_name, db):
    contact = db.query(Contact).filter(Contact.name == contact_name).first()
    return contact


async def get_contact_by_surname(contact_surname, db):
    contact = db.query(Contact).filter(Contact.surname == contact_surname).first()
    return contact


async def get_contact_by_email(contact_email, db):
    contact = db.query(Contact).filter(Contact.email == contact_email).first()
    return contact


async def get_birthdays(db):
    now = datetime.now().date()
    after = now + timedelta(days=7)
    birth_day = extract('day', Contact.birth_date)
    birth_month = extract('month', Contact.birth_date)
    contacts = db.query(Contact).filter(
        birth_month == extract('month', now),
        birth_day.between(extract('day', now), extract('day', after))).all()
    return contacts


async def update_contact(contact_id: int, body: ContactModel, db: Session) -> Contact | None:
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        contact.name = body.name
        contact.surname = body.surname
        contact.email = body.email
        contact.phone = body.phone
        contact.description = contact.description
        db.commit()
    return contact


async def remove_contact(contact_id: int, db: Session) -> Contact | None:
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact
