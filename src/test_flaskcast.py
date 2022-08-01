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
#JWT_CAST_ASSISTANT = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjBRRmt5TjFCaFN4NzhoekxJOEJvMSJ9.eyJpc3MiOiJodHRwczovL3NvbGF0ZS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjJkZDFlZTJlNTE4ZWJiNjc3NWViODVkIiwiYXVkIjpbImNhc3RpbmdhZ2VuY3kiLCJodHRwczovL3NvbGF0ZS51cy5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNjU5MzQxNjM3LCJleHAiOjE2NTk0MjgwMzcsImF6cCI6ImJxYjdSTnJ5OWx4ajB1eGN1eHloTlVnU2RPdzlKVExEIiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIl19.XF2gG6zkRfVRs-GCyZs7gTTS1iRgGCsZ9QALbFx5gHBaak7LHtpmBMIHYqCt90OTBxN9SUp4mAZ_vBndx6MGahjFR7bcM9qqVR6XFRHtSKIy4vvK-YNDbptF-qJFNP4AYBXiIuOhJgYQ--Y-8_n-un1z5zDlB6EBDi1LcAC_mzy6mxVwouIgUS380vZKovFd3MksUDvs_G-4nXMCc8c0PM5iyQxSnXOJJIBWj7NF-h7ZR62lLVuZ9VWwpQOBQkWGyGQL8aAuWRoAH2-gi22QaxShuThTb1fGuRPkq9LXlouDs1x4MVwoRqWpOy8IEVBQVBnKZ3XcGhYpWmn-ZElx9A'
#JWT_CAST_DIRECTOR = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjBRRmt5TjFCaFN4NzhoekxJOEJvMSJ9.eyJpc3MiOiJodHRwczovL3NvbGF0ZS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjJlMmI4MWNlYTQ4Mzk4NzQyMmRlZTMyIiwiYXVkIjpbImNhc3RpbmdhZ2VuY3kiLCJodHRwczovL3NvbGF0ZS51cy5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNjU5MzQxNzE4LCJleHAiOjE2NTk0MjgxMTgsImF6cCI6ImJxYjdSTnJ5OWx4ajB1eGN1eHloTlVnU2RPdzlKVExEIiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIl19.G4AItiXnb8DNj-v7Q7pghKsgejmO8aa_8XGpV7z0pWQJrfbjLYdt3bIUtOo8TVYpAPgqiwe1J2LQPtsQXkklb96tdwxKBi0zbdkX7wcpy_gW1KOyeVKG05V1MALRwGo6xeaaTGs8lh1hzef2_CGTJs9kNTCA3ZqgFVnJaWemD_uAL3ijGJxAKlh2b9thSpJPacvVb5VK_r7R6kRujTHkZPGEE8qhqYbn0QEvD1i9IaCUDVrW-sDs2vpyXUILCLKD-OOUKx9OkBMX2jKgsqX-IgvKQRBAkmQvz1MvE9b_v9oxDmGYg0P6BKPB8NaCLnbVCK_UwVhkxXnV0vq0fPsDNA'
#JWT_EXEC_PRODUCER = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjBRRmt5TjFCaFN4NzhoekxJOEJvMSJ9.eyJpc3MiOiJodHRwczovL3NvbGF0ZS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjJlM2Y0ZmZiMzEwNzRjZTg0OGFkMjcxIiwiYXVkIjpbImNhc3RpbmdhZ2VuY3kiLCJodHRwczovL3NvbGF0ZS51cy5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNjU5MzQxNzk5LCJleHAiOjE2NTk0MjgxOTksImF6cCI6ImJxYjdSTnJ5OWx4ajB1eGN1eHloTlVnU2RPdzlKVExEIiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIl19.V80hKkgjGBVmO7jQTk-Q9p1h-FsJum5N6SF8JSAqQvzRe5JQFAaw3lci1e7YPEtIFm-JTvXXz6rFB7W6fmm2XPkWJrMSvi5FHPJPjfq1pIoebolRh8L15eUGajSqU7BM5y2miz-J5qjoxPD9T8UCAZBwPjyqL7k6qfHQVMDWlWKeKp8pWyY8oaCUrOD7Hm5GeLEaT7AIUGZS6VQFQ68JGtmaqIxKww4g_b4r5Q7w-h2Q9Owe5ry9U7--7gCVG_Aw7CDN_NHuR0yOtBd_CudlZl0fFFUhTe8JXf3K4f60nECGIrwKE9YydF9i1e7V5xXunvqcjdPhAb8NUzsAOZnCqg'

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

            self.actor_test_id = 18
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

            self.new_actor_without_name = {
                'age': 32,
                'gender': 'female'
            }

            self.movie_test_id = 29
            self.movie_updated_test_id = self.movie_test_id + 1

            self.new_movie = {
                'title': "Child's Play",
                'release_date': '1990-01-25'
            }

            self.updated_movie = {
                'title': 'Bevery Hills Cop',
                'release_date': '1985-03-27'
            }

            self.new_movie_without_title = {
                'release_date': '1990-01-25'
            }

            self.updated_movie_with_compromised_list_of_actors = {
                'title': 'The sixth sense',
                'release_date': '1990-01-25',
                'movie_cast': [598, 25, 54]
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
        self.assertEqual(data['success'], True)
        self.assertTrue(data['new_actor_id'])
        self.assertTrue(data['actors_count'])

    def test_post_actor_without_actor_name(self):
        res = self.client().post('/add_actor', 
                                 json=self.new_actor_without_name,
                                 headers=self.headers_cast_director)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'],'invalid request')
        self.assertEqual(data['error'], 400)

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
        self.assertEqual(data['success'], True)
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
        self.assertEqual(data['success'], True)
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
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie_id'])
        self.assertTrue(data['movies_list'])
        self.assertTrue(data['movies_count'])

    def test_update_movie_with_compromised_list_of_actors(self):
        res = self.client().patch('/movies/' + str(self.movie_updated_test_id), 
                                  json=self.updated_movie_with_compromised_list_of_actors,
                                  headers=self.headers_cast_director)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 422)
        self.assertEqual(data['message'], 'unable to be processed')
        
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
        self.assertEqual(data['success'], True)
        self.assertTrue(data['new_movie_id'])
        self.assertTrue(data['movies_count'])

    def test_post_movie_without_movie_title(self):
        res = self.client().post('/add_movie', json=self.new_movie_without_title, headers=self.headers_exec_producer)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], 'invalid request')

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
        #print('IN TEST DELETE MOVIE, VALUE OF ID:', self.movie_test_id)
        res = self.client().delete('/movies/' + str(self.movie_test_id), headers=self.headers_exec_producer)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
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

    def test_get_actor_filmography(self):
        res = self.client().get('/actors/' + str(self.actor_updated_test_id) + '/movies',
                                headers = self.headers_cast_assistant)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor_id'])
        #data['list_of_movies'] can be empty if an actor isn't featured in any movies.
        #self.assertTrue(data['list_of_movies'])

    def test_get_actor_filmography_for_nonexistant_actor(self):
        #we are assuming there is no actor in our database with the id: 50000
        res = self.client().get('/actors/50000/movies', headers = self.headers_cast_assistant)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')

    def test_get_actor_filmography_without_auth_header(self):
        res = self.client().get('/actors/' + str(self.actor_updated_test_id) + '/movies')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], 'authorization_header_missing')
        self.assertEqual(data['description'], 'Authorization header is expected.')

    def test_get_movie_cast(self):
        res = self.client().get('/movies/' + str(self.movie_updated_test_id) + '/actors',
                                headers=self.headers_cast_assistant)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie_id'])
        #data['film_cast_list'] can be empty if no actors are feature in this movie
        #self.assertTure(data['film_cast_list'])

    def test_get_movie_cast_for_nonexistant_movie(self):
        #we are assuming there is no movie in our database with the id: 50000
        res = self.client().get('/movies/50000/actors', headers=self.headers_cast_assistant)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')

    def test_get_movie_cast_without_auth_header(self):
        res = self.client().get('/movies/' + str(self.movie_updated_test_id) + '/actors')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], 'authorization_header_missing')
        self.assertEqual(data['description'], 'Authorization header is expected.')

if __name__ == '__main__':
    unittest.main()