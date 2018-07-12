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
        self.todo_1 = Todo(
            title="firt todo"
        )
        self.todo_2 = Todo(
            title="second todo"
        )
        self.user_1.todos.append(self.todo_1)
        self.user_2.todos.append(self.todo_2)
        self.user_1.save()
        self.user_2.save()
        self.token_1 = generate_token(self.user_1)
        self.token_2 = generate_token(self.user_2)
        self.headers_1 = { "Authorization": f"Bearer {self.token_1}"}
        self.headers_2 = { "Authorization": f"Bearer {self.token_2}"}

    def test_creating_todo_item_succesfully(self):
        """
        tests succesfull creation of todo item
        """
        todo_item = {"content": "cut the onions"}
        response = self.client.post(f'/api/todos/{self.todo_1.id}/todo_items', json=todo_item, headers=self.headers_1)
        json_data = response.get_json()
        self.assertStatus(response, 201)
        self.assertEqual(json_data["todo_item"]["content"], todo_item["content"])
        self.assertEqual(json_data["message"], "todo item created")
    
    def test_creating_todo_item_for_non_existent_todo(self):
        """
        tests creating todo item for non existent todo
        """
        todo_item = {"content": "cut the onions"}
        response = self.client.post('/api/todos/190000099/todo_items', json=todo_item, headers=self.headers_1)
        json_data = response.get_json()
        self.assertStatus(response, 404)
        self.assertEqual(json_data["message"], "todo does not exist")
    
    def test_creating_todo_item_with_empty_content(self):
        """
        tests creating todo item with empty content
        """
        todo_item = {"content": ""}
        response = self.client.post(f'/api/todos/{self.todo_1.id}/todo_items', json=todo_item, headers=self.headers_1)
        json_data = response.get_json()
        self.assertStatus(response, 422)
        self.assertEqual(json_data["message"], "validation failed")
        self.assertEqual(json_data["errors"]["content"][0], "Data not provided.")
    
    def test_successfull_deletion_of_todo_item(self):
        """
        tests deletion of single todo succesfully
        """

        todo_item_1 = TodoItem(content="test content 1", todo_id=self.todo_1.id) 
        todo_item_1.save()

        todo_item_2 = TodoItem(content="test content 2", todo_id=self.todo_2.id) 
        todo_item_2.save()

        response = self.client.delete(f'/api/todos/{self.todo_1.id}/todo_items/{todo_item_1.id}', headers=self.headers_1)
        json_data = response.get_json()
        self.assertStatus(response, 200)
        self.assertEqual(json_data["message"], "todo item deleted")
    
    def test_deletion_of_todo_item_with_non_existent_todo_id_in_url(self):
        """
        tests deletion of todo todo item with no existent todo_id in url
        """

        todo_item_1 = TodoItem(content="test content 1", todo_id=self.todo_1.id) 
        todo_item_1.save()

        todo_item_2 = TodoItem(content="test content 2", todo_id=self.todo_2.id) 
        todo_item_2.save()

        response = self.client.delete(f'/api/todos/999999999/todo_items/{todo_item_1.id}', headers=self.headers_1)
        json_data = response.get_json()
        self.assertStatus(response, 404)
        self.assertEqual(json_data["message"], "todo does not exist")
    
    def test_deletion_of_todo_item_with_non_existent_todo_item_id_in_url(self):
        """
        tests deletion of todo todo item with no existent todo_item_id in url
        """

        todo_item_1 = TodoItem(content="test content 1", todo_id=self.todo_1.id) 
        todo_item_1.save()

        todo_item_2 = TodoItem(content="test content 2", todo_id=self.todo_2.id) 
        todo_item_2.save()

        response = self.client.delete(f'/api/todos/{self.todo_1.id}/todo_items/99999999', headers=self.headers_1)
        json_data = response.get_json()
        self.assertStatus(response, 404)
        self.assertEqual(json_data["message"], "todo item does not exist")
    
     
    def test_deletion_of_todo_item_not_created_by_user(self):
        """
        tests deletion of todo item not created by user
        """

        todo_item_1 = TodoItem(content="test content 1", todo_id=self.todo_1.id) 
        todo_item_1.save()

        todo_item_2 = TodoItem(content="test content 2", todo_id=self.todo_2.id) 
        todo_item_2.save()

        response = self.client.delete(f'/api/todos/{self.todo_2.id}/todo_items/{todo_item_2.id}', headers=self.headers_1)
        json_data = response.get_json()
        self.assertStatus(response, 401)
        self.assertEqual(json_data["message"], "unauthorized")
    
    def test_updating_of_todo_item_not_created_by_user(self):
        """
        tests update of todo item not created by user
        """

        todo_item_1 = TodoItem(content="test content 1", todo_id=self.todo_1.id) 
        todo_item_1.save()

        todo_item_2 = TodoItem(content="test content 2", todo_id=self.todo_2.id) 
        todo_item_2.save()

        todo_item_update = {
            "complete": True
        }

        response = self.client.put(f'/api/todos/{self.todo_2.id}/todo_items/{todo_item_2.id}', headers=self.headers_1,
                                   json=todo_item_update)
        json_data = response.get_json()
        self.assertStatus(response, 401)
        self.assertEqual(json_data["message"], "unauthorized")

    def test_update_of_todo_item_with_non_existent_todo_id_in_url(self):
        """
        tests update of todo todo item with no existent todo_id in url
        """

        todo_item_1 = TodoItem(content="test content 1", todo_id=self.todo_1.id) 
        todo_item_1.save()

        todo_item_2 = TodoItem(content="test content 2", todo_id=self.todo_2.id) 
        todo_item_2.save()

        todo_item_update = {
            "complete": True
        }

        response = self.client.put(f'/api/todos/999999999/todo_items/{todo_item_1.id}', headers=self.headers_1,
                                      json=todo_item_update)
        json_data = response.get_json()
        self.assertStatus(response, 404)
        self.assertEqual(json_data["message"], "todo does not exist")
    
    def test_update_of_todo_item_with_non_existent_todo_item_id_in_url(self):
        """
        tests update of todo todo item with no existent todo_item_id in url
        """

        todo_item_1 = TodoItem(content="test content 1", todo_id=self.todo_1.id) 
        todo_item_1.save()

        todo_item_2 = TodoItem(content="test content 2", todo_id=self.todo_2.id) 
        todo_item_2.save()

        todo_item_update = {
            "complete": True
        }

        response = self.client.put(f'/api/todos/{self.todo_1.id}/todo_items/99999999', headers=self.headers_1,
                                      json=todo_item_update)
        json_data = response.get_json()
        self.assertStatus(response, 404)
        self.assertEqual(json_data["message"], "todo item does not exist")
    
    def test_update_of_todo_item_successfully(self):
        """
        tests update of todo todo item succesfully
        """

        todo_item_1 = TodoItem(content="test content 1", todo_id=self.todo_1.id) 
        todo_item_1.save()

        todo_item_2 = TodoItem(content="test content 2", todo_id=self.todo_2.id) 
        todo_item_2.save()

        todo_item_update = {
            "complete": True
        }

        response = self.client.put(f'/api/todos/{self.todo_1.id}/todo_items/{todo_item_1.id}', headers=self.headers_1,
                                      json=todo_item_update)
        json_data = response.get_json()
        self.assertStatus(response, 200)
        self.assertEqual(json_data["message"], "todo_item updated")
        self.assertEqual(json_data["todo_item"]["complete"], todo_item_update["complete"])
    
    def test_update_of_todo_item_with_invalid_data(self):
        """
        tests update of todo todo item with invalid data
        """

        todo_item_1 = TodoItem(content="test content 1", todo_id=self.todo_1.id) 
        todo_item_1.save()

        todo_item_2 = TodoItem(content="test content 2", todo_id=self.todo_2.id) 
        todo_item_2.save()

        todo_item_update = {
            "complete": "how"
        }

        response = self.client.put(f'/api/todos/{self.todo_1.id}/todo_items/{todo_item_1.id}', headers=self.headers_1,
                                      json=todo_item_update)
        json_data = response.get_json()
        self.assertStatus(response, 422)
        self.assertEqual(json_data["message"], "validation failed")

