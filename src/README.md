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
- Fetches a dictionay with the list of actors (key: 'list_actors') and the number of actors (key: 'actors_count'). Each entry in the list of actor describes an actor with:
    - actor's id
    - actor's name
    - actor's age
    - actor's gender
- Request Arguments: None
- Returns: An object with 2 keys: 'list_actors' and 'actors_count'. 
- Sample: ```curl http://127.0.0.1:5000/actors```

#### GET '/actors/{actor_id}/movies'

#### GET '/movies'

#### GET '/movies/{movie_id}/actors'

#### POST '/add_actor'

#### POST '/add_movie'

#### PATCH '/actors/{actor_id}'

#### PATCH '/movies/{movie_id}'

#### DELETE '/actors/{actor_id}'

#### DELETE '/movies/{movie_id}'

