//Global vars
let username;
let password;
let page = 1;
let has_prev = false;
let has_next = false;
let loginForm = document.querySelector("#loginForm");
let loginSection = document.querySelector(".login-section");
let bookForm = document.querySelector(".add-book-section form");
let mainSection = document.querySelector(".main-section");
let alertSection = document.querySelector(".alert");

//Login
loginForm.onsubmit = function(event) {
    //Prevent page loading
    event.preventDefault();

    //Get user and password
    let formData = new FormData(event.target);
    username = formData.get('username');
    password = formData.get('password');

    //Fetch method
    fetch("http://127.0.0.1:5000/auth", {
        method: "POST",
        headers: {
            'Authorization': 'Basic ' + btoa(username + ":" + password)
        },
        body: formData
    })
    .then(resp => resp.json())
    .then(data => handleLogin(data))
    .catch(error => console.log(error))
};

//Handle login data
function handleLogin(data) {
    if (data.status && data.status !== 200) {
        displayMessage(data.message);
        username = null;
        password = null
    } else {
        //Hide login box and show login panel when logged in
        showAdminPanel();
        getBooks(); //Get books and display
        getAnalytics(); //Get data and draw graph
    }
}

function showAdminPanel() {
    //When logged in -> Hide the form
    loginSection.style.display = "none";
    //And display the main section
    mainSection.style.display = "block"
}

//Display message using the alert div in main
function displayMessage(data) {
    alertSection.style.display = "block";
    alertSection.querySelector("span").textContent = data
}

//Close alert box when clicked
alertSection.querySelector(".close").onclick = function() {
    alertSection.style.display = "none";
};

//Add book
bookForm.onsubmit = function(event) {
    //Prevent redirect
    event.preventDefault();

    //Get form data
    let formData = new FormData(event.target);

    //Send post request
    fetch(`http://127.0.0.1:5000/books/add`, {
        method: "POST",
        headers: {
            'Authorization': 'Basic ' + btoa(username + ":" + password)
        },
        body: formData
    })
    .then(resp => resp.json())
    .then(data => {
        if (data.message) {
            displayMessage(data.message)
        } else {
            displayMessage(`New book added with id ${data.id}`)
        }
    })
    .catch(error => console.log(error))
};

//Request data from server
function getBooks() {
    console.log('Called');
    fetch(`http://127.0.0.1:5000/books/${page}`, {
        method: "GET",
        headers: {
            'Authorization': 'Basic ' + btoa(username + ":" + password)
        }
    })
    .then(resp => resp.json())
    .then(data => displayBook(data))
}


//Display data after requested
function displayBook(data) {
    let ul = mainSection.querySelector(".book-list ul");
    has_next = data.has_next;
    has_prev = data.has_prev;

    //Clear first
    ul.innerHTML = '';

    //Add all books
    data.books.forEach(book => {
        //Create a li element and add
        let li = document.createElement('li');
        li.className = "list-group-item";
        li.textContent = `${book.book_title} - ${book.book_author}`;

        //Create a delete button
        let deleteButton = document.createElement("button");
        deleteButton.textContent = "Delete";
        deleteButton.className = "btn btn-danger float-right mb-2";
        deleteButton.onclick = function() {
            deleteBook(book.book_id)
        };

        //Add
        li.append(deleteButton);
        ul.appendChild(li)
    });

    //Pagination
    if (has_prev) {
        document.querySelector("#previous")
                .className = "page-item active";
        document.querySelector("#previous a")
                .onclick = () => {
                    page -= 1;
                    getBooks()
                }
    } else {
        document.querySelector("#previous")
                .className = "page-item disabled"
    }

    if (has_next) {
        document.querySelector("#next")
                .className = "page-item active";
        document.querySelector("#next a")
                .onclick = () => {
                    page += 1;
                    getBooks()
                }
    } else {
        document.querySelector("#next")
                .className = "page-item disabled"
    }
}

//Delete book
function deleteBook(id) {
    fetch(`http://127.0.0.1:5000/books/delete/${id}`, {
        method: "DELETE",
        headers: {
            'Authorization': 'Basic ' + btoa(username + ":" + password)
        }
    })
        .then(resp => resp.json())
        .then(data => {
            if (data.error) {
                displayMessage("Book has been returned or borrowed -> Can not remove")
            } else {
                displayMessage("Item deleted");
                getBooks()
            }
        })
        .catch(error => displayMessage(error))
}

//Analytics
function getAnalytics() {
    fetch(`http://127.0.0.1:5000/analytics/daily`, {
        method: "GET",
        headers: {
            'Authorization': 'Basic ' + btoa(username + ":" + password)
        }
    })
    .then(resp => resp.json())
    .then(data => drawDailyGraph(data));

    fetch(`http://127.0.0.1:5000/analytics/monthly`, {
        method: "GET",
        headers: {
            'Authorization': 'Basic ' + btoa(username + ":" + password)
        }
    })
    .then(resp => resp.json())
    .then(data => drawMonthlyGraph(data))
}
