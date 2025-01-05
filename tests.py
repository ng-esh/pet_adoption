from unittest import TestCase
from app import app, db, Pet


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///test_agency'
app.config['TESTING'] = True
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

# you have to disable the CSRF token inorder to be able to send a POST request to our routes
app.config['WTF_CSRF_ENABLED'] = False


class AddPetTestCase(TestCase):
    def setUp(self):
        """Set up test environment: create tables."""
        with app.app_context():
            db.create_all()

    def tearDown(self):
        """Clean up test environment: drop tables."""
        with app.app_context():
            db.session.remove()
            db.drop_all()
    

    def test_add_pet_form(self):
        with app.test_client() as client:
            resp = client.get('/add')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<form id="add-pet-form"', html)

    def test_add_pet(self):
        with app.test_client() as client:
            d = { 'name':'Test', 'species': "cat"}
            resp = client.post('/add', data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Successfully added Test, the cat!', html)