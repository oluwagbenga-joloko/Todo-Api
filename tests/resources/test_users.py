from api.models import User, db
from ..base import BaseTestCase
from api.util import generate_token

class UsersTestCase(BaseTestCase):

    def setUp(self):
        db.drop_all()
        db.create_all()
    
        self.user_1_data = dict(
            first_name="existing_first_name",
            last_name="existing_last_name",
            password= "existing_password",
            email="test1@yahoo.com"
        )
        self.user_2_data = dict(
            first_name="existing_first_name",
            last_name="existing_last_name",
            password= "existin_password",
            email="test2@yahoo.com"
        )
        self.user_1 = User(**self.user_1_data)
        self.user_2 = User(**self.user_2_data)

        self.user_1.save()
        self.user_2.save()
        self.token_1 = generate_token(self.user_1)
        self.token_2 = generate_token(self.user_2)
        self.headers_1 = { "Authorization": f"Bearer {self.token_1}"}
        self.headers_2 = { "Authorization": f"Bearer {self.token_2}"}

    def test_succesful_creation_of_users(self):
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

        user_login_details = { 
            "email": "",
            "password": ""
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

        user_login_details = { 
            "email": "tesddfdfdft2@yahoo.com",
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
        user_login_details = { 
            "email": "test2@yahoo.com",
            "password": "existdfdfin_password"
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

        user_login_details = { 
            "email": self.user_1_data["email"],
            "password": self.user_1_data["password"]
        }
        response = self.client.post('/api/users/login', json=user_login_details)
        json_data = response.get_json()
        self.assertStatus(response, 200)
        self.assertEqual(json_data["message"], "log in successfull")
        self.assertIn("token", json_data)
    

    def test_succesful_update_of_user(self):
        """
        tests succesful update of user
        """
        user = { 
            "first_name": "jacob",
            "email":"test2ii@test.com",
        }
        response = self.client.put(f'/api/users/{self.user_1.id}', json=user, headers=self.headers_1)
        json_data = response.get_json()
        self.assertStatus(response, 200)
        self.assertEqual(json_data["message"], "user updated")
        self.assertEqual(json_data["user"]["first_name"], user["first_name"])
        self.assertEqual(json_data["user"]["email"], user["email"])
    
    def test_update_of_non_existent_user(self):
        """
        tests update non existent user
        """
        user = { 
            "first_name": "jacob",
            "email":"test2ii@test.com",
        }
        response = self.client.put(f'/api/users/99999999', json=user, headers=self.headers_1)
        json_data = response.get_json()
        self.assertStatus(response, 404)
        self.assertEqual(json_data["message"], "user does not exist")
    
    def test_update_user_with_token_of_diffrent_user(self):
        """
        tests update user with diffrent user token
        """
        user = { 
            "first_name": "jacob",
            "email":"test2ii@test.com",
        }
        response = self.client.put(f'/api/users/{self.user_1.id}', json=user, headers=self.headers_2)
        json_data = response.get_json()
        self.assertStatus(response, 401)
        self.assertEqual(json_data["message"], "unauthorized")
    
    def test_update_user_with_empty_fields(self):
        """
        test update use with empty first name field
        """
        
        user = { 
            "first_name": "",
            "email":"test2ii@test.com",
        }
        response = self.client.put(f'/api/users/{self.user_1.id}', json=user, headers=self.headers_1)
        json_data = response.get_json()
        self.assertStatus(response, 422)
        self.assertEqual(json_data["message"], "validation failed")
    
    def test_update_of_user_with_email_that_exists(self):
        """
        tests update user with email that exists 
        """
        user = { 
            "first_name": "jacob",
            "email": self.user_2.email,
        }
        response = self.client.put(f'/api/users/{self.user_1.id}', json=user, headers=self.headers_1)
        json_data = response.get_json()
        self.assertStatus(response, 409)
        self.assertEqual(json_data["message"], "user with email already exists")
       
        


        
    




