import unittest
import json
import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from app import app


class TaskAPITestCase(unittest.TestCase):

    def setUp(self):
        '''Set up test client'''
        self.app = app.test_client()
        self.app.testing = True

    def test_home_endpoint(self):
        '''Test home page endpoint'''
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Task Management API', response.data)

    def test_get_tasks(self):
        '''Test getting tasks list'''
        response = self.app.get('/tasks')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('tasks', data)
        self.assertIn('count', data)

    def test_create_task_valid(self):
        '''Test creating task with valid data'''
        task_data = {"title": "New Test Task", "completed": False}
        response = self.app.post('/tasks',
                                 data=json.dumps(task_data),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn('task', data)
        self.assertEqual(data['task']['title'], "New Test Task")

    def test_create_task_missing_title(self):
        '''Test creating task with missing title'''
        task_data = {"completed": False}
        response = self.app.post('/tasks',
                                 data=json.dumps(task_data),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)

    def test_health_check(self):
        '''Test health check endpoint'''
        response = self.app.get('/health')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'healthy')

    def test_create_task_wrong_status_WILL_FAIL(self):
        '''Test that will fail - expecting wrong status code'''
        task_data = {"title": "Test Task", "completed": False}
        response = self.app.post('/tasks',
                                 data=json.dumps(task_data),
                                 content_type='application/json')
        # INTENTIONAL FAILURE - expecting 200 but should be 201
        self.assertEqual(response.status_code, 200)

    def test_health_wrong_format_WILL_FAIL(self):
        '''Test that will fail - expecting wrong response format'''
        response = self.app.get('/health')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        # INTENTIONAL FAILURE - expecting wrong field name
        self.assertIn('health_status', data)  # Should be 'status'

    def test_get_tasks_wrong_structure_WILL_FAIL(self):
        '''Test that will fail - expecting wrong response structure'''
        response = self.app.get('/tasks')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        # INTENTIONAL FAILURE - expecting wrong field name
        self.assertIn('task_list', data)  # Should be 'tasks'


if __name__ == '__main__':
    unittest.main()
