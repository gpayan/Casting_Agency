export function displayMovies(list_movies, divElement){
    for(const movie of list_movies){
        const newDiv = document.createElement('div');
        newDiv.classList.add('movie-details');
        newDiv.setAttribute('data-id', movie['id']);

        const deleteButton = document.createElement('button');
        deleteButton.setAttribute('name','delete-movie-button');
        deleteButton.setAttribute('data-id', movie['id']);
        deleteButton.innerText = 'Delete Movie';

        const updateButton = document.createElement('button');
        updateButton.setAttribute('name', 'update-movie-button');
        updateButton.setAttribute('data-id', movie['id']);
        updateButton.innerText = 'Update Movie';

        newDiv.innerText = movie['title'] + ' coming out on: ' + movie['release_date'];
        newDiv.append(updateButton);
        newDiv.append(deleteButton);

        divElement.append(newDiv);
    }
}

export function displayActors(list_actors, divElement){
    for (const actor of list_actors){
        const newDiv = document.createElement('div');
        newDiv.classList.add('actor-details');
        newDiv.setAttribute('data-id', actor['id']);

        const deleteButton = document.createElement('button');
        deleteButton.setAttribute('name','delete-actor-button');
        deleteButton.setAttribute('data-id', actor['id']);
        deleteButton.innerText = 'Delete Actor';

        const updateButton = document.createElement('button');
        updateButton.setAttribute('name', 'update-actor-button');
        updateButton.setAttribute('data-id', actor['id']);
        updateButton.innerText = 'Update Actor';

        newDiv.innerText = actor['name'] + ' : ' + actor['age'] + ' ' + actor['gender'];
        newDiv.append(updateButton);
        newDiv.append(deleteButton);

        divElement.append(newDiv);
    }
}

export function updateActorData(actorData, divActorId, moviesList, gendersList){

    console.log('In updateActorData:', gendersList);
    console.log(actorData);

    const newDivForm = document.createElement('div');
    newDivForm.classList.add('update-entry');
    console.log('divActorId', divActorId);
    
    const nameInput = document.createElement('input');
    nameInput.setAttribute('type', 'text');
    nameInput.setAttribute('id', 'updated-name');
    nameInput.setAttribute('name', 'updated-name');
    nameInput.value = actorData.name;
    newDivForm.append(nameInput);

    const ageInput = document.createElement('input');
    ageInput.setAttribute('number', 'text');
    ageInput.setAttribute('id', 'updated-age');
    ageInput.setAttribute('name', 'updated-age');
    ageInput.value = actorData.age;
    newDivForm.append(ageInput);

    const genderInput = document.createElement('select');
    genderInput.setAttribute('id', 'updated-gender');
    genderInput.setAttribute('name', 'updated-gender');
    for (let gender of gendersList) {
        const newOption = document.createElement('option');
        newOption.setAttribute('value', gender);
        newOption.innerText = gender;
        if (gender == actorData.gender) {
            newOption.selected = true;
        }
        genderInput.append(newOption);
    }
    newDivForm.append(genderInput);
    
    const moviesInput = document.createElement('select');
    moviesInput.setAttribute('id', 'movie-starred-select-updated');
    moviesInput.multiple = true;
    for (let movie of moviesList) {
        const optionMov = document.createElement('option');
        optionMov.setAttribute('value', movie.id);
        optionMov.innerText = movie.title;
        if (actorData.starred_movies.includes(movie.id)){
            optionMov.selected = true;
        }
        moviesInput.append(optionMov);
    }
    newDivForm.append(moviesInput);

    const updateButton = document.createElement('button');
    updateButton.setAttribute('name', 'confirm-update');
    updateButton.setAttribute('data-id', actorData.id);
    updateButton.innerText = 'Update actor entry';
    newDivForm.append(updateButton);

    divActorId.append(newDivForm);
    console.log('newDivForm', newDivForm);

    return updateButton;
}