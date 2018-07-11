from api.models import User
from ..base import BaseTestCase


class UsersTestCase(BaseTestCase):

    def test__succesful_creation_of_users(self):
        """
        tess succesful creation of users
        """
        user = { 
            "first_name": "test_first_name",
            "last_name": "test_last_name",
            "email":"test@test.com",
            "password": "testpassword"
        }
        response = self.client.post('/api/users', json=user)
        json_data = response.get_json()
        self.assertStatus(response, 201)
        self.assertEqual(json_data["message"], "user created")
        self.assertIn("token",json_data )
    
    def test_creation_of_invalid_email_user(self):
        """
        tess succesful creation of users with invalid email
        """
        user = { 
            "first_name": "test_first_name",
            "last_name": "test_last_name",
            "email":"test",
            "password": "testpassword"
        }
        response = self.client.post('/api/users', json=user)
        json_data = response.get_json()
        self.assertEqual(json_data["errors"]["email"][0], "Not a valid email address.")
        self.assertNotIn("token",json_data )
        self.assertStatus(response, 422)
    
    def test_creation_of_invalid_password_user(self):
        """
        tess succesful creation of users with invalid email
        """
        user = { 
            "first_name": "test_first_name",
            "last_name": "test_last_name",
            "email":"test@yahoo.com",
            "password": ""
        }
        response = self.client.post('/api/users', json=user)
        json_data = response.get_json()
        self.assertStatus(response, 422)
        self.assertNotIn("token",json_data )
        self.assertEqual(json_data["errors"]["password"][0], "Data not provided.")
    

    def test_creation_of_user_with_existing_email(self):
        """
        tess creation of user with existing email
        """

        existing_user = User(
            first_name="existing_first_name",
            last_name="existing_last_name",
            password= "existing_password",
            email="test@yahoo.com"
        )
        existing_user.save()
        user = { 
            "first_name": "test_first_name",
            "last_name": "test_last_name",
            "email":"test@yahoo.com",
            "password": "test_password"
        }
        response = self.client.post('/api/users', json=user)
        json_data = response.get_json()
        self.assertStatus(response, 400)
        self.assertEqual(json_data["message"], "user with email already exists")
        self.assertNotIn("token", json_data)
    

    def test_user_login_without_email_and_password(self):
        """
        test user login without email or password
        """

        existing_user = User(
            first_name="existing_first_name",
            last_name="existing_last_name",
            password= "existing_password",
            email="test@yahoo.com"
        )
        existing_user.save()
        user_login_details = { 
            "email":"",
            "password":""
        }
        response = self.client.post('/api/users/login', json=user_login_details)
        json_data = response.get_json()
        self.assertStatus(response, 422)
        self.assertEqual(json_data["errors"]["password"][0], "Data not provided.")
        self.assertEqual(json_data["errors"]["email"][0],  "Not a valid email address.")
        self.assertEqual(json_data["message"], "validation failed")
        self.assertNotIn("token", json_data)
    

    def test_user_login_with_wrong_email(self):
        """
        test user login with wrong email
        """

        existing_user = User(
            first_name="existing_first_name",
            last_name="existing_last_name",
            password= "existing_password",
            email="test@yahoo.com"
        )
        existing_user.save()
        user_login_details = { 
            "email": "test2@yahoo.com",
            "password": "existing_password"
        }
        response = self.client.post('/api/users/login', json=user_login_details)
        json_data = response.get_json()
        self.assertStatus(response, 401)
        self.assertEqual(json_data["message"], "invalid email or password")
        self.assertNotIn("token", json_data)
    
    def test_user_login_with_wrong_password(self):
        """
        test user login with wrong password
        """

        existing_user = User(
            first_name="existing_first_name",
            last_name="existing_last_name",
            password= "existing_password",
            email="test@yahoo.com"
        )
        existing_user.save()
        user_login_details = { 
            "email": "test2@yahoo.com",
            "password": "existin_password"
        }
        response = self.client.post('/api/users/login', json=user_login_details)
        json_data = response.get_json()
        self.assertStatus(response, 401)
        self.assertEqual(json_data["message"], "invalid email or password")
        self.assertNotIn("token", json_data)
    
    def test_user_login_with_correct_email_and_password(self):
        """
        test user login with correct email and password
        """

        existing_user = User(
            first_name="existing_first_name",
            last_name="existing_last_name",
            password= "existing_password",
            email="test@yahoo.com"
        )
        existing_user.save()
        user_login_details = { 
            "email": "test@yahoo.com",
            "password": "existing_password"
        }
        response = self.client.post('/api/users/login', json=user_login_details)
        json_data = response.get_json()
        self.assertStatus(response, 200)
        self.assertEqual(json_data["message"], "log in successfull")
        self.assertIn("token", json_data)
    




