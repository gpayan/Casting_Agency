import { displayActors, displayMovies, updateActorData } from './displayContent.js';

const newMovButton = document.querySelector('button[name="add-movie"]');
const newActButton = document.querySelector('button[name="add-actor"]');

const divNewMovie = document.querySelector('.new-movie');
const divNewActor = document.querySelector('.new-actor');

const gendersList = ['male', 'female', 'other']; 

newMovButton.addEventListener('click', () => {
    console.log('I clicked on new movie');
    divNewMovie.classList.toggle('disabled');
});

newActButton.addEventListener('click', () => {
    console.log('I clicked on new actor');
    divNewActor.classList.toggle('disabled');
});

const subMovieButton = document.querySelector('button[name="submit-movie"]');
subMovieButton.addEventListener('click', async (e) => {
    e.preventDefault();
    const movieTitle = document.getElementById('movie-title').value;
    const releaseDate = document.getElementById('release-date').value;

    const responseMovieObj = await fetch('/add_movie', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          title: movieTitle,
          release_date: releaseDate 
        })
    });

    const responseMovie = await responseMovieObj.json();

    if (responseMovie['Success'] == true) {
        window.alert('Movie added to the database');
    }

});


const subActorButton = document.querySelector('button[name="submit-actor"]');
subActorButton.addEventListener('click', async (e) => {
    e.preventDefault();
    const actorName = document.getElementById('actor-name').value;
    const actorAge = document.getElementById('actor-age').value;
    const actorGender = document.getElementById('actor-gender').value;
    const movieStarred = document.getElementById('movie-starred-select');

    const movieAppearances = []
    for (const movOption of movieStarred.options){
        if (movOption.selected){
            movieAppearances.push(movOption.value);
        }
    }
    console.log('movieAppearances is:', movieAppearances);

    const responseActorObj = await fetch('/add_actor', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer' + ' ' + localStorage.getItem('jwt')
        },
        body: JSON.stringify({
            name: actorName,
            age: actorAge,
            gender: actorGender,
            starred_movies: movieAppearances
        })
    });

    const responseActor = await responseActorObj.json();

    if (responseActor['Success'] === true) {
        window.alert('Actor added to the database');
    }

});

window.addEventListener('DOMContentLoaded', async (e) => {
    const divListMovies = document.querySelector('.list-movies');
    const listMoviesObj = await fetch('/movies', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer' + ' ' + localStorage.getItem('jwt')
        }
    });
    const listMovies = await listMoviesObj.json();
    const movies = listMovies['list_movies'];

    displayMovies(movies,divListMovies);

    const deleteMovieButtons = document.querySelectorAll('button[name="delete-movie-button"]');
    for (let i=0; i<deleteMovieButtons.length; i++){
        deleteMovieButtons[i].addEventListener('click', async (e) => {
            const resultMovieObj = await fetch('/movies/' + e.target.dataset.id, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer' + ' ' + localStorage.getItem('jwt')
                }
            });
            console.log('resultObj pour le DELETE is:', resultMovieObj);
            console.log('STATUS OF THE RESPONSE:', resultMovieObj.status);
            const resultMovie = await resultMovieObj.json();
            console.log('On a le resultat du DELETE', resultMovie);
            if (resultMovie['Success'] === true){
                const movieToRemove = document.querySelector('div.movie-details[data-id="' + e.target.dataset.id + '"]');
                movieToRemove.remove();
            }
        });
    }

    const divListActors = document.querySelector('.list-actors');
    const listActorsObj = await fetch('/actors');
    const listActors = await listActorsObj.json();
    const actors = listActors['list_actors'];

    displayActors(actors,divListActors);

    const selectMovieStarred = document.querySelector('#movie-starred-select');
    
    for (const mov of movies){
        const newOption = document.createElement('option');
        newOption.setAttribute('value', mov['id']);
        newOption.innerText = mov['title'];
        selectMovieStarred.append(newOption);
    }

    selectMovieStarred.classList.remove('disabled');
    
    const deleteActorButtons = document.querySelectorAll('button[name="delete-actor-button"]');
    for (let i=0; i < deleteActorButtons.length; i++) {
        deleteActorButtons[i].addEventListener('click', async (e) => {
            const resultActorObj = await fetch('/actors/' + e.target.dataset.id, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer' + ' ' + localStorage.getItem('jwt')
                }
            });
            const resultActor = await resultActorObj.json();
            console.log(resultActor);
            if (resultActor['Success'] === true){
                const actorToRemove = document.querySelector('div.actor-details[data-id="' + e.target.dataset.id + '"]');
                actorToRemove.remove();
            }
        })
    }

    const updateActorButtons = document.querySelectorAll('button[name="update-actor-button"]');
    for (let i=0; i < updateActorButtons.length; i++) {
        updateActorButtons[i].addEventListener('click', async (e) => {

            if (document.querySelector('.update-entry')){

                document.querySelector('.update-entry').remove();
            
            } else {

                const updateActorObj = await fetch('/actors/' + e.target.dataset.id, {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': 'Bearer QQ'
                    }
                });

                const actorData = await updateActorObj.json();
                console.log('We received actorData', actorData);

                const moviesListObj = await fetch('/movies', {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': 'Bearer' + ' ' + localStorage.getItem('jwt') 
                    }
                });

                const moviesList = await moviesListObj.json();

                const divActorId = document.querySelector('div.actor-details[data-id="' + actorData.id +'"]');
                console.log('in Index divActorId', divActorId);
                console.log('GENDERSLIST IS:', gendersList);
                const confirmUpdateButton = updateActorData(actorData, divActorId, moviesList['list_movies'], gendersList);

                confirmUpdateButton.addEventListener('click', async (e) => {
                    
                    const actorUpdatedName = document.getElementById('updated-name').value;
                    const actorUpdatedAge = document.getElementById('updated-age').value;
                    const actorUpdatedGender = document.getElementById('updated-gender').value;
                    const movieStarredUpdated = document.getElementById('movie-starred-select-updated');
                
                    const updatedMovieAppearances = []
                    for (const movOptionUpdated of movieStarredUpdated.options){
                        if (movOptionUpdated.selected){
                            updatedMovieAppearances.push(movOptionUpdated.value);
                        }
                    }
                    
                    const respUpdateObj = await fetch('/actors/' + e.target.dataset.id, {
                        method: 'PATCH',
                        headers: {
                            'Content-Type': 'application/json',
                            'Authorization': 'Bearer' + ' ' + localStorage.getItem('jwt')
                        },
                        body: JSON.stringify({
                            id: e.target.dataset.id,
                            name: actorUpdatedName,
                            age: actorUpdatedAge,
                            gender: actorUpdatedGender,
                            starred_movies:updatedMovieAppearances
                        })
                    });

                    const respUpdate = await respUpdateObj.json();
                    if(respUpdate['Success'] === true){
                        const updateEntryDiv = document.querySelector('.update-entry');
                        updateEntryDiv.remove();
                    }
                })
            }
        });
    }
});


const DOMAIN = 'solate.us.auth0.com';
const CLIENT_ID = 'bqb7RNry9lxj0uxcuxyhNUgSdOw9JTLD';

createAuth0Client({
    domain: DOMAIN,
    client_id: CLIENT_ID,
    //redirect_uri: window.location.origin,
    redirect_uri : "https://127.0.0.1:5000/index",
    cacheLocation: 'localstorage',
    audience: 'castingagency'
}).then(async (auth0) => {
    // Assumes a button with id "login" in the DOM
    const loginButton = document.getElementById("login");

    loginButton.addEventListener("click", (e) => {
        e.preventDefault();                    
        auth0.loginWithRedirect();
    });

    if (location.search.includes("state=") && 
        (location.search.includes("code=") || 
        location.search.includes("error="))) {
            console.log('IM HERE!!!')
            try {
                console.log('starting running the function');
                await auth0.handleRedirectCallback();
                console.log('Just finished running the function');
            } catch(error) {
                console.log('We ran into an error:', error);
            }
            console.log('IM THERE!!!')
            window.history.replaceState({}, document.title, "/");
    }

    // Assumes a button with id "logout" in the DOM
    const logoutButton = document.getElementById("logout");

    logoutButton.addEventListener("click", (e) => {
        e.preventDefault();
        auth0.logout();
    });

    const isAuthenticated = await auth0.isAuthenticated();
    console.log('Printing isAuthenticated');
    console.log(isAuthenticated);
    console.log('HELLO GG');
    const userProfile = await auth0.getUser();

    console.log(userProfile);

    const jwt = await auth0.getTokenSilently();
    console.log('We have jwt');
    console.log(jwt);
    localStorage.setItem('jwt',jwt);

    // Assumes an element with id "profile" in the DOM
    /*
    const profileElement = document.getElementById("profile");

    if (isAuthenticated) {
        profileElement.style.display = "block";
        profileElement.innerHTML = `
                <p>${userProfile.name}</p>
                <img src="${userProfile.picture}" />
            `;
    } else {
        profileElement.style.display = "none";
    }
    */
});
