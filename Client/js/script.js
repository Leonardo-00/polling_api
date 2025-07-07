function logout() {
    console.log("ses");
    localStorage.removeItem("token");
    location.reload(); // ricarica la pagina senza il token
}

function login() {
    localStorage.setItem("postLoginRedirect", window.location.pathname);
    window.location.href = "login.html";
}

async function checkLogin() {
    token = localStorage.getItem("token");
    if (!token) return null;

    try {
        const response = await fetch("http://localhost:8000/whoami/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                Authorization: `Token ${token}`,
            },
        });
        if (!response.ok) {
            localStorage.removeItem("token");
            return null;
        }
        else {
            return token;
        }
    } catch (err) {
        return null;
    }
}

async function welcomeUser() {

    const token = await checkLogin();

    if (token) {
        const response = await fetch("http://localhost:8000/whoami/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                Authorization: `Token ${token}`,
            },
        });
        const data = await response.json();

        if (response.ok) {
            document.getElementById("welcome-message").innerText =
                "Welcome " + data.message + "!";
            document.getElementById("authenticated").removeAttribute("hidden");
            document.getElementById("unauthenticated").style.display = "none";
        document.getElementById("create-poll-link").removeAttribute("hidden");
        }
    } else {
        document.getElementById("welcome-message").innerText = "Guest user";
        document.getElementById("unauthenticated").removeAttribute("hidden");
        document.getElementById("authenticated").style.display = "none";
    }
}

async function loadPollsOfInterest(elementId) {
    const token = localStorage.getItem("token");
    if (!token){
        const noPollsMessage = document.createElement("p");
        noPollsMessage.textContent = "Please log in to see polls of interest.";
        document.getElementById(elementId).appendChild(noPollsMessage);
        return;
    };

    const isLoggedIn = await checkLogin(token);

    if (isLoggedIn) {
        const response = await fetch("http://localhost:8000/api/interest/", {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                Authorization: `Token ${token}`,
            },
        });
        const data = await response.json();

        if (response.ok) {
            if (data.length === 0) {
                const noPollsMessage = document.createElement("p");
                noPollsMessage.textContent = "No poll of interest found.";
                document.getElementById(elementId).appendChild(noPollsMessage);
                return;
            }

            renderPolls(data, elementId);
        } else {
            console.error("Errore nel recupero dei sondaggi di interesse:", data);
        }
    }
}

function loadCategories(elementId) {
    fetch("http://localhost:8000/api/categories/")
        .then((response) => response.json())
        .then((data) => {
            const categoriesList = document.getElementById(elementId);
            data.forEach((category) => {
                const option = document.createElement("option");
                option.value = category.name;
                option.textContent = category.name;
                categoriesList.appendChild(option);
            });
        })
        .catch((error) => {
            console.error("Error loading categories:", error);
        });
}

function loadPolls(elementId) {
    const selectedCategory = document.getElementById("category-select").value;
    const pollList = document.getElementById(elementId || "poll-list");
    pollList.innerHTML = ""; // Clear existing polls
    let url = "http://localhost:8000/api/polls/";
    if (selectedCategory) {
        url += `?category=${encodeURIComponent(selectedCategory)}`;
    }
    fetch(url, {
            method: "GET",
        })
        .then((response) => response.json())
        .then((data) => {
            if (data.length === 0) {
                const noPollsMessage = document.createElement("p");
                noPollsMessage.textContent = "Nessun sondaggio trovato.";
                pollList.appendChild(noPollsMessage);
                return;
            }
            renderPolls(data, elementId);
        })
        .catch((error) => {
            console.error("Errore nel recupero dei sondaggi:", error);
        });
}

function renderPolls(data, elementId) {
    const container = document.getElementById(elementId);
    container.innerHTML = ""; // svuota il contenuto precedente

    // crea la tabella
    const table = document.createElement("table");
    table.className = "table table-striped";

    // crea l'intestazione
    const thead = document.createElement("thead");
    const headerRow = document.createElement("tr");
    const headers = ["Question", "Category", "Created by", "Date of creation", ""];
    headers.forEach(text => {
        const th = document.createElement("th");
        th.textContent = text;
        headerRow.appendChild(th);
    });
    thead.appendChild(headerRow);
    table.appendChild(thead);

    // crea il corpo
    const tbody = document.createElement("tbody");

    data.forEach(poll => {
        const row = document.createElement("tr");

        const questionCell = document.createElement("td");
        questionCell.textContent = poll.question;

        const categoryCell = document.createElement("td");
        categoryCell.textContent = poll.category || "-";

        const ownerCell = document.createElement("td");
        ownerCell.textContent = poll.created_by_username;

        const dateCell = document.createElement("td");
        const pollDate = new Date(poll.created_at);
        dateCell.textContent =
            pollDate.toLocaleDateString() + " " + pollDate.toLocaleTimeString();

        const actionsCell = document.createElement("td");
        const detailsBtn = document.createElement("button");
        detailsBtn.className = "btn btn-sm btn-primary";
        detailsBtn.textContent = "Details";
        detailsBtn.onclick = function () {
            window.location.href = `poll_detail.html?id=${poll.id}`;
        };
        actionsCell.appendChild(detailsBtn);

        row.appendChild(questionCell);
        row.appendChild(categoryCell);
        row.appendChild(ownerCell);
        row.appendChild(dateCell);
        row.appendChild(actionsCell);

        tbody.appendChild(row);
    });

    table.appendChild(tbody);
    container.appendChild(table);
}


function loadPollDetails(){
    const urlParams = new URLSearchParams(window.location.search);
    const pollId = urlParams.get('id');

    if (!pollId) {
        alert("Poll ID is missing in the URL.");
        return;
    }

    fetch(`http://localhost:8000/api/polls/${pollId}/`, {
        method: 'GET',
    })
        .then(async response => {
            if (response.status === 404) {
                const errorMessage = document.createElement('p');
                errorMessage.textContent = "No poll with ID: " + pollId + " found.";
                document.getElementById('poll-details').innerHTML = ''; // Clear existing content
                document.getElementById('poll-details').appendChild(errorMessage);
                return;
            }
            const data = await response.json();

            document.getElementById('poll-question').innerText = data.question;
            const optionsList = document.getElementById('poll-options');
            optionsList.innerHTML = ''; // Clear existing options
            data.choices.forEach(choice => {
                const listItem = document.createElement('li');
                listItem.textContent = choice.text;
                optionsList.appendChild(listItem);
            });
            document.getElementById("vote-button").hidden = false; // Show the vote button
        })
        .catch(error => {
        });
}

function addOption(value = '') {
    const container = document.getElementById('optionsContainer');

    const optionDiv = document.createElement('div');
    optionDiv.classList.add('input-group', 'mb-2');
    optionDiv.innerHTML = `
    <input type="text" class="form-control option-input" value="${value}" placeholder="Inserisci un'opzione" required>
    <button type="button" class="btn btn-outline-danger" onclick="removeOption(this)">Rimuovi</button>
    `;

    container.appendChild(optionDiv);
}

function removeOption(button) {
    button.parentElement.remove();
}