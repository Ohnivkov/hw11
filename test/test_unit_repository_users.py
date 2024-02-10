import os
import sys

sys.path.append(os.path.abspath('..'))
import collections
from libgravatar import Gravatar

collections.Callable = collections.abc.Callable
import unittest
from unittest.mock import MagicMock
from src.schemas import UserModel
from sqlalchemy.orm import Session
from src.database.models import User
from src.repository.users import (
    check_exist_user,
    create_new_user,
    token_to_db,
    find_user_by_email,
    confirmed_email,
    update_avatar
)


class TestContact(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = User(id=1, username='test_user', password="qwerty", confirmed=True)

    async def test_check_exist_user(self):
        email = 'vasya@gmail.com'
        user = User(id=1, email=email)
        self.session.query.return_value.filter.return_value.first.return_value = user
        result = await check_exist_user(email, self.session)
        self.assertEqual(result, user)

    async def test_create_new_user(self):
        email = 'vasya@gmail.com'

        avatar = None
        try:
            g = Gravatar(email)
            avatar = g.get_image()
        except Exception as err:
            print(err)
        user = UserModel(id=1, email=email, password='dfsfsfds', username='vlad')
        result = await create_new_user(user, self.session)

        self.assertEqual(result.username, user.username)
        self.assertEqual(result.password, user.password)
        self.assertEqual(result.email, user.email)
        self.assertEqual(result.avatar, avatar)

    async def test_token_to_db(self):
        refresh_token = '12312313'
        user = User(id=1)
        self.session.return_value = user
        result = await token_to_db(user, refresh_token, self.session)
        self.assertEqual(refresh_token, result)

    async def test_find_user_by_email(self):
        user_email = 'vasya@gmail.com'
        user = User(email=user_email)

        self.session.query.return_value.filter.return_value.first.return_value = user

        result = await find_user_by_email(user_email, self.session)
        self.assertEqual(user, result)

    async def test_confirmed_email(self):
        user_email = 'vasya@gmail.com'
        user = User(email=user_email, confirmed=False)
        self.session.query.return_value.filter.return_value.first.return_value = user
        await confirmed_email(user_email, self.session)
        self.assertEqual(user.confirmed, True)

    async def test_update_avatar(self):
        url = 'https://upload.wikimedia.org/wikipedia/commons/thumb/b/b6/Image_created_with_a_mobile_phone.png/1280px-Image_created_with_a_mobile_phone.png'
        user_email = 'vasya@gmail.com'
        user = User(email=user_email, avatar=None)
        self.session.query.return_value.filter.return_value.first.return_value = user
        await update_avatar(user_email, url, self.session)
        self.assertEqual(url, user.avatar)


if __name__ == '__main__':
    unittest.main()
