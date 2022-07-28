import os
from flaskcast import app
from flaskcast.models import Actor, Movie
from flask import request, render_template, jsonify
from flaskcast.auth import requires_auth, AuthError


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/movies', methods=['GET'])
@requires_auth('get:movies')
def get_movies(payload):
    movies = Movie.query.order_by('title').all()
    list_movies = [movie.format() for movie in movies]
    return jsonify({
        'list_movies': list_movies
    })


@app.route('/add_movie', methods=['POST'])
def add_movie():
    data = request.get_json()
    movie_title = data.get('title')
    release_date = data.get('release_date')
    actors = data.get('actors', '')

    print('Release date', release_date)

    new_movie = Movie(
        title = movie_title,
        release_date = release_date
    )

    try:
        new_movie.insert()
    except Exception as e:
        print('Issue adding new movie to database', e)
    
    return jsonify({
        'Success': True
    })


@app.route('/movies/<int:movie_id>', methods=['DELETE'])
@requires_auth('get:movies')
def delete_movie(payload, movie_id):

    movie_to_delete = Movie.query.filter_by(id=movie_id).one_or_none()
    
    try:
        movie_to_delete.delete()
    except Exception as e:
        print('Issue deleting movie form database', e)

    return jsonify({
        'Success': True
    })


@app.route('/actors', methods=['GET'])
def get_actors():
    actors = Actor.query.order_by('name').all()
    actors_list = [actor.format() for actor in actors]

    movies = Movie.query.order_by('title').all()
    movies_list = [movie.format() for movie in movies]

    return jsonify({
        'list_actors': actors_list,
        'list_movies': movies_list
        })


@app.route('/add_actor', methods=['POST'])
def add_actor():

    data = request.get_json()
    print(data)
    actor_name = data.get('name')
    actor_age = data.get('age')
    actor_gender = data.get('gender')
    starred_movies = data.get('starred_movies', '')

    print('STARRED_MOVIES is:', starred_movies)

    new_actor = Actor(
        name = actor_name,
        age = actor_age,
        gender = actor_gender
    )

    list_movies = []
    for movie_id in starred_movies:
        movie = Movie.query.filter_by(id=movie_id).one_or_none()
        if movie:
            list_movies.append(movie)
    
    new_actor.cast = list_movies
    new_actor.insert()

    return jsonify({
        'Success': True
    })


@app.route('/actors/<int:actor_id>', methods=['DELETE'])
@requires_auth('delete:actors')
def delete_actor(payload, actor_id):
    actor_to_delete = Actor.query.filter_by(id=actor_id).one_or_none()
    try:
        actor_to_delete.delete()
    except Exception as e:
        print(e)
    return jsonify({
        'Success': True,
        'Actor_id': actor_to_delete.id
    })


@app.route('/actors/<int:actor_id>', methods=['GET', 'PATCH'])
def update_actor(actor_id):
    actor = Actor.query.filter_by(id=actor_id).one_or_none()
    if request.method == 'PATCH':
        data = request.get_json()
        print('WE HAVE RECEIVED A PATCH REQUEST')
        print(data)

        actor.name = data.get('name')
        actor.age = data.get('age')
        actor.gender = data.get('gender')
        starred_movies_updated = data.get('starred_movies')

        list_movies = []
        for movie_id in starred_movies_updated:
            movie = Movie.query.filter_by(id=movie_id).one_or_none()
            if movie:
                list_movies.append(movie)
    
        actor.cast = list_movies

        actor.update()

        return jsonify({
            'Success': True,
            'Actor_id': actor_id
        })

    else: 
        starred_movies = actor.cast
        id_movie_list = [movie.id for movie in starred_movies]
        return jsonify({
            'id': actor.id,
            'name': actor.name,
            'age': actor.age,
            'gender': actor.gender,
            'starred_movies': id_movie_list
        })


@app.errorhandler(AuthError)
def handler_for_autherror(error):
    print('Handling a AuthError')
    response = jsonify(error.error)
    response.status_code = error.status_code
    return response