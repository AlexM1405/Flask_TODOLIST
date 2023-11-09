from flask_testing import TestCase
from flask import current_app, url_for
from main import app, db


class MainTest(TestCase):
    def create_app(self):
        app.config["TESTING"] = True
        app.config["WTF_CSRF_ENABLED"] = False
        
        return app

    def test_homepage(self):
        self.assertIsNotNone(current_app)
    
    def test_app_in_test_mode(self):
        self.assertTrue(current_app.config["TEST"])
    
    def test_index_redirects(self):
        response = self.client.get(url_for("index"))
        self.assertRedirects(response, url_for("hello"))

    def test_hello_get(self):
        response = self.client.get(url_for("hello"))
        self.assertEqual(200, response.status_code)

    def test_hello_post(self): 
        response = self.client.get(url_for("hello"))
        self.assertTrue(response.status_code, 405)

    def test_auth_blueprint_exists(self):
        self.assertIn("auth", self.app.blueprints)

    def test_auth_login_get(self):
        self.client.get(url_for("auth.login"))
    
        self.assertTemplateUsed("login.html")

    def test_auth_login_post(self):
        fake_form = {
            "username": "fake",
            "password": "fake"
        }
        response = self.client.post(url_for("auth.login"), data=fake_form)
        self.assertRedirects(response, url_for("index"))

    def test_app_database_exists(self):
         self.assertIsNotNone(db)

    def test_auth_signup_get(self):
        response = self.client.get(url_for('auth.signup'))

        self.assert200(response)
    

    def test_auth_signup_post(self):
        try:
            fake_form = {
                'username': 'test_user',
                'password': '123456'
            }
            response = self.client.post(url_for('auth.signup'), data=fake_form)
            self.assertRedirects(response, url_for('hello'))
        finally:
            #Remove added db
            db.collection('users').document(fake_form['username']).delete()

    def test_delete_todo_post(self):
        #Login
        self.client.post(url_for('auth.login'), data=self.fake_log_form)
        response = self.client.post(url_for('delete_user_todo', todo_description='fake_todo'))
        self.assertRedirects(response, url_for('hello'))