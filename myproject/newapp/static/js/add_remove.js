
       
        

// Modified showAnnotators function to use fetchAnnotators
function showAnnotators() {
    var language = document.getElementById('language-dropdown').value;
    if (language) {
        fetch(`/newapp/get_annotators/${language}`)
            .then(response => response.json())
            .then(data => {
                updateAnnotatorContainer(data, language);
            })
            .catch(error => console.error('Error fetching annotators:', error));
    } else {
        document.getElementById('annotator-container').innerHTML = '';
    }
}

function fetchAnnotators(language) {
    fetch(`/newapp/get_annotators/${language}`)
        .then(response => response.json())
        .then(data => {
            updateAnnotatorContainer(data , language);
        })
        .catch(error => console.error('Error fetching annotators:', error));
}
function updateAnnotatorContainer(annotators, language) {
    console.log("Updating container for language:", language);

    var annotatorContainer = document.getElementById('annotator-container');
    annotatorContainer.innerHTML = ''; // Clear existing annotators

    if (Array.isArray(annotators) && annotators.length > 0) {
        annotators.forEach(annotator => {
            var div = document.createElement('div');
            div.textContent = annotator.username; // Assuming the annotator object has a 'name' property
            div.className = 'draggable';
            div.setAttribute('draggable', true);
            div.setAttribute('ondragstart', 'drag(event)');
            div.setAttribute('data-language', language); // Set the language as a data attribute
            annotatorContainer.appendChild(div);
        });
    } else {
        var messageDiv = document.createElement('div');
        messageDiv.textContent = annotators.message || "No annotators available for this language.";
        messageDiv.style.color = 'red'; // You can customize the style
        annotatorContainer.appendChild(messageDiv);
    }
}




/* var annotators = {
    "English": ['rohit', 'suraj', 'Amar'],
    "Hindi": ['Yugandhar', 'Abhinav', 'Souvik'],
    "Kannada": ['Sanket', 'Suman'],
    "Malayalam": ['Anto', 'Rohit'],
    "Marathi": ['Yugandhar', 'Ninad'],
    "Bengali": ['Santanu', 'Arghadeep', 'Souvik'],
    "Tamil": ['Anto', 'Arun', 'Govind'],
    // Add more languages and annotators here
};

function showAnnotators() {
    var language = document.getElementById('language-dropdown').value;
    var annotatorContainer = document.getElementById('annotator-container');
    annotatorContainer.innerHTML = ''; // Clear current list

    if (annotators[language]) {
        annotators[language].forEach(function(annotator) {
            var div = document.createElement('div');
            div.textContent = annotator;
            div.setAttribute('draggable', true);
            div.setAttribute('ondragstart', 'drag(event)');
            div.className = 'draggable';
            div.setAttribute('data-language', language); // Set the language as a data attribute
            annotatorContainer.appendChild(div);
        });
    }
}*/
function drag(event) {
    var annotatorName = event.target.textContent;
    event.dataTransfer.setData('text/plain', event.target.textContent);
    var language = event.target.getAttribute('data-language');
    event.dataTransfer.setData('language', language);
    console.log("Dragging: ", event.target.textContent, " Language: ", language);
}


function handleAnnotatorClick(event, annotatorElement, language) {
    var confirmation = confirm("Do you want to deselect this annotator?");
    if (confirmation) {
        annotatorElement.remove(); // Remove the annotator element
    }
}


function allowDrop(event) {
    event.preventDefault();
    if(!event.target.classList.contains('dropped')) {
        event.target.classList.add('over');
    }
}



// ... existing JavaScript ...

function drop(event, language) {
        event.preventDefault();
        var dropLanguage = event.dataTransfer.getData('language');
        var data = event.dataTransfer.getData('text/plain');
        console.log('Dropped language:', dropLanguage, 'Target container language:', language);

        if (language === dropLanguage) {
            var assignedContainer = document.getElementById(`${language}`);
            if (!assignedContainer.textContent.includes(data)) {
                var div = document.createElement('div');
                div.textContent = data;
                div.className = 'dropped';
                div.addEventListener('click', function() {
                    if (confirm('Do you want to remove this annotator?')) {
                        div.remove(); // Remove the annotator from the assigned list
                    }
                });
                assignedContainer.appendChild(div);
            } else {
                alert('This annotator is already assigned.');
            }
        } else {
            alert('You can only assign annotators to their respective language section.');
        }
        event.target.classList.remove('over');
    }

            
    function handleAssignedAnnotatorClick(event, annotatorElement, language) {
        var confirmation = confirm("Do you want to remove this annotator?");
        if (confirmation) {
            // Remove the annotator from the UI
            annotatorElement.remove();

            // Create a dictionary to group annotators by language
            var annotatorsByLanguage = {};
            annotatorsByLanguage[language] = annotatorsByLanguage[language] || [];
            annotatorsByLanguage[language].push(annotatorElement.textContent);

            // Send a request to the server to save or remove the annotators
            fetch('/newapp/save_selected_annotators/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': document.querySelector('meta[name="csrf-token"]').getAttribute('content')
                },
                body: JSON.stringify({
                    selected_annotators: annotatorsByLanguage
                })
            })
            .then(response => response.json())
            .then(data => {
                console.log(data.message); // Handle the server's response as needed
            })
            .catch(error => console.error('Error saving or removing annotator:', error));
        }
    }

    // This function add the annotators back to the annotators list after removing it from the language container 
        
    function addToAvailableAnnotators(annotatorName, language) {
        var annotatorContainer = document.getElementById('annotator-container');
        var div = document.createElement('div');
        div.textContent = annotatorName;
        div.setAttribute('draggable', true);
        div.setAttribute('ondragstart', 'drag(event)');
        div.className = 'draggable';
        div.setAttribute('data-language', language);
        
        // Find the appropriate container for the language
        var languageContainer = document.getElementById(language);
        if (languageContainer) {
            // Append the div to the language-specific available annotators container
            languageContainer.appendChild(div);
        } else {
            // If the language container doesn't exist, append to the general annotator container
            annotatorContainer.appendChild(div);
        }
    }

            
    function saveSelectedAnnotators() {
        var selectedAnnotatorUsernames = [];

        // Collect the IDs of selected annotators and the language container id
        var selectedAnnotatorElements = document.querySelectorAll('.dropped');
        selectedAnnotatorElements.forEach(function(element) {
            var languageContainerId = element.parentElement.id;  // Get the language container id
            selectedAnnotatorUsernames.push({
                username: element.textContent,
                language: languageContainerId
            });
        });

        console.log('Selected Annotators:', selectedAnnotatorUsernames);

        // Send the selected annotator IDs to the server
        fetch('/newapp/save_selected_annotators/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('meta[name="csrf-token"]').getAttribute('content')
            },
            body: JSON.stringify({
                selected_annotators: selectedAnnotatorUsernames
            })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log(data.message);
            // Handle success here if needed
        })
        .catch(error => {
            console.error('Error saving selected annotators:', error);
            // Handle error here, you can log the error or show a user-friendly message
        });
    }



            
            
            
            










document.addEventListener("DOMContentLoaded", function() {
    // Define an array of languages
    var languages = ['English', 'Hindi', 'Telugu', 'Tamil', 'Kannada', 'Malayalam', 'Marathi', 'Gujarati', 'Bengali', 'Punjabi', 'Odia', 'Assamese'];

    // Fetch and display assigned annotators for each language
    languages.forEach(function(language) {
        fetchAssignedAnnotators(language);
    });
});

function fetchAssignedAnnotators(language) {
    // Fetch the assigned annotators for the given language from the server
    fetch(`/newapp/get_assigned_annotators/${language}`)
        .then(response => response.json())
        .then(data => {
            // Update the assigned annotators container for the specified language
            updateAssignedAnnotatorContainer(data, language);
        })
        .catch(error => console.error(`Error fetching assigned annotators for ${language}:`, error));
}

function updateAssignedAnnotatorContainer(assignedAnnotators, language) {
    console.log(`Updating assigned annotators container for ${language}`);
    console.log('Received data:', assignedAnnotators);

    var assignedContainer = document.getElementById(`${language}`);
    assignedContainer.innerHTML = ''; // Clear existing assigned annotators

    if (Array.isArray(assignedAnnotators.selected_annotators) && assignedAnnotators.selected_annotators.length > 0) {
        assignedAnnotators.selected_annotators.forEach(annotator => {
            var div = document.createElement('div');
            div.textContent = annotator; // Use 'annotator' directly
            div.className = 'dropped';
            div.addEventListener('click', function () {
                handleAssignedAnnotatorClick(event, div, language);
            });
            assignedContainer.appendChild(div);
        });
    } else {
        // Handle case when no annotators are assigned (e.g., display a message or leave the container empty)
        // For example, you could add a message:
        var messageDiv = document.createElement('div');
        messageDiv.textContent = 'No annotators assigned.';
        assignedContainer.appendChild(messageDiv);
    }
}




