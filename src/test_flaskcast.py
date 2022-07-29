import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from flaskcast import app
from flaskcast.models import db, Actor, Movie


DB_PATH = "postgresql://gpayan@localhost:5432/casting_agency_test"
JWT_CAST_ASSISTANT = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjBRRmt5TjFCaFN4NzhoekxJOEJvMSJ9.eyJpc3MiOiJodHRwczovL3NvbGF0ZS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjJkZDFlZTJlNTE4ZWJiNjc3NWViODVkIiwiYXVkIjpbImNhc3RpbmdhZ2VuY3kiLCJodHRwczovL3NvbGF0ZS51cy5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNjU5MDI0NzUzLCJleHAiOjE2NTkxMTExNTMsImF6cCI6ImJxYjdSTnJ5OWx4ajB1eGN1eHloTlVnU2RPdzlKVExEIiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIl19.jkpOAlDZeAzCtBCTaKTwgTWzLUALQ3Zy9yT-Mmxb59kO_cUzbtxMmyMWEh4eBGXLuoGz2QFzRB71AhFO7B7T0-OC2immotQP0F767E2OS_GIFOjhRSSzT95Jr2u_NMP_JF4ESTMpHJIBicgw7L0A9lIaSop83L1lUpbScGGJethxBNki0aADDezLhuCtCuIz5vAkmdtDuOwZWJa7faH_TLlmmoqa5_CRZh_ejpV_0GMNKTQT1a2WLv_eUTncKBwO2YiVS9MKGxbL-IHgGR_dBrkb7EB9cE3mGLf0Rt2oDJJdD1ibDZSndAIwG4zI1zxBq905T57Uuxa6VZxhADWyLg'
JWT_CAST_DIRECTOR = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjBRRmt5TjFCaFN4NzhoekxJOEJvMSJ9.eyJpc3MiOiJodHRwczovL3NvbGF0ZS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjJlMmI4MWNlYTQ4Mzk4NzQyMmRlZTMyIiwiYXVkIjpbImNhc3RpbmdhZ2VuY3kiLCJodHRwczovL3NvbGF0ZS51cy5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNjU5MDI2MTY3LCJleHAiOjE2NTkxMTI1NjcsImF6cCI6ImJxYjdSTnJ5OWx4ajB1eGN1eHloTlVnU2RPdzlKVExEIiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIl19.itvqGKDcjhx8KKGIN3kc5L0s-v-YYwqY83_TESGUoQKl9-pmIWjmBI8ezptAmKI2vbQKeEXTi39GcG-meyc5Qg5xRHyj0HZktLXd7VsE1XxOFmoxOFdTzy3tQzKzl0V3NGYzoik-Zy4-P7_lYpDrBS7K1eGHX156ANmbCFH8XChmBbMMrdFl6RxqmsmV5JerctZLG0o4XMg1FUPiqmqlN6lYWOmUHpP_rfWAHsvoKlv0Yo_Xny0vzUCD9A-RD3kp4DXxJ89L5Zpx_mMLiTv4QQK_YwglUke_TLSvdjxm5mhmlsMVm2_w3L-f30ODL6RQ9yHrbTl9ciPElblBIc0Hww'
JWT_EXEC_PRODUCER = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjBRRmt5TjFCaFN4NzhoekxJOEJvMSJ9.eyJpc3MiOiJodHRwczovL3NvbGF0ZS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjJlM2Y0ZmZiMzEwNzRjZTg0OGFkMjcxIiwiYXVkIjpbImNhc3RpbmdhZ2VuY3kiLCJodHRwczovL3NvbGF0ZS51cy5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNjU5MTA2NzIxLCJleHAiOjE2NTkxOTMxMjEsImF6cCI6ImJxYjdSTnJ5OWx4ajB1eGN1eHloTlVnU2RPdzlKVExEIiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIl19.DBEZN6vqkCv4W05fXkZFCEXVGQhj64aQV95mOZQoA2wVESS-xe-Pq0CJilhK_nILJGwca7wIbSLMCvFkFYpwJOsniCHMNG2zO7bL9hhJ12ZToaLmlTs2Rhu6I7Xh0TTgLOAxvEAkAIT_GDI2GacCrIS7lmFHelHF_z97_lby2m9NxzmtN_AiUr5bbg4matMz2iEQedTn3dAalF8BiJBcoTaC60JA7fKzU6Po5w-QCyjLzsS7nZ6ju22s-q5AmX2yyaW8jfNVyYQuW3DPx_lVTAU7ruswkL4NTQ_7kxJVba-8X3tJXsJpUEVtM0VvpIiCEeSQMaF8ZtVwf9FIc-SnCg'

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

            self.actor_test_id = 14
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

            self.movie_test_id = 24
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
        self.assertTrue(data['list_movies'])
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
        self.assertTrue(data)
        self.assertEqual(res.status_code, 200)

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
        res = self.client().delete('/movies/' + str(self.movie_test_id), headers=self.headers_exec_producer)
        data = json.loads(res.data)
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