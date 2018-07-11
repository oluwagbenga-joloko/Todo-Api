import json
from ..base import BaseTestCase
from api.models import Todo


class TodosTestCase(BaseTestCase):

    def test_creating_todos_succesfully(self):
        """
        tests succesfull creation of todo 
        """
        todo = {"title": "test"}
        response = self.client.post('/api/todos', json=todo)
        json_data = response.get_json()
        self.assertStatus(response, 201)
        self.assertEqual(json_data["todo"]["title"], todo["title"])
        self.assertEqual(json_data["message"], "todo created")

    def test_creating_todos_with_empty_title(self):
        """
        tests creating todo with empty title
        """
        todo = {"title": ""}
        response = self.client.post('/api/todos', json=todo)
        self.assertStatus(response, 400)
    

    def test_fetch_all_todos(self):
        """
        test getting all todos
        """
        todo_1 = Todo(title="test")
        todo_2 = Todo(title="test2")
        todo_1.save()
        todo_2.save()
        response = self.client.get('/api/todos')
        json_data = response.get_json()
        self.assert200(response)
        self.assertEqual(json_data["message"], "todos retrieved")
        self.assertEqual(len(json_data["todos"]), 2)

    def test_fetch_single_todos(self):
        """
        tests getting single todo
        """
        todo_1 = Todo(title="test")
        todo_2 = Todo(title="test2")
        todo_1.save()
        todo_2.save()

        response = self.client.get(f'api/todos/{todo_1.id}')
        json_data = response.get_json()
        self.assert200(response)
        self.assertEqual(json_data["message"], "todo retrieved")
        self.assertEqual(json_data["todo"]["title"], todo_1.title)
    
    def test_delete_single_todos(self):
        """
        tests deletion of single todo
        """
        todo_1 = Todo(title="test")
        todo_2 = Todo(title="test2")
        todo_1.save()
        todo_2.save()

        response = self.client.delete(f'api/todos/{todo_1.id}')
        json_data = response.get_json()
        self.assert200(response)
        self.assertEqual(json_data["message"], "todo deleted")
    

    def test_update_single_todos(self):
        """
        tests deletion of single todo
        """
        todo_1 = Todo(title="test")
        todo_2 = Todo(title="test2")
        todo_1.save()
        todo_2.save()

        todo_update = {"title": "new title"}
        response = self.client.put(f'api/todos/{todo_1.id}', json=todo_update)
        json_data = response.get_json()
        self.assert200(response)
        self.assertEqual(json_data["message"], "todo updated")
        self.assertEqual(json_data["todo"]["title"], todo_update["title"]) 

