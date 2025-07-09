let baseUrl = "http://localhost:8000/";

function logout() {
    localStorage.removeItem("token");
    location.reload(); // ricarica la pagina senza il token
}

function login() {
    localStorage.setItem("postLoginRedirect", window.location.pathname);
    window.location.href = "login.html";
}

async function checkLogin() {
    token = localStorage.getItem("token");

    if (!token) {
        return null;
    }
    try {
        const response = await fetch(baseUrl + "api/users/whoami/", {
            method: "GET",
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
            const data = await response.json();
            localStorage.setItem("username", data.message);
            return token;
        }
    } catch (err) {
        return null;
    }
}

async function welcomeUser() {

    const token = await checkLogin();

    if (token) {
        document.getElementById("welcome-message").innerText =
            "Welcome " + localStorage["username"] + "!";
        document.getElementById("authenticated").removeAttribute("hidden");
        document.getElementById("unauthenticated").style.display = "none";
        hiddenElements = document.getElementsByClassName("authenticated-only");
        for (let i = 0; i < hiddenElements.length; i++) {
            hiddenElements[i].removeAttribute("hidden");
        }
    } else {
        document.getElementById("welcome-message").innerText = "Guest user";
        document.getElementById("unauthenticated").removeAttribute("hidden");
        document.getElementById("authenticated").style.display = "none";
    }
}

async function loadPollsOfInterest(elementId) {
    const token = await checkLogin();
    if (!token){
        const noPollsMessage = document.createElement("p");
        noPollsMessage.textContent = "Please log in to see polls of interest.";
        document.getElementById(elementId).appendChild(noPollsMessage);
        return;
    };

    if (token) {
        const response = await fetch(baseUrl + "api/users/interest/", {
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
            console.error("Error retrieving polls of interest: ", data);
        }
    }
}

function loadCategories(elementId) {
    fetch(baseUrl + "api/polls/categories/")
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
            console.error("Error loading categories: ", error);
        });
}

function loadPolls(elementId) {
    const selectedCategory = document.getElementById("category-select").value;
    const pollList = document.getElementById(elementId || "poll-list");
    pollList.innerHTML = ""; // Clear existing polls
    let url = baseUrl + "api/polls/";
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
            console.error("Error retrieving polls: ", error);
        });
}

function renderPolls(data, elementId, action = "details") {
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
        const actionBtn = document.createElement("button");
        actionBtn.className = "btn btn-sm btn-primary";
        // Aggiungi un'azione in base al parametro action
        if (action === "manage") {
            actionBtn.textContent = "Manage";
            actionBtn.onclick = function () {
                window.location.href = `manage_poll.html?id=${poll.id}`;
            }
        }
        else if (action === "details") {
            actionBtn.textContent = "Details";
            actionBtn.onclick = function () {
                window.location.href = `poll_detail.html?id=${poll.id}`;
            };
        }
        actionsCell.appendChild(actionBtn);

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

async function loadPollDetails(){
    const urlParams = new URLSearchParams(window.location.search);
    const pollId = urlParams.get('id');

    document.getElementById('poll-question').innerHTML = 'Loading...';
    document.getElementById('poll-options').innerHTML = ''; // Clear existing options
    document.getElementById('vote-button').hidden = true; // Hide vote button initially
    

    if (!pollId) {
        alert("Poll ID is missing in the URL.");
        return;
    }

    const optionsList = document.getElementById('poll-options');

    const headers = {};

    const token = await checkLogin();
    if (token) {
        headers['Content-Type'] = 'application/json';
        headers['Authorization'] = `Token ${token}`;
    }

    fetch( baseUrl +`api/polls/${pollId}/results/`, {
        method: 'GET',
        headers: headers,
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

            const authenticated = await checkLogin();

            document.getElementById('poll-question').innerText = data.question;
            optionsList.innerHTML = ''; // Clear existing options
            totalVotes = data.choices.reduce((sum, choice) => sum + choice.votes, 0);
            data.choices.forEach(choice => {
                const listItem = document.createElement('li');
                listItem.className = 'list-group-item d-flex align-items-center';
                if (authenticated) {
                    radioButton = document.createElement('input');
                    radioButton.type = 'radio';
                    radioButton.name = 'poll-choice';
                    radioButton.value = choice.id;
                    if(choice.voted)
                        radioButton.checked = true;
                    radioButton.id = `choice-${choice.id}`;
                    listItem.appendChild(radioButton);
                    radioButton.classList.add('me-2');
                    radioButton.dataset.choiceId = choice.id;
                }
                choiceText = document.createElement('span');
                choiceText.textContent = choice.text + " - Votes: " + choice.votes + (totalVotes > 0 ? ` (${((choice.votes / totalVotes) * 100).toFixed(2)}%)` : '');
                listItem.appendChild(choiceText);
                optionsList.appendChild(listItem);
            });
            if(authenticated){
                document.getElementById('vote-button').hidden = false;
                document.getElementById('vote-button').onclick = function() {
                    const selectedChoice = document.querySelector('input[name="poll-choice"]:checked');
                    if (selectedChoice) {
                        const choiceId = selectedChoice.value;
                        submitVote(pollId, choiceId);
                    } else {
                        alert("Please select a choice before voting.");
                    }
                }
            }
            
        })
        .catch(error => {
        });
    
    
}

function submitVote(pollId, choiceId) {
    const token = localStorage.getItem("token") || checkLogin();
    if (!token) {
        alert("You must be logged in to vote.");
        return;
    }

    fetch(baseUrl + "api/polls/vote/${pollId}/", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Token ${token}`,
        },
        body: JSON.stringify({ option_id: choiceId }),
    }).then(response => {
        if (response.ok) {
            alert("Vote submitted successfully!");
            // Reload the poll details to reflect the new vote count
        } else {
            response.json().then(data => {
                alert(data.error);
            });
        }
        loadPollDetails();
    }).catch(error => {
        console.error("Error submitting vote: ", error);
        alert("An error occurred while submitting your vote.");
    });

}

function addOption(value = '', id= null) {
    const container = document.getElementById('optionsContainer');

    const optionDiv = document.createElement('div');
    optionDiv.classList.add('input-group', 'mb-2');
    optionDiv.innerHTML = `
    <input type="text" class="form-control option-input" id="${id}" value="${value}" placeholder="Inserisci un'opzione" required>
    <button type="button" class="btn btn-outline-danger" onclick="removeOption(this)">Rimuovi</button>
    `;

    container.appendChild(optionDiv);
}

function removeOption(button) {
    button.parentElement.remove();
}

async function loadUserPolls(elementId) {

    const token = await checkLogin();
    enforceLogin(token, "You must be logged in to view your polls.");
    const response = await fetch(baseUrl + "api/polls/user-polls/", {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Token ${token}`,
        },
    });

    const data = await response.json();
    
    if(!response.ok) {
        const errorMessage = document.createElement("p");
        errorMessage.textContent = "Error loading polls: " + data.detail;
        document.getElementById(elementId).appendChild(errorMessage);
        return;
    }

    if (data.length === 0) {
        const noPollsMessage = document.createElement("p");
        noPollsMessage.textContent = "No polls found.";
        document.getElementById(elementId).appendChild(noPollsMessage);
        return;
    }

    renderPolls(data, elementId, "manage");

}

function enforceLogin(token, message) {
    if (!token) {
        alert(message);
        login();
    }
}