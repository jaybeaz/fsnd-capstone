import os
import unittest
import json
from app import create_app
from models import setup_db, Actors, Movies, db

# NOTE: These are test tokens with 24-hour expiration.
# In production, tokens would be stored in environment variables.
# Generate fresh tokens before running tests using generate_tokens.py

ASSISTANT_TOKEN="eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImhadjdxRUIzcGRMeTd2MU9qNXhCYyJ9.eyJpc3MiOiJodHRwczovL2Rldi0yY2hiOGJ3MHpkaDF6MXVtLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2OGZkMzZkZWE0MDc3Mzg0N2M2MDE4YWIiLCJhdWQiOlsiZnNuZC1jYXN0aW5nLWFnZW5jeS1jYXBzdG9uZSIsImh0dHBzOi8vZGV2LTJjaGI4YncwemRoMXoxdW0udXMuYXV0aDAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTc2MTYyMTYxMiwiZXhwIjoxNzYyMjI2NDEyLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwiZ3R5IjoicGFzc3dvcmQiLCJhenAiOiJUZmRZejlVVmc2TDFZRVVPRUlkVmZrRzdKNUR3Mlg2OSIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIl19.aHFyOcFnmWVIM1b2kD2AzOR7AOKPHL2EB6pk0l1wu1NgTKQaWlxwEFaENM2xN6OxjEYpK8tn_Mn6SnSjjfLsqd2w83j-G4nv6mcZ5cfcaXQvx-HQ-PE2w9OBBahUSPIOvURb6FjjHUcc5vYZU0bSkQWwXzeLP9ZDAdqcprFPD6wJec4Ud_rmT6w4OX71m2tXPfUiTpi2HDvKj2l5jLLQbkM_BFpZ6SUKhlsHEEb1NTRdgOSWYvBUdq0oqtDmKdLvD_7SlNgJnPeJF07FsAJocv0llh13EOUrBxZsBGe3mX1QZHXs8sGckAmR8TxkQBAIkeOgyTBIvoisHBRr4oPmXQ"
DIRECTOR_TOKEN="eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImhadjdxRUIzcGRMeTd2MU9qNXhCYyJ9.eyJpc3MiOiJodHRwczovL2Rldi0yY2hiOGJ3MHpkaDF6MXVtLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2OGZkM2EwYTg4NTA5NTNjYmU1MGE3NGYiLCJhdWQiOlsiZnNuZC1jYXN0aW5nLWFnZW5jeS1jYXBzdG9uZSIsImh0dHBzOi8vZGV2LTJjaGI4YncwemRoMXoxdW0udXMuYXV0aDAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTc2MTYyMTYxMywiZXhwIjoxNzYyMjI2NDEzLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwiZ3R5IjoicGFzc3dvcmQiLCJhenAiOiJUZmRZejlVVmc2TDFZRVVPRUlkVmZrRzdKNUR3Mlg2OSIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIl19.vgSyIC6tdv6Tfm5rl0qdXM9TUzDDOS5ihw15CoLM3CXBSakwln9Pdzoh8cVA5-cUoKRTvzuO9a1Ah1Q_wIoFOeNLPSOad8tM0Lg82clvpTYileyglV3jg-nPBR9wahT4NwNYmlsO9P2TlbHSpXRwtwHkPtAcRqs8wrPYbCZYaoYeifG0olEvpKVQh-MlAnLZZodKh0pXlolIcNnnATuZZLn03RMAoLvF5cUP29xdgyvb-XOKmfniV0mbzu6uFBt91jig_PVaFKca93eJzHfX0IQcJeh8wLqn-CPxUkDbst1pjKHVdR3xCz_w_cjk2GlYOdcLQ-rbaraU26GfNNlUTg"
EXECUTIVE_TOKEN="eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImhadjdxRUIzcGRMeTd2MU9qNXhCYyJ9.eyJpc3MiOiJodHRwczovL2Rldi0yY2hiOGJ3MHpkaDF6MXVtLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2OGZkM2E2YmM3OTQwY2U2MjUyZWMwZmYiLCJhdWQiOlsiZnNuZC1jYXN0aW5nLWFnZW5jeS1jYXBzdG9uZSIsImh0dHBzOi8vZGV2LTJjaGI4YncwemRoMXoxdW0udXMuYXV0aDAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTc2MTYyMTYxMywiZXhwIjoxNzYyMjI2NDEzLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwiZ3R5IjoicGFzc3dvcmQiLCJhenAiOiJUZmRZejlVVmc2TDFZRVVPRUlkVmZrRzdKNUR3Mlg2OSIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIl19.EZ_uhQeyeBIKFmKEg9S8v49DS1hR4PTCUQLnPdnMXT-nHrWTc4IFxu6oZkVU5sIlbMfpNtLEjiUnavPndGBPODS-0u5HBqTS2ph4s_4f-CQSYGOGu2sAx0XZ1dEckcS8cR7QL92sEeQjic-QiKitRDGLqYHU6Ee-fCUWgzvGXbonYqKIFfAzkroTBlWT6V5t1FXpgsZWkG4QeYs7eF7LcxK3vMJolqTZ4QaXKFzkuTG8Ct95qQvf8rQz8dFRt_2gUQjtk4OB3MipRfIzFgg73y-IoGLWoHZPwr52Hx2leO1yx70o0tS80dPITWoXX8c5QyXcGMnCtCEBmdCuPPUDwg"

class CastingTestCase(unittest.TestCase):
    """This class represents the Casting Agency test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.database_name = "casting_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        self.app = create_app({
            "SQLALCHEMY_DATABASE_URI": self.database_path,
            "SQLALCHEMY_TRACK_MODIFICATIONS": False,
            "TESTING": True
        })
        
        self.client = self.app.test_client()
        #setup_db(self.app, self.database_path)
        # Bind the app to the current context and create all tables
        with self.app.app_context():
            db.create_all()
            actor = Actors(name="Test Actor1", age=23, gender="Male")
            movie = Movies(title="Test Movie1", release_date="2001-01-01")
            db.session.add_all([actor, movie])
            db.session.commit()

    def tearDown(self):
        """Executed after each test"""
        with self.app.app_context():
            db.session.remove()
            db.engine.execute('DROP TABLE IF EXISTS actors CASCADE')
            db.engine.execute('DROP TABLE IF EXISTS movies CASCADE')
            db.drop_all()

    def auth_header(self, token):
        return {'Authorization': f'Bearer {token}'}

#TEST GET with Auth
    def test_get_actors(self):
        """TEST GET method for /actors endpoint"""
        res = self.client.get('/actors', headers=self.auth_header(ASSISTANT_TOKEN))
        print(f"Status: {res.status_code}")
        print(f"Data: {res.data}")  # See what's actually returned
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_actors'])
        self.assertTrue(len(data['actors']))

    def test_get_movies(self):
        """TEST GET method for /movies endpoint"""
        res = self.client.get('/movies', headers=self.auth_header(ASSISTANT_TOKEN))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_movies'])
        self.assertTrue(len(data['movies']))

#TEST GET with no auth
    def test_get_actors_no_auth(self):
        """TEST GET method for /actors endpoint"""
        res = self.client.get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_get_movies_no_auth(self):
        """TEST GET method for /movies endpoint"""
        res = self.client.get('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

#Test POST with auth
    def test_post_actor_auth(self):
        """Test POST method to create new actor"""
        new_actor = {
            "name": "Test Actor 2",
            "age": 41,
            "gender": "Female"
        }
        res = self.client.post('/actors', headers=self.auth_header(EXECUTIVE_TOKEN), json=new_actor)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    def test_post_movie_auth(self):
        """Test POST method to create new actor"""
        new_movie = {
            "title": "Test Movie 2",
            "release_date": "2026-01-01"
        }
        res = self.client.post('/movies', headers=self.auth_header(EXECUTIVE_TOKEN), json=new_movie)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

#Test POST with no auth

    def test_post_actor_no_auth(self):
        """Test POST method to create new actor"""
        new_actor = {
            "name": "Test Actor 2",
            "age": 41,
            "gender": "Female"
        }
        res = self.client.post('/actors', json=new_actor)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])

    def test_post_movie_auth(self):
        """Test POST method to create new actor"""
        new_movie = {
            "title": "Test Movie 2",
            "release_date": "2026-01-01"
        }
        res = self.client.post('/movies', json=new_movie)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])


#Test DELETEs with auth
    def test_delete_actor_auth(self):
        """TEST DELETE for /actors/id endpoint with Director role - has permissions"""
        with self.app.app_context():
            actor = Actors.query.first()
            actor_id = actor.id

        res = self.client.delete(f'/actors/{actor_id}', headers=self.auth_header(DIRECTOR_TOKEN))
        data = json.loads(res.data)
        with self.app.app_context():
            deleted_actor = Actors.query.filter(Actors.id == actor_id).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], actor_id)
        self.assertEqual(deleted_actor, None)

    def test_delete_movie_auth(self):
        """TEST DELETE for /movies/id endpoint"""
        with self.app.app_context():
            movie = Movies.query.first()
            movie_id = movie.id

        res = self.client.delete(f'/movies/{movie_id}', headers=self.auth_header(EXECUTIVE_TOKEN))
        data = json.loads(res.data)
        with self.app.app_context():
            deleted_movie = Movies.query.filter(Movies.id == movie_id).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], movie_id)
        self.assertEqual(deleted_movie, None)


#Test DELETEs with no auth
    def test_delete_actor_no_auth(self):
        """TEST DELETE for /actors/id endpoint with Assistant role - no actor delete permissions"""
        with self.app.app_context():
            actor = Actors.query.first()
            actor_id = actor.id

        res = self.client.delete(f'/actors/{actor_id}', headers=self.auth_header(ASSISTANT_TOKEN))
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_delete_movie_no_auth(self):
        """TEST DELETE for /movies/id endpoint with Director role - no movie delete permissions"""
        with self.app.app_context():
            movie = Movies.query.first()
            movie_id = movie.id

        res = self.client.delete(f'/movies/{movie_id}', headers=self.auth_header(DIRECTOR_TOKEN))
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

#Test PATCH with auth
    def test_update_movie_auth(self):
        """Test PATCH /movies/<id> with Director role"""
        res = self.client.patch('/movies/1',
                                json={"title": "Updated Movie"},
                                headers=self.auth_header(DIRECTOR_TOKEN))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

#Test PATCH with no auth
      
    def test_update_movie_no_auth(self):
        """Test PATCH /movies/<id> with Assitant role - lacks permissions"""
        res = self.client.patch('/movies/1', 
                                json={"title": "Updated Movie"},
                                headers=self.auth_header(ASSISTANT_TOKEN))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

if __name__ == "__main__":
    unittest.main()
