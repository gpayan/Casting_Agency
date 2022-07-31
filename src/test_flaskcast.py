import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from flaskcast import app
from flaskcast.models import db, Actor, Movie

import os
from dotenv import load_dotenv

load_dotenv()
#DB_PATH = os.getenv('DB_PATH')
JWT_CAST_ASSISTANT = os.getenv('JWT_CAST_ASSISTANT')
JWT_CAST_DIRECTOR = os.getenv('JWT_CAST_DIRECTOR')
JWT_EXEC_PRODUCER = os.getenv('JWT_EXEC_PRODUCER')

DB_PATH = "postgresql://gpayan@localhost:5432/casting_agency_test"
#JWT_CAST_ASSISTANT = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjBRRmt5TjFCaFN4NzhoekxJOEJvMSJ9.eyJpc3MiOiJodHRwczovL3NvbGF0ZS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjJkZDFlZTJlNTE4ZWJiNjc3NWViODVkIiwiYXVkIjpbImNhc3RpbmdhZ2VuY3kiLCJodHRwczovL3NvbGF0ZS51cy5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNjU5MTcwMTk4LCJleHAiOjE2NTkyNTY1OTgsImF6cCI6ImJxYjdSTnJ5OWx4ajB1eGN1eHloTlVnU2RPdzlKVExEIiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIl19.jaJDllfSsNOTWGivyhHAy524xk2PWB0rtVK6bdPhuG-fv2QrPUOAapSxJ0mGL4Af6BPGplj9jaDZ9kGyxI7wdgAMQcfqNKT1dms16FhbLrZq3iSSf3KIuAK1-RXDttFz90bk15tySFe_oyxoyBZgzOT6yzgSHnSLduPU1fD3gi7dVT4MOVy9XSzw6INsvZfK1Pxt6mFtq-55fRC652X9oLsgKefAj_F4MrAN4psOsq8HDFMGSH-yvvE5U_A9Dw0yoYXFMRMEXgAf_kyizc44L70vTBQHv8I0MnGI2SEaTNIftKW_6g8KvipsgzTT0zOtdd6Q7eLn4z2JEX93G_4jOg'
#JWT_CAST_DIRECTOR = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjBRRmt5TjFCaFN4NzhoekxJOEJvMSJ9.eyJpc3MiOiJodHRwczovL3NvbGF0ZS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjJlMmI4MWNlYTQ4Mzk4NzQyMmRlZTMyIiwiYXVkIjpbImNhc3RpbmdhZ2VuY3kiLCJodHRwczovL3NvbGF0ZS51cy5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNjU5MTcwMjU0LCJleHAiOjE2NTkyNTY2NTQsImF6cCI6ImJxYjdSTnJ5OWx4ajB1eGN1eHloTlVnU2RPdzlKVExEIiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIl19.DnptfnSdhCIe-uFbe50p1H7UHZVP4rHZIuXeLmEIsG9qgqwL4419R7dH8o_HDtLTn3IIKFPYmytnNwRBkaJmkr9SDFszH2bAbxfi5DQUyTAwT_J_xUuN_SGM00676G2gG7CEv8tjxxKUn1vmr0oBmb1k4FHd4QghRtgrtbLSk2X4JqFNqPT9ZxUMj8oG0ggmNeq6avYqsNj-I8kOpUD1nT1q8Z1svjsgQOlhP7t5-XT7QRXM0-1vHfhgB-dNL18bVtil1x_A53iMyOzSNNCVJYdgRZSc3-JB2eLqOaZOpBLzZcbYII2Dk3el_pZMtvV4ewKy-_w0AsdDs4YHJXU9kQ'
#JWT_EXEC_PRODUCER = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjBRRmt5TjFCaFN4NzhoekxJOEJvMSJ9.eyJpc3MiOiJodHRwczovL3NvbGF0ZS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjJlM2Y0ZmZiMzEwNzRjZTg0OGFkMjcxIiwiYXVkIjpbImNhc3RpbmdhZ2VuY3kiLCJodHRwczovL3NvbGF0ZS51cy5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNjU5MTA2NzIxLCJleHAiOjE2NTkxOTMxMjEsImF6cCI6ImJxYjdSTnJ5OWx4ajB1eGN1eHloTlVnU2RPdzlKVExEIiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIl19.DBEZN6vqkCv4W05fXkZFCEXVGQhj64aQV95mOZQoA2wVESS-xe-Pq0CJilhK_nILJGwca7wIbSLMCvFkFYpwJOsniCHMNG2zO7bL9hhJ12ZToaLmlTs2Rhu6I7Xh0TTgLOAxvEAkAIT_GDI2GacCrIS7lmFHelHF_z97_lby2m9NxzmtN_AiUr5bbg4matMz2iEQedTn3dAalF8BiJBcoTaC60JA7fKzU6Po5w-QCyjLzsS7nZ6ju22s-q5AmX2yyaW8jfNVyYQuW3DPx_lVTAU7ruswkL4NTQ_7kxJVba-8X3tJXsJpUEVtM0VvpIiCEeSQMaF8ZtVwf9FIc-SnCg'

class CastingAgencyTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app
        self.client = self.app.test_client

        self.app.config['SQLALCHEMY_DATABASE_URI'] = DB_PATH
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

        with self.app.app_context():
            self.db = db
            self.db.init_app(self.app)
            self.db.create_all()

            self.headers_cast_assistant = {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer' + ' ' + JWT_CAST_ASSISTANT
            }

            self.headers_cast_director = {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer' + ' ' + JWT_CAST_DIRECTOR
            }

            self.headers_exec_producer = {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer' + ' ' + JWT_EXEC_PRODUCER
            }

            '''
            actor = Actor(
                name = 'Buffy',
                age = '42',
                gender = 'female'
            )
            actor.insert()

            self.actor_test_id = actor.id
            print('ACTOR_TEST_ID', self.actor_test_id)

            movie = Movie(
                title = 'Buffy the Vampire Slayer',
                release_date = '2022-08-01'
            )
            movie.insert()
            '''

            self.actor_test_id = 15
            self.actor_updated_test_id = self.actor_test_id + 1

            self.new_actor = {
                'name': 'George Clooney',
                'age': '65',
                'gender': 'male'
            }

            self.updated_actor = {
                'name': 'George Clooney',
                'age': '61',
                'gender': 'male'
            }

            self.movie_test_id = 26
            self.movie_updated_test_id = self.movie_test_id + 1

            self.new_movie = {
                'title': "Child's Play",
                'release_date': '1990-01-25'
            }

            self.updated_movie = {
                'title': 'Bevery Hills Cop',
                'release_date': '1985-03-27'
            }

    def tearDown(self):
        pass

    def test_get_actors(self):
        res = self.client().get('/actors', headers=self.headers_cast_assistant)
        data = json.loads(res.data)
        self.assertTrue(data['list_actors'])
        self.assertTrue(data['actors_count'])
        self.assertEqual(res.status_code, 200)

    def test_get_actors_without_auth_header(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], 'authorization_header_missing')
        self.assertEqual(data['description'], 'Authorization header is expected.')

    def test_get_movies(self):
        res = self.client().get('/movies', headers=self.headers_cast_assistant)
        data = json.loads(res.data)
        #print('Movies:', data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['list_movies'])
        self.assertTrue(data['movies_count'])

    def test_get_movies_without_auth_header(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], 'authorization_header_missing')
        self.assertEqual(data['description'], 'Authorization header is expected.')

    def test_post_actor(self):
        res = self.client().post('/add_actor', json=self.new_actor, headers=self.headers_cast_director)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['Success'], True)
        self.assertTrue(data['actors_list'])
        self.assertTrue(data['actors_count'])

    def test_post_actor_without_permission(self):
        res = self.client().post('/add_actor', json=self.new_actor, headers=self.headers_cast_assistant)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found')
    
    def test_post_actor_without_auth_header(self):
        res = self.client().post('/add_actor', json=self.new_actor)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], 'authorization_header_missing')
        self.assertEqual(data['description'], 'Authorization header is expected.')
    
    def test_delete_actor(self):
        #print('THIS IS ACTOR_TEST_ID', self.actor_test_id)
        res = self.client().delete('/actors/' + str(self.actor_test_id), headers=self.headers_cast_director)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['Success'], True)
        self.assertTrue(data['actor_id'])
        self.assertTrue(data['actors_list'])
        self.assertTrue(data['actors_count'])
    
    def test_delete_actor_without_permission(self):
        res = self.client().delete('/actors/' + str(self.actor_test_id), headers=self.headers_cast_assistant)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found')

    def test_delete_actor_without_auth_header(self):
        res = self.client().delete('/actors/' + str(self.actor_test_id))
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], 'authorization_header_missing')
        self.assertEqual(data['description'], 'Authorization header is expected.')

    def test_update_actor(self):
        res = self.client().patch('/actors/' + str(self.actor_updated_test_id), json=self.updated_actor, headers=self.headers_cast_director)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['actor_id'])
        self.assertTrue(data['actors_list'])
        self.assertTrue(data['actors_count'])

    def test_update_actor_without_permission(self):
        res = self.client().patch('/actors/' + str(self.actor_updated_test_id), json=self.updated_actor, headers=self.headers_cast_assistant)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found') 

    def test_update_actor_without_auth_header(self):
        res = self.client().patch('/actors/' + str(self.actor_updated_test_id), json=self.updated_actor)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertTrue(data['code'], 'authorization_header_missing')
        self.assertTrue(data['description'], 'Authorization header is expected.')

    def test_update_movie(self):
        res = self.client().patch('/movies/' + str(self.movie_updated_test_id), json=self.updated_movie, headers=self.headers_cast_director)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['Success'], True)
        self.assertTrue(data['movie_id'])
        self.assertTrue(data['movies_list'])
        self.assertTrue(data['movies_count'])

    def test_update_movie_without_permission(self):
        res = self.client().patch('/movies/' + str(self.movie_updated_test_id), json=self.updated_movie, headers=self.headers_cast_assistant)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found')

    def test_update_movie_without_auth_header(self):
        res = self.client().patch('/movies/' + str(self.movie_updated_test_id), json=self.updated_movie)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], 'authorization_header_missing')
        self.assertEqual(data['description'], 'Authorization header is expected.')

    def test_post_movie(self):
        res = self.client().post('/add_movie', json=self.new_movie, headers=self.headers_exec_producer)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['Success'], True)

    def test_post_movie_without_permission(self):
        res = self.client().post('/add_movie', json=self.new_movie, headers=self.headers_cast_director)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found')

    def test_post_movie_without_auth_header(self):
        res = self.client().post('/add_movie', json=self.new_movie)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], 'authorization_header_missing')
        self.assertEqual(data['description'], 'Authorization header is expected.')

    def test_delete_movie(self):
        print('IN TEST DELETE MOVIE, VALUE OF ID:', self.movie_test_id)
        res = self.client().delete('/movies/' + str(self.movie_test_id), headers=self.headers_exec_producer)
        data = json.loads(res.data)
        print('DATA SUCCESS', data['Success'])
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['Success'], True)
        self.assertEqual(data['movie_id'], self.movie_test_id)
        self.assertTrue(data['movies_list'])
        self.assertTrue(data['movies_count'])

    def test_delete_movie_without_permission(self):
        res = self.client().delete('/movies/' + str(self.movie_test_id), headers=self.headers_cast_director)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found')

    def test_delete_movie_without_auth_header(self):
        res = self.client().delete('/movies/' + str(self.movie_test_id))
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], 'authorization_header_missing')
        self.assertEqual(data['description'], 'Authorization header is expected.')

    
if __name__ == '__main__':
    unittest.main()