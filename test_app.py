import unittest
from fastapi.testclient import TestClient
from src.main import app
import os
import sys

lst = os.listdir("src")
for folder in lst:
    my_lib_path = os.path.abspath(os.path.join("src", folder))
    sys.path.append(my_lib_path)


class MyTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.client = TestClient(app)

    def test_read_main(self):
        response = self.client.get('/')
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.text, 'Welcome to Short URL Service (SUS)')

    def test_ping_db(self):
        response = self.client.get('/ping_db')
        self.assertTrue(response)

    def test_create_item(self):
        response = self.client.post("/", json={"full_url": "https://www.youtube.com/"})
        self.assertEquals(response.status_code, 201)


if __name__ == "__main__":
    unittest.main()
