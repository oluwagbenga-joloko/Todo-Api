import json
import jwt
from ..base import BaseTestCase
from api.models import Todo, User, db, TodoItem
from api.util import generate_token
from datetime import datetime, timedelta



class TodosTestCase(BaseTestCase):

    def setUp(self):
        db.drop_all()
        db.create_all()
    
        self.user_1 = User(
            first_name="existing_first_name",
            last_name="existing_last_name",
            password= "existing_password",
            email="test1@yahoo.com"
        )
        self.user_2 = User(
            first_name="existing_first_name",
            last_name="existing_last_name",
            password= "existin_password",
            email="test2@yahoo.com"
        )
        self.user_1.save()
        self.user_2.save()
        self.token_1 = generate_token(self.user_1)
        self.token_2 = generate_token(self.user_2)
        self.headers_1 = { "Authorization": f"Bearer {self.token_1}"}
        self.headers_2 = { "Authorization": f"Bearer {self.token_2}"}
    
    def test_create_todo_without_authorization_token(self):
        """
        test creation of todos without authorization token
        """

        todo = {"title": "test"}
        response = self.client.post('/api/todos', json=todo)
        json_data = response.get_json()
        self.assertStatus(response, 400)
        self.assertEqual(json_data["message"], "no authorization token provided")

    def test_create_todo_with_authorization_token_without_berear_prefix(self):
        """
        test creation of todos with authorization token_without bearer prefix
        """

        todo = {"title": "test"}
        response = self.client.post('/api/todos', json=todo, headers={"Authorization": self.token_1})
        json_data = response.get_json()
        self.assertStatus(response, 400)
        self.assertEqual(json_data["message"], "invalid Authorization header, authorization header should begin with Bearer")

    def test_create_todo_with_invalid_authorization_token(self):
        """
        test creation of todos without authorization token
        """

        todo = {"title": "test"}
        response = self.client.post('/api/todos', json=todo, headers={"Authorization": f"Bearer token"})
        json_data = response.get_json()
        self.assertStatus(response, 401)
        self.assertEqual(json_data["message"], "authoriation token is invalid")

    def test_create_todo_with_expired_authorization_token(self):
        """
        test creation of todos with expired authorization token
        """
        token = jwt.encode({"user": {"id": 1, "email": 'test@gmail.com' },
                            "exp": datetime.utcnow() - timedelta(hours=1)},
                            self.app.config.get("SECRET_KEY"), algorithm='HS256').decode()

        todo = {"title": "test"}
        response = self.client.post('/api/todos', json=todo, headers={"Authorization": f"Bearer {token}"})
        json_data = response.get_json()
        self.assertStatus(response, 401)
        self.assertEqual(json_data["message"], "authorization token has expired")


    def test_creating_todos_succesfully(self):
        """
        tests succesfull creation of todo 
        """
        todo = {"title": "test"}
        response = self.client.post('/api/todos', json=todo, headers=self.headers_1)
        json_data = response.get_json()
        self.assertStatus(response, 201)
        self.assertEqual(json_data["todo"]["title"], todo["title"])
        self.assertEqual(json_data["message"], "todo created")

    def test_creating_todos_with_empty_title(self):
        """
        tests creating todo with empty title
        """
        todo = {"title": ""}
        response = self.client.post('/api/todos', json=todo, headers=self.headers_1)
        json_data = response.get_json()
        self.assertStatus(response, 422)
        self.assertEqual(json_data["message"], "validation failed")
    

    def test_fetch_all_todos(self):
        """
        test getting all todos
        """
        todo_1 = Todo(title="test", user_id=self.user_1.id)
        todo_2 = Todo(title="test2", user_id=self.user_2.id)
        todo_1.save()
        todo_2.save()
        response = self.client.get('/api/todos', headers=self.headers_1)
        json_data = response.get_json()
        self.assert200(response)
        self.assertEqual(json_data["message"], "todos retrieved")
        self.assertEqual(len(json_data["todos"]), 1)

    def test_fetch_single_todo_successfully(self):
        """
        tests getting single todo successfully
        """
        todo_1 = Todo(title="test", user_id=self.user_1.id)
        todo_2 = Todo(title="test2", user_id=self.user_1.id)
        todo_1.save()
        todo_2.save()

        response = self.client.get(f'api/todos/{todo_1.id}', headers=self.headers_1)
        json_data = response.get_json()
        self.assert200(response)
        self.assertEqual(json_data["message"], "todo retrieved")
        self.assertEqual(json_data["todo"]["title"], todo_1.title)
        self.assertEqual(len(json_data["todo"]["todo_items"]), 0)
    
    def test_fetch_single_todo_successfully_includes_todo_items(self):
        """
        tests getting single todos includes todo items
        """
        todo_1 = Todo(title="test", user_id=self.user_1.id)
        todo_2 = Todo(title="test2", user_id=self.user_1.id)
        todo_item_1 = TodoItem(content="testing")
        todo_1.todo_items.append(todo_item_1)
        todo_1.save()
        todo_2.save()

        response = self.client.get(f'api/todos/{todo_1.id}', headers=self.headers_1)
        json_data = response.get_json()
        self.assert200(response)
        self.assertEqual(json_data["message"], "todo retrieved")
        self.assertEqual(json_data["todo"]["title"], todo_1.title)
        self.assertEqual(len(json_data["todo"]["todo_items"]), 1)
    
    def test_fetch_no_existent_todo(self):
        """
        tests getting single todo successfully
        """
        todo_1 = Todo(title="test", user_id=self.user_1.id)
        todo_2 = Todo(title="test2", user_id=self.user_1.id)
        todo_1.save()
        todo_2.save()

        response = self.client.get(f'api/todos/1000000', headers=self.headers_1)
        json_data = response.get_json()
        self.assert404(response)
        self.assertEqual(json_data["message"], "todo does not exist")

    
    def test_fetch_single_todo_not_created_by_user(self):
        """
        tests getting single todo not created by user
        """
        todo_1 = Todo(title="test", user_id=self.user_1.id)
        todo_2 = Todo(title="test2", user_id=self.user_1.id)
        todo_1.save()
        todo_2.save()

        response = self.client.get(f'api/todos/{todo_1.id}', headers=self.headers_2)
        json_data = response.get_json()
        self.assert401(response)
        self.assertEqual(json_data["message"], "unauthorized")
    
    def test_delete_single_todos_successfully(self):
        """
        tests deletion of single todo successfully
        """
        todo_1 = Todo(title="test", user_id=self.user_1.id)
        todo_2 = Todo(title="test2", user_id=self.user_1.id)
        todo_1.save()
        todo_2.save()

        response = self.client.delete(f'api/todos/{todo_1.id}', headers=self.headers_1)
        json_data = response.get_json()
        self.assert200(response)
        self.assertEqual(json_data["message"], "todo deleted")
    
    def test_delete_non_existent_single_todo(self):
        """
        tests deletion of single of non existent todo
        """
        todo_1 = Todo(title="test", user_id=self.user_1.id)
        todo_2 = Todo(title="test2", user_id=self.user_1.id)
        todo_1.save()
        todo_2.save()

        response = self.client.delete('api/todos/1000000', headers=self.headers_1)
        json_data = response.get_json()
        self.assert404(response)
        self.assertEqual(json_data["message"], "todo does not exist")
      

    def test_delete_single_todos_not_created_by_user(self):
        """
        tests deletion of single todo successfully
        """
        todo_1 = Todo(title="test", user_id=self.user_1.id)
        todo_2 = Todo(title="test2", user_id=self.user_1.id)
        todo_1.save()
        todo_2.save()

        response = self.client.delete(f'api/todos/{todo_1.id}', headers=self.headers_2)
        json_data = response.get_json()
        self.assert401(response)
        self.assertEqual(json_data["message"], "unauthorized")
       
    
    def test_update_single_todos_succesfully(self):
        """
        tests deletion of single todo
        """
        todo_1 = Todo(title="test", user_id=self.user_1.id)
        todo_2 = Todo(title="test2", user_id=self.user_1.id)
        todo_1.save()
        todo_2.save()

        todo_update = {"title": "new title"}
        response = self.client.put(f'api/todos/{todo_1.id}', json=todo_update, headers=self.headers_1)
        json_data = response.get_json()
        self.assert200(response)
        self.assertEqual(json_data["message"], "todo updated")
        self.assertEqual(json_data["todo"]["title"], todo_update["title"])
    

