from datetime import datetime, timedelta

from sqlalchemy import extract
from sqlalchemy.orm import Session
from src.database.models import Contact, User
from src.schemas import ContactModel


async def get_contacts(limit, offset, db: Session, current_user: User):
    """
        Get list of contacts with the specified number of them for a specific user.

        :param offset: The number of contacts to skip.
        :type offset: int
        :param limit: The maximum number of contact to return.
        :type limit: int
        :param current_user: The user to retrieve contacts for.
        :type current_user: User
        :param db: The database session.
        :type db: Session
        :return: A list of contacts.
        :rtype: List[Contact]
        """
    contacts = db.query(Contact).filter(Contact.user_id == current_user.id).limit(limit).offset(offset).all()
    return contacts


async def create_contacts(contact, db: Session, current_user):
    """
        Creates a new contact for a specific user.

        :param contact: The data for the contact to create.
        :type contact: ContactModel
        :param current_user: The user to create the contact for.
        :type current_user: User
        :param db: The database session.
        :type db: Session
        :return: The newly created contact.
        :rtype: Contact
        """
    new_contact = Contact(**contact.model_dump(exclude_unset=True), user_id=current_user.id)
    db.add(new_contact)
    db.commit()
    db.refresh(new_contact)
    return new_contact


async def get_contact(contact_id, db, current_user):
    """
        Get contact with the specified id for a specific user

        :param contact_id: The ID of the contacts to retrieve.
        :type contact_id: int
        :param current_user: The user to retrieve the contact for.
        :type current_user: User
        :param db: The database session.
        :type db: Session
        :return: The contact with the specified ID, or None if it does not exist.
        :rtype: Contact | None
        """
    contact = db.query(Contact).filter(Contact.user_id == current_user.id).filter(Contact.id == contact_id).first()
    return contact


async def get_contact_by_name(contact_name, db, current_user):
    """
                Get contact with the specified name for a specific user.

                :param contact_name: The email of the contact to get.
                :type contact_name: str
                :param current_user: The user to update the contact for.
                :type current_user: User
                :param db: The database session.
                :type db: Session
                :return: The contact with the specified name, or None if it does not exist.
                :rtype: Contact | None
                """
    contact = db.query(Contact).filter(Contact.user_id == current_user.id).filter(Contact.name == contact_name).first()
    return contact


async def get_contact_by_surname(contact_surname, db, current_user):
    """
                Get contact with the specified surname for a specific user.

                :param contact_surname: The surname of the contact to get.
                :type contact_surname: str
                :param current_user: The user to update the contact for.
                :type current_user: User
                :param db: The database session.
                :type db: Session
                :return: The contact with the specified email, or None if it does not exist.
                :rtype: Contact | None
                """
    contact = db.query(Contact).filter(Contact.user_id == current_user.id).filter(
        Contact.surname == contact_surname).first()
    return contact


async def get_contact_by_email(contact_email, db, current_user):
    """
            Get contact with the specified email for a specific user.

            :param contact_email: The email of the contact to get.
            :type contact_email: str
            :param current_user: The user to update the contact for.
            :type current_user: User
            :param db: The database session.
            :type db: Session
            :return: The contact with the specified email, or None if it does not exist.
            :rtype: Contact | None
            """
    contact = db.query(Contact).filter(Contact.user_id == current_user.id).filter(
        Contact.email == contact_email).first()
    return contact


async def get_birthdays(db, current_user):
    """
        Get contacts with the specified birthdays for a specific user.

        :param current_user: The user to update the contact for.
        :type current_user: User
        :param db: The database session.
        :type db: Session
        :return: The contact with the specified email, or None if it does not exist.
        :rtype: Contact | None
        """
    now = datetime.now().date()
    after = now + timedelta(days=7)
    birth_day = extract('day', Contact.birth_date)
    birth_month = extract('month', Contact.birth_date)
    contacts = db.query(Contact).filter(Contact.user_id == current_user.id).filter(
        birth_month == extract('month', now),
        birth_day.between(extract('day', now), extract('day', after))).all()
    return contacts


async def update_contact(contact_id: int, body: ContactModel, db: Session, current_user) -> Contact | None:
    """
        Updates a single contact with the specified ID for a specific user.

        :param contact_id: The ID of the contact to update.
        :type contact_id: int
        :param body: The updated data for the contact.
        :type body: ContactModel
        :param current_user: The user to update the contact for.
        :type current_user: User
        :param db: The database session.
        :type db: Session
        :return: The updated contact, or None if it does not exist.
        :rtype: Contact | None
        """
    contact = db.query(Contact).filter(Contact.user_id == current_user.id).filter(Contact.id == contact_id).first()
    if contact:
        contact.name = body.name
        contact.surname = body.surname
        contact.email = body.email
        contact.phone = body.phone
        contact.description = contact.description
        db.commit()
    return contact


async def remove_contact(contact_id: int, db: Session, current_user) -> Contact | None:
    """
        Removes a single contact with the specified ID for a specific user.

        :param contact_id: The ID of the contact to remove.
        :type contact_id: int
        :param current_user: The user to remove the contact for.
        :type current_user: User
        :param db: The database session.
        :type db: Session
        :return: The removed contact, or None if it does not exist.
        :rtype: Contact | None
        """
    contact = db.query(Contact).filter(Contact.user_id == current_user.id).filter(Contact.id == contact_id).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact
