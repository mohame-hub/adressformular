// Fetches address data from the Vienna address service
async function fetchAdressData(query) {
    const url = `https://data.wien.gv.at/daten/OGDAddressService.svc/GetAddressInfo?Address=${query}`;
    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error('Fehler beim Abrufen der Straßen.');
        }
        const data = await response.json();
        return data;  // Return the fetched data
    } catch (error) {
        console.error('Error fetching address data:', error);
        showError('Fehler beim Abrufen der Straßen: ' + error.message);
        return null;
    }
}

// Displays the fetched suggestions under the input field
function displaySuggestions(data, suggestionsDiv, handleSelection) {
    suggestionsDiv.innerHTML = '';  // Clear previous suggestions

    if (data && data.features && data.features.length > 0) {
        data.features.forEach(ort => {
            const suggestionItem = document.createElement('div');
            suggestionItem.classList.add('suggestion-item');
            suggestionItem.textContent = ort.properties.Adresse;
            suggestionItem.onclick = () => handleSelection(ort.properties.Adresse);
            suggestionsDiv.appendChild(suggestionItem);
        });
    } else {
        suggestionsDiv.innerHTML = '<div>Keine Vorschläge gefunden</div>';
    }
}

// Handles user input for street and calls fetchAdressData
async function handleStreetInput(event, suggestionsDiv, handleSelection) {
    const query = event.target.value;

    if (query.length >= 3) {
        const data = await fetchAdressData(query);
        if (data) {
            displaySuggestions(data, suggestionsDiv, handleSelection);
        }
    } else {
        suggestionsDiv.innerHTML = '';  // Clear suggestions if input is too short
    }
}

// Handles user input for the "Ort" field and provides suggestions based on a static list
function handleOrtInput(event, suggestionsDiv, handleSelection) {
    const query = event.target.value.toLowerCase();
    const bundeslaender = ['Wien', 'Niederösterreich', 'Oberösterreich', 'Salzburg', 'Tirol', 'Steiermark', 'Burgenland', 'Kärnten'];
    const filtered = bundeslaender.filter(bundesland => bundesland.toLowerCase().startsWith(query));

    suggestionsDiv.innerHTML = '';  // Clear previous suggestions

    if (filtered.length > 0) {
        filtered.forEach(bundesland => {
            const suggestionItem = document.createElement('div');
            suggestionItem.classList.add('suggestion-item');
            suggestionItem.textContent = bundesland;
            suggestionItem.onclick = () => handleSelection(bundesland);
            suggestionsDiv.appendChild(suggestionItem);
        });
    } else {
        suggestionsDiv.innerHTML = '<div>Keine Vorschläge gefunden</div>';
    }
}

// Fills the form with the selected suggestion
function selectSuggestion(suggestion, inputField, suggestionsDiv) {
    inputField.value = suggestion;  // Set the input field value
    suggestionsDiv.innerHTML = '';  // Clear suggestions after selection
}

function showError(message) {
    const errorDiv = document.getElementById('error-message');
    errorDiv.innerHTML = message;
    errorDiv.style.display = 'block';
}

