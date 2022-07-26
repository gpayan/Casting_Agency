import os
#from flaskcast import app
from . import app #fix for Heroku deployment
#from flaskcast.models import Actor, Movie
from .models import Actor, Movie #fix for Heroku deployment
from flask import request, render_template, jsonify, abort
#from flaskcast.auth import requires_auth, AuthError
from .auth import requires_auth, AuthError

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/movies', methods=['GET'])
@requires_auth('get:movies')
def get_movies(payload):
    movies = Movie.query.order_by('title').all()

    if len(movies) == 0:
        abort(404)

    list_movies = [movie.format() for movie in movies]

    return jsonify({
        'list_movies': list_movies,
        'movies_count': len(list_movies)
    })


@app.route('/add_movie', methods=['POST'])
@requires_auth('post:movies')
def add_movie(payload):
    data = request.get_json()
    movie_title = data.get('title', None)
    release_date = data.get('release_date', None)
    actors = data.get('actors', '')

    if (movie_title == None or release_date == None):
        abort(400)

    new_movie = Movie(
        title = movie_title,
        release_date = release_date
    )

    try:
        new_movie.insert()
    except Exception as e:
        print('Issue adding new movie to database', e)

    try:
        movies_count = Movie.query.count()
    except Exception as e:
        print('Issue counting movies in database', e)
    
    return jsonify({
        'new_movie_id': new_movie.id,
        'success': True,
        'movies_count': movies_count
    })


@app.route('/movies/<int:movie_id>', methods=['GET', 'PATCH'])
@requires_auth('patch:movies')
def patch_movie(payload, movie_id):
    
    movie = Movie.query.filter_by(id=movie_id).one_or_none()
    if movie is None:
        abort(404)

    if request.method == 'PATCH':
        data = request.get_json()
        movie_title = data.get('title', None)
        movie_release_date = data.get('release_date', None)
        movie_cast_id_updated = data.get('movie_cast','')

        if movie_title is None or movie_release_date is None:
            abort(400)
        movie.title = movie_title
        movie.release_date = movie_release_date

        list_actors = []
        for actor_id in movie_cast_id_updated:
            actor = Actor.query.filter_by(id=actor_id).one_or_none()
            if actor:
                list_actors.append(actor)
            else:
                abort(422)

        movie.actors = list_actors
        try:
            movie.update()
        except Exception as e:
            print('Issue updating movie data', e)

        movies = Movie.query.order_by('title').all()
        movies_list = [movie.format() for movie in movies]

        return jsonify({
            'success': True,
            'movie_id': movie.id,
            'movies_list': movies_list,
            'movies_count': len(movies_list)
        })
    else:
        movie_cast = movie.actors
        id_actors_list = [actor.id for actor in movie_cast]
        return jsonify({
            'id': movie_id,
            'title': movie.title,
            'release_date': movie.release_date,
            'movie_cast': id_actors_list
        })


@app.route('/movies/<int:movie_id>', methods=['DELETE'])
@requires_auth('delete:movies')
def delete_movie(payload, movie_id):

    movie_to_delete = Movie.query.filter_by(id=movie_id).one_or_none()
    if movie_to_delete is None:
        abort(404)
    
    try:
        movie_to_delete.delete()
    except Exception as e:
        print('Issue deleting movie form database', e)

    movies = Movie.query.order_by('title').all()
    movies_list = [movie.format() for movie in movies]

    return jsonify({
        'success': True,
        'movie_id': movie_to_delete.id,
        'movies_list': movies_list,
        'movies_count': len(movies_list)
    })


@app.route('/movies/<int:movie_id>/actors', methods=['GET'])
@requires_auth('get:actors')
def get_movie_cast(payload, movie_id):
    movie = Movie.query.filter_by(id=movie_id).one_or_none()

    if movie is None:
        abort(404)

    film_cast = movie.actors
    film_cast_list = [actor.format() for actor in film_cast]

    return jsonify({
        'success': True,
        'movie_id': movie_id,
        'film_cast_list': film_cast_list
    })


@app.route('/actors', methods=['GET'])
@requires_auth('get:actors')
def get_actors(payload):
    actors = Actor.query.order_by('name').all()

    if len(actors) == 0:
        abort(404)

    actors_list = [actor.format() for actor in actors]

    #movies = Movie.query.order_by('title').all()
    #movies_list = [movie.format() for movie in movies]

    return jsonify({
        'list_actors': actors_list,
        'actors_count': len(actors_list)
    })


@app.route('/add_actor', methods=['POST'])
@requires_auth('post:actors')
def add_actor(payload):

    data = request.get_json()
    actor_name = data.get('name', None)
    actor_age = data.get('age', None)
    actor_gender = data.get('gender', None)
    starred_movies = data.get('starred_movies', '')

    if actor_name is None or actor_age is None or actor_gender is None:
        abort(400)

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
        else:
            abort(422)
    
    new_actor.cast = list_movies
    new_actor.insert()

    actors_count = Actor.query.count()

    return jsonify({
        'success': True,
        'new_actor_id': new_actor.id,
        'actors_count': actors_count
    })


@app.route('/actors/<int:actor_id>', methods=['DELETE'])
@requires_auth('delete:actors')
def delete_actor(payload, actor_id):
    actor_to_delete = Actor.query.filter_by(id=actor_id).one_or_none()
    if actor_to_delete is None:
        abort(404)

    try:
        actor_to_delete.delete()
    except Exception as e:
        print('Issue deleting actor form database', e)

    actors = Actor.query.order_by('name').all()
    actors_list = [actor.format() for actor in actors]

    return jsonify({
        'success': True,
        'actor_id': actor_to_delete.id,
        'actors_list': actors_list,
        'actors_count': len(actors_list)
    })


@app.route('/actors/<int:actor_id>', methods=['GET', 'PATCH'])
@requires_auth('patch:actors')
def update_actor(payload, actor_id):
    actor = Actor.query.filter_by(id=actor_id).one_or_none()

    if actor is None:
        abort(404)

    if request.method == 'PATCH':
        data = request.get_json()

        updated_name = data.get('name', None)
        updated_age = data.get('age', None)
        updated_gender = data.get('gender', None)
        starred_movies_updated = data.get('starred_movies', '')

        if updated_name is None or updated_age is None or updated_gender is None:
            abort(400)

        actor.name = updated_name
        actor.age = updated_age
        actor.gender = updated_gender

        list_movies = []
        for movie_id in starred_movies_updated:
            movie = Movie.query.filter_by(id=movie_id).one_or_none()
            if movie:
                list_movies.append(movie)
            else:
                abort(422)
    
        actor.cast = list_movies
        actor.update()

        actors = Actor.query.order_by('name').all()
        actors_list = [actor.format() for actor in actors]

        return jsonify({
            'success': True,
            'actor_id': actor_id,
            'actors_list': actors_list,
            'actors_count': len(actors_list)
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


@app.route('/actors/<int:actor_id>/movies')
@requires_auth('get:movies')
def get_filmography(payload, actor_id):

    actor = Actor.query.filter_by(id=actor_id).one_or_none()

    if actor is None:
        abort(404)

    filmography = actor.cast
    list_of_movies = [film.format() for film in filmography]

    return jsonify({
        'success': True,
        'actor_id': actor_id,
        'list_of_movies': list_of_movies,
    })

@app.errorhandler(AuthError)
def handler_for_autherror(error):
    print('Handling a AuthError')
    response = jsonify(error.error)
    response.status_code = error.status_code
    return response


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'error': 404,
        'success': False,
        'message': 'resource not found'
    }), 404


@app.errorhandler(400)
def invalid_request(error):
    return jsonify({
        'success': False,
        'error': 400,
        'message': 'invalid request'
    }), 400


@app.errorhandler(422)
def cant_process(error):
    return jsonify({
        'success': False,
        'error': 422,
        'message': 'unable to be processed'
    }), 422