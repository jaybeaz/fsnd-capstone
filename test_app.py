import os
import unittest
import json
from app import create_app
from models import setup_db, Actors, Movies, db

# NOTE: These are test tokens with 24-hour expiration.
# In production, tokens would be stored in environment variables.
# Generate fresh tokens before running tests using generate_tokens.py

ASSISTANT_TOKEN="eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImhadjdxRUIzcGRMeTd2MU9qNXhCYyJ9.eyJpc3MiOiJodHRwczovL2Rldi0yY2hiOGJ3MHpkaDF6MXVtLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2OGZkMzZkZWE0MDc3Mzg0N2M2MDE4YWIiLCJhdWQiOlsiZnNuZC1jYXN0aW5nLWFnZW5jeS1jYXBzdG9uZSIsImh0dHBzOi8vZGV2LTJjaGI4YncwemRoMXoxdW0udXMuYXV0aDAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTc2MTUwMTcxMCwiZXhwIjoxNzYxNTg4MTEwLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwiZ3R5IjoicGFzc3dvcmQiLCJhenAiOiJUZmRZejlVVmc2TDFZRVVPRUlkVmZrRzdKNUR3Mlg2OSIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIl19.a41twXF4DBKOZ1EYR6aB_wUSEUEWCeUNUHOJUEStgBj9cGcEUR9PwMkJ8yj5Iy9GSMQ2V5KLXa10d6YujJMYT9c_O0PVt25x36O6f7_FhGqcXTmOhuwb3h1grtI8IETqH_P1wlUKR-Fna7OiwuDENa0MUhRgXuOn5BsSQ7Ep1xGYRlQFuOKB2gAHZ2Pi85Gf8zuoU6isx4KhKHXh9eukdPI7gEyxdmKsI9ezSdYux9d3rnWt7d3lKcNPgFvhGw-MgeqjdrxhBfszdEej4TNSjiAK69qWVhuPSim_cRdwXQK2QKL9ua8DkzTQOIgG2zJrNdvLYYMWDRyQeJSvBeMSHQ"
DIRECTOR_TOKEN="eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImhadjdxRUIzcGRMeTd2MU9qNXhCYyJ9.eyJpc3MiOiJodHRwczovL2Rldi0yY2hiOGJ3MHpkaDF6MXVtLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2OGZkM2EwYTg4NTA5NTNjYmU1MGE3NGYiLCJhdWQiOlsiZnNuZC1jYXN0aW5nLWFnZW5jeS1jYXBzdG9uZSIsImh0dHBzOi8vZGV2LTJjaGI4YncwemRoMXoxdW0udXMuYXV0aDAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTc2MTUwMTcxMCwiZXhwIjoxNzYxNTg4MTEwLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwiZ3R5IjoicGFzc3dvcmQiLCJhenAiOiJUZmRZejlVVmc2TDFZRVVPRUlkVmZrRzdKNUR3Mlg2OSIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIl19.hjJ5pOs2N7r3s490-iQIXckOYRU6zkwpQa-fZNIwpqKmOKT6F-Osk5oNYP9iqCSEx4171b73HspyQn1q24LqKzY96ap_eQH6_hfA2d3w-Dx4ew8-dTiKUuwpQFM4ZbbC0NU2lK-Br87CyYfJEaTP7_Mi7ZSr-bTmBoyxN3oMQgIoUYoDqGHt1IUoRd78zcQn7-NowcEUITROALVkog0TvcVztdScaaGezA9H-9x147plJDR_t0LxFosZ-YqYC8C6MEagEyhPtrcq_0om9HIK7h8myR1wDYnRwIJO7d5FSzJOpAyV3wwmzPr1Kcw6dxW8BJwipT35-PJiWphig1C9gQ"
EXECUTIVE_TOKEN="eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImhadjdxRUIzcGRMeTd2MU9qNXhCYyJ9.eyJpc3MiOiJodHRwczovL2Rldi0yY2hiOGJ3MHpkaDF6MXVtLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2OGZkM2E2YmM3OTQwY2U2MjUyZWMwZmYiLCJhdWQiOlsiZnNuZC1jYXN0aW5nLWFnZW5jeS1jYXBzdG9uZSIsImh0dHBzOi8vZGV2LTJjaGI4YncwemRoMXoxdW0udXMuYXV0aDAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTc2MTUwMTcxMCwiZXhwIjoxNzYxNTg4MTEwLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwiZ3R5IjoicGFzc3dvcmQiLCJhenAiOiJUZmRZejlVVmc2TDFZRVVPRUlkVmZrRzdKNUR3Mlg2OSIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIl19.APkSCmuJwtvypQ9lApWblraW4zIhcL2EPNkrQ1UbKxDJoIVno6KMwTfpqZmWKF5vvWv3bc_dLD6Ly6OEgpn-awS6hujK8ikpYK8wh1iZFAl0gAHN0fSuUFbqSEsEEnK-4LczohIfwOLBgIwOG_TIY6iCWI8q5xWaUIw6YGtPw4tQ89PkB_FK4v9R4hj4lyNWSTyF7UqXbQHgwt0y2fZQ41Hl-9naygLMVzA9CH_Iz4k4zZ2BCU_5-rwcQuPKmKIeXv9qbpeXyQvx5Vc8voAxOGGatPYj30dEMGf9iVVPB4zZ_oApLAYydCdY3S1RaKorq1wCLy4WJkIRUohzAie97A"

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
            # science = Category(type='Science')
            #art = Category(type='Art')
            #db.session.add_all([science, art])
            #db.session.commit()
            # q1 = Question(question='Test question 1', answer='Test answer 1',
            #                category=art.id, difficulty=1)
            # q2 = Question(question='Test question 2', answer='Test answer 2',
            #                category=science.id, difficulty=2)
            #q1.insert()
            #q2.insert()

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
