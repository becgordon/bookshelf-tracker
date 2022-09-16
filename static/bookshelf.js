'use strict';

const addBookButton = document.querySelector('#add_book');

function addBook() {
    window.location = `/addbook/${document.querySelector('#volume_id').attributes.name.value}`
    addBookButton.innerHTML = 'Book added';
}

addBookButton.addEventListener('click', addBook);

const logOutButton = document.querySelector('#log_out');

function logOut() {
    // fetch('/logout');
    console.log('touched')
    window.location = '/logout'
}

logOutButton.addEventListener('click', logOut);