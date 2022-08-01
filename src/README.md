## API Reference 

### Getting started

- Base URL: 
- Authentication: The app requires authentication.

### Error handling

Errors are returned as JSON objects in the following format:

'''
{
    'success': False,
    'error': 400,
    'message': 'bad request'
}
'''

The API will return 3 errors types when requests fail:
- 400: bad request
- 404: resource not found
- 422: request unable to be proccessed

### Endpoints

#### GET '/actors'
- Fetches a dictionay with the list of actors (key: ```list_actors```) and the total number of actors returned (key: ```actors_count```). Each entry in the list of actor describes an actor with:
    - actor's id
    - actor's name
    - actor's age
    - actor's gender
- Request arguments: None.
- If there is no actor entries in the database, returns a 404 error.
- Authorization: Requires the ```get:actors``` permission to be accessed.
- Sample: ```curl https://127.0.0.1:5000/actors```

#### GET '/actors/{actor_id}/movies'
- Fetches a dictionary with the filmography (list of movies with key: ```list_of_movies```) of the actor with ```actor_id```. The dictionary includes the id of the actor (key: ```actor_id```) and the sucess factor (key: ```success```). Each entry in the list of movies describes a movie with:
    - movie's title
    - movie's release data
- Request arguments: actor's unique id (stored in the database).
- Returns: Returns an empty array if actor is not appearing in any movie stored in the database. If there is no actor in the datbase with submitted ```actor_id``` returns 404. 
- Authorization: Requires the ```get:movies``` permission to be accessed.
- Sample: ```curl https://127.0.0.1:5000/actors/13/movies```

```
{
  "actor_id": 13, 
  "list_of_movies": [
    {
      "id": 13, 
      "release_date": "Fri, 04 Feb 2000 00:00:00 GMT", 
      "title": "Harry Potter v3"
    }, 
    {
      "id": 15, 
      "release_date": "Thu, 24 Oct 1996 00:00:00 GMT", 
      "title": "Beverly Hills Cop 2"
    }
  ], 
  "success": true
}
```

#### GET '/movies'
- Fetches a dictionary with the list of movies (key: ```list_movies```) and the total number of movies (key: ```movies_count```). Each entry in the list of movies describes a movie with:
    - movie's title
    - movie's release date
- Request arguments: None.
- If there is no movie entries in the database, returns a 404 error.
- Authorization: Requires the ```get:movies``` permission to be accessed.
- Sample: ```curl https://127.0.0.1:5000/movies```

#### GET '/movies/{movie_id}/actors'
- Fetches a dictionary with the cast of a movie (list of actors with key: ```film_cast_list```) of the movie with ```movie_id```. The dictionary also includes the id of the movie (key: ```movie_id```), and the success factor (key: ```success```). Each entry in the list of actors describes an actor with:
    - actor's id
    - actor's name
    - actor's age
    - actor's genre
- Request arguments: movie's unique id (stored in the database).
- Returns: Returns an empty array if no actors are featured in the movie stored in the database. If there is no movie in the datbase with submitted ```movie_id``` returns 404. 
- Authorization: Requires the ```get:actors``` permission to be accessed.
- Sample: ```curl https://127.0.0.1:5000/movies/11/actors```

```
{
  "film_cast_list": [
    {
      "age": 32, 
      "gender": "female", 
      "id": 1, 
      "name": "Bunny BB"
    }, 
    {
      "age": 69, 
      "gender": "male", 
      "id": 13, 
      "name": "Daniel Payan"
    }, 
    {
      "age": 61, 
      "gender": "male", 
      "id": 15, 
      "name": "George Clooney"
    }, 
    {
      "age": 55, 
      "gender": "male", 
      "id": 14, 
      "name": "Bruce Willis"
    }, 
    {
      "age": 85, 
      "gender": "male", 
      "id": 16, 
      "name": "Jacques Chirac"
    }
  ], 
  "movie_id": 13, 
  "success": true
}
```

#### POST '/add_movie'
- Creates a new movie with the submitted: title and release date. Returns the id of the newly created movie, the success value, and the new total number of movies.
- Request arguments: 
    - New movie's title
    - New movie's release date
- Returns: an object with 4 keys: the success factor (key: ```success```), the movie_id of the newly created movie (key: ```movie_id```), and total number of movies stored in the database (key: ```movies_count```).
- If the title or release date of the movie are not submitted, returns a 400 error. 
- Authorization: Requires the ```post:movies``` permission to be accessed.
- Sample: ```curl https://```

#### POST '/add_actor'
- Creates a new actor with the submitted: actor's name, actor's gender, actor's age, and as an option the list of movies the newly created actor starred in. Returns the id of the newly created actor, the success value, and the new total number of actors.
- Request arguments:
    - New actor's name
    - New actor's age
    - New actor's gender
    - [optionally] List of movies (ids of the movies) the actor was featured in.
- Returns: an object with 3 keys: the success factor(key: ```success```), the actor_id of the newly created actor (key: ```actor_id```), and total number of actors in the database (key: ```actors_count```)
- If the actor's name, gender or age are missing, returns a 400 error. If one element in the list of movies provided does not correspond to a database entry, returns a 422 error. 
- Authorization: Requires the ```post:actors``` permission to be accessed. 
- Sample: ```curl https://```

#### PATCH '/actors/{actor_id}'
- Modifies one or more entries of actor with ```actor_id``` id: name, age, gender, and list of movies an actor is featured in. Returns success factor (key: ```success```), id of actor updated (key: ```actor_id```, the updated list of actors (key: ```actors_list```), and the total number of actors in the database (```actors_count```).
- Request arguments:
    - actor's id (passed via URL)
    - actor's name
    - actor's age
    - actor's gender
    - [optionally] List of movies (ids of the movies) the actor was featured in.
- If the ```actor_id``` is not found in the database, returns 404. If the actor's name, age or gender are missing, returns 400. If one element onin the list of movies provided does not correspond to a database entry, returns 422.
- Authorization: Requires the ```patch:actors``` permission to be accessed.
- Sample: 

#### PATCH '/movies/{movie_id}'
- Modifies one or more entries of movie with ```movie_id``` id: title, release date, and cast (list of actors which appear in the movie). Returns success factor (key: ```success```), id of movie updated (key: ```movie_id```, the updated list of movies (key: ```movies_list```), and the total number of movies in the database (```movies_count```).
- Request argument contains: the id of the movie (passed via the URL), the movie title and the movie's release date. The list of actors is an optional parameter.
- If no movies are associated with ```movie_id```, returns a 404 error. If the movie title or release date are not submitted, returns a 400 error.  If a list of actors is submitted but any ```actor_id``` contains in the list does not match an entry in the database, returns a 422 error.
- Authorization: Requires the ```patch:movies``` permission to be accessed.
- Sample: 

#### DELETE '/actors/{actor_id}'
- Delete the actor with ```actor_id``` id. Returns the success factor (key: ```success```), id of actor that just got deleted (key: ```actor_id```), the updated movie list (key: ```actors_list```, and the updated movie count (key: ```actors_count```).
- Request arguments:
    - only takes the actor id passed via URL
- If no movies are associated with ```actor_id``` returns 404.
- Authorization: Requires the ```delete:actors``` permission to be accessed. 
- Sample: 


#### DELETE '/movies/{movie_id}'
- Delete the movie with ```movie_id``` id. Returns the success factor (key: ```success```), id of movie that just got deleted (key: ```movie_id```), the updated movie list (key: ```movies_list```, and the updated movie count (key: ```movies_count```).
- Request arguments:
    - only takes the movie id passed via URL
- If no movies are associated with ```movie_id``` returns 404.
- Authorization: Requires the ```delete:movies``` permission to be accessed. 
- Sample: 

### Authorization


### Testing 
To run the tests, run:
```
dropbb casting_agency_test
createdb casting_agency_test
psql casting_agency_test < casting_agency.psql
python3 test_flaskcast.py
```
