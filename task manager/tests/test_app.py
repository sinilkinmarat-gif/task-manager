import unittest
import json
import os
from app import load_tasks, save_tasks

DATA_FILE = 'data/tasks.json'

class TestTaskManager(unittest.TestCase):
    def setUp(self):
        if os.path.exists(DATA_FILE):
            os.remove(DATA_FILE)

    def test_load_save_empty(self):
        tasks = load_tasks()
        self.assertEqual(tasks, [])

    def test_save_load(self):
        sample = [{"id": 1234, "title": "Test", "description": "", "priority": 3}]
        save_tasks(sample)
        loaded = load_tasks()
        self.assertEqual(loaded, sample)

    def tearDown(self):
        if os.path.exists(DATA_FILE):
            os.remove(DATA_FILE)

if __name__ == '__main__':
    unittest.main()