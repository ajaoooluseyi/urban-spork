import unittest
from flask import Flask
from flask_testing import TestCase
from api.app import app, db, Word


class AppTestCase(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_get_word(self):
        # Add a sample word to the database for testing
        word = Word(word="Test")
        db.session.add(word)
        db.session.commit()

        # Make a GET request to the '/' route
        response = self.client.get('/get-word')

        # Assert that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Assert that the response contains the expected word value
        self.assertEqual(response.json, {'word': 'Test'})

    def test_admin_post(self):
        # Make a POST request to the '/admin' route with a new word
        response = self.client.post('/admin', data={'word': 'New Word'})

        # Assert that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Assert that the word is updated in the database
        word = Word.query.first()
        self.assertEqual(word.word, 'New Word')

if __name__ == '__main__':
    unittest.main()
