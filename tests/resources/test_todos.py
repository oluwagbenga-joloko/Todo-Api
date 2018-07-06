import json
from ..base import BaseTestCase


class TodosTestCase(BaseTestCase):

    def test_creating_todos_succesfully(self):
        todo = {"title": "2"}
        response = self.client.post('/api/todos', json=todo)
        json_data = response.get_json()
        self.assertStatus(response, 201)
        self.assertEqual(json_data["todo"]["title"], todo["title"])
        self.assertEqual(json_data["message"], "todo created")

