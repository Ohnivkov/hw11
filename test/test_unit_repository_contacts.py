import os
import sys

sys.path.append(os.path.abspath('..'))

import collections

collections.Callable = collections.abc.Callable
import unittest
from unittest.mock import MagicMock

from sqlalchemy.orm import Session
from datetime import datetime
from src.database.models import Contact, User
from src.schemas import ContactModel
from src.repository.contacts import (
    get_contacts,
    get_contact,
    create_contacts,
    update_contact,
    remove_contact,
    get_birthdays,
    get_contact_by_email,
    get_contact_by_surname,
    get_contact_by_name
)


class TestContact(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = User(id=1, username='test_user', password="qwerty", confirmed=True)

    async def test_get_contacts(self):
        contacts = [Contact(), Contact(), Contact()]
        mocked_contacts = MagicMock()
        mocked_contacts.all.return_value = contacts
        self.session.query.return_value.filter.return_value.limit.return_value.offset.return_value = mocked_contacts
        result = await get_contacts(10, 0, self.session, self.user)
        self.assertEqual(result, contacts)

    async def test_get_contact_found(self):
        contacts_id = 1
        contact = Contact(id=contacts_id, user_id=self.user.id)

        self.session.query.return_value.filter.return_value.filter.return_value.first.return_value = contact

        result = await get_contact(contacts_id, self.session, self.user)
        self.assertEqual(result, contact)

    async def test_get_contact_not_found(self):
        contacts_id = 1
        self.session.query.return_value.filter.return_value.filter.return_value.first.return_value = None
        result = await get_contact(contacts_id, self.session, self.user)
        self.assertIsNone(result)

    async def test_create_contact(self):
        body = ContactModel(name="test", surname='test1', email='test@gmail.com', description="test note",
                            phone='0970909090', birth_date=datetime(year=2024, day=2, month=3).date(),
                            created_at=datetime.now(), updated_at=datetime.now())
        result = await create_contacts(body, self.session, self.user)
        self.assertEqual(result.name, body.name)
        self.assertEqual(result.surname, body.surname)
        self.assertEqual(result.description, body.description)
        self.assertEqual(result.email, body.email)

        self.assertTrue(hasattr(result, "id"))

    async def test_update_contact(self):
        body = ContactModel(name="test", surname='test1', email='test@gmail.com', description="test note",
                            phone='0970909090', birth_date=datetime(year=2024, day=2, month=3).date(),
                            created_at=datetime.now(), updated_at=datetime.now())
        self.session.query.return_value.filter.return_value.filter.return_value.first.return_value = Contact(
            name="test", surname='test1', email='test@gmail.com', description="test note",
            phone='0970909090', birth_date=datetime(year=2024, day=2, month=3).date(), created_at=datetime.now(),
            updated_at=datetime.now())
        result = await update_contact(1, body, self.session, self.user)
        self.assertIsInstance(result, Contact)
        self.assertEqual(result.name, body.name)
        self.assertEqual(result.description, body.description)

    async def test_delete_contact(self):
        self.session.query.return_value.filter.return_value.filter.return_value.first.return_value = Contact(
            name="test", surname='test1', email='test@gmail.com',
            description="test note",
            phone='0970909090',
            birth_date=datetime(year=2024, day=2, month=3).date(),
            created_at=datetime.now(), updated_at=datetime.now())
        result = await remove_contact(1, self.session, self.user)
        self.session.delete.assert_called_once()
        self.session.commit.assert_called_once()

        self.assertIsInstance(result, Contact)

    async def test_get_birthdays(self):
        contacts = [Contact(name="test", surname='test1', email='test@gmail.com',
                            description="test note",
                            phone='0970909090',
                            birth_date=datetime.now(),
                            created_at=datetime.now(), updated_at=datetime.now()),
                    Contact(name="test111", surname='test22221', email='test2312@gmail.com',
                            description="test note",
                            phone='0970909090',
                            birth_date=datetime.now(),
                            created_at=datetime.now(), updated_at=datetime.now())]
        mocked_contacts = MagicMock()
        mocked_contacts.all.return_value = contacts
        self.session.query.return_value.filter.return_value.filter.return_value.all.return_value = contacts
        result = await get_birthdays(self.session, self.user)
        self.assertEqual(result, contacts)

    async def test_get_contact_by_email(self):
        contacts_email = 'vasya@gmail.com'
        contact = Contact(email=contacts_email, user_id=self.user.id)

        self.session.query.return_value.filter.return_value.filter.return_value.first.return_value = contact

        result = await get_contact_by_email(contacts_email, self.session, self.user)
        self.assertEqual(result, contact)

    async def test_get_contact_by_surname(self):
        contact_surname = 'Nechuporyk'
        contact = Contact(surname=contact_surname, user_id=self.user.id)
        self.session.query.return_value.filter.return_value.filter.return_value.first.return_value = contact

        result = await get_contact_by_surname(contact_surname, self.session, self.user)
        self.assertEqual(result, contact)

    async def test_get_contact_by_name(self):
        contact_name = 'Vladyslav'
        contact = Contact(surname=contact_name, user_id=self.user.id)
        self.session.query.return_value.filter.return_value.filter.return_value.first.return_value = contact

        result = await get_contact_by_name(contact_name, self.session, self.user)
        self.assertEqual(result, contact)


if __name__ == '__main__':
    unittest.main()
