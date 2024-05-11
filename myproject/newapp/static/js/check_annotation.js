const annotations = {};
        const languageSelect = document.getElementById('languageSelect');
        let selectedLanguage = ''; // Initialize with an empty string

        // Add an event listener to the language dropdown to update the selectedLanguage variable
        languageSelect.addEventListener('change', function () {
            selectedLanguage = languageSelect.value;
            if (selectedLanguage) {
                fetch(`/newapp/get_annotation_data/${selectedLanguage}/`)
                    .then(response => response.json())
                    .then(data => {
                        const { annotators, images, data: annotationData } = data;
        
                        // Now you can use the fetched data to update your JavaScript variables
                        annotations[selectedLanguage] = {
                            annotators,
                            images,
                            data: annotationData,
                        };
                        console.log(annotations);
        
                        // Call a function to update your UI or perform any other actions with the fetched data
                        const annotationIds = Object.values(annotationData).flatMap(userAnnotations => userAnnotations.map(annotation => annotation.id));
                        console.log(annotationIds);
                        updateUI();
                        loadAnnotations();
                        resetAll();
                    })
                    .catch(error => console.error('Error fetching data:', error));
            }
        });
        

        // Function to update UI based on the selected language
        function updateUI() {
            // Implement your logic to update the UI based on the fetched data for the selected language
            console.log(`Update UI for ${selectedLanguage}`);
        }
        

    //const languageSelect = document.getElementById('languageSelect');
        languageSelect.addEventListener('change', () => {
        resetAll();  // Reset all before loading annotations for the selected language
        loadAnnotations();
    });

    document.getElementById('searchInput').addEventListener('keyup', filterList);

    function toggleListDisplay(selectionType) {
        const annotatorSection = document.getElementById('annotatorSection');
        const imageSection = document.getElementById('imageSection');
        // Make sure these IDs exist in your HTML and are unique
        if (selectionType === 'annotator') {
            annotatorSection.style.display = 'block';
            imageSection.style.display = 'none';
        } else {
            annotatorSection.style.display = 'none';
            imageSection.style.display = 'block';
        }
    }
    
    function toggleTableVisibility(tableToShow) {
        const userAnnotationsTable = document.getElementById('userAnnotations');
        const imageAnnotationsTable = document.getElementById('imageAnnotations');
    
        if (tableToShow === 'userAnnotations') {
            userAnnotationsTable.style.display = 'block';
            imageAnnotationsTable.style.display = 'none';
        } else if (tableToShow === 'imageAnnotations') {
            userAnnotationsTable.style.display = 'none';
            imageAnnotationsTable.style.display = 'block';
        }
    }
    
    // Example usage:
    // Call this function when you want to toggle to the userAnnotations table
   
    
    // Call this function when you want to toggle to the imageAnnotations table
    
    
    
    
    

    function resetAll() {
        var userAnnotations = document.getElementById('userAnnotations');
        var downloadUserAnnotations = document.getElementById('downloadUserAnnotations');
        var imageAnnotations = document.getElementById('imageAnnotations');
        var downloadImageAnnotations = document.getElementById('downloadImageAnnotations');
    
        if (userAnnotations) userAnnotations.style.display = 'none';
        if (downloadUserAnnotations) downloadUserAnnotations.style.display = 'none';
        if (imageAnnotations) imageAnnotations.style.display = 'none';
        if (downloadImageAnnotations) downloadImageAnnotations.style.display = 'none';
    }
    function filterList() {
        const searchValue = document.getElementById('searchInput').value.toLowerCase();
        const items = document.querySelectorAll('.section ul li');
        items.forEach(item => {
            if (item.textContent.toLowerCase().indexOf(searchValue) > -1) {
                item.style.display = '';
            } else {
                item.style.display = 'none';
            }
        });
    }



    function populateAnnotatorList(annotators) {
        const annotatorList = document.getElementById('annotatorList');
        annotatorList.innerHTML = ''; // Clear any existing list items
    
        annotators.forEach(annotator => {
            let li = document.createElement('li');
            li.textContent = annotator; // If 'annotator' is just a string
            // If 'annotator' is an object, use `annotator.name` or the appropriate property
    
            li.addEventListener('click', function() {
                displayUserAnnotations(language, annotator); // Make sure to use the correct language variable
            });
    
            annotatorList.appendChild(li);
        });
    }
    

    function showSelection(selectionType) {
        if (selectionType === 'annotator') {
            // Logic to load and display the list of annotators
            loadAnnotators();
        } else if (selectionType === 'image') {
            // Logic to load and display the image gallery
            loadImageGallery();
        }
    }

    let isFirstLoad = true;
    function loadAnnotations() {
        const selectedLanguage = languageSelect.value;
        if (!annotations[selectedLanguage]) {
            if (!isFirstLoad) { // Only show the alert if it's not the first load
                alert('No data available for selected language');
            }
            return;
        }

        isFirstLoad = false;
            
        // Load annotators
        const annotatorList = document.getElementById('annotatorList');
        annotatorList.innerHTML = ''; // Clear existing
        annotations[selectedLanguage].annotators.forEach(user => {
            let li = document.createElement('li');
            li.textContent = user;
            li.onclick = function() {
                displayUserAnnotations(selectedLanguage, user);
            };
            annotatorList.appendChild(li);
        });
    
        // Load images
        const imageSection = document.getElementById('imageSection');
    imageSection.innerHTML = ''; // Clear existing
    annotations[selectedLanguage].images.forEach(imgSrc => {
        let img = document.createElement('img');
        img.src = imgSrc;
        img.alt = "Demo Image";
        img.className = 'demo-image';
        img.onclick = function() {
            displayImageAnnotations(selectedLanguage, img.src);
        };
        imageSection.appendChild(img); // Append the image directly to the imageSection
    });
    }
    
    function displayUserAnnotations(language, user) {
        const table = document.getElementById('userAnnotations');
        if (!table) {
            console.error('Table #userAnnotations not found.');
            return; // Exit the function if the table isn't found
        }
    
        // Clear the table body
        const tbody = table.querySelector('tbody');
        tbody.innerHTML = ''; // Clear any existing rows
    
        annotations[language].data[user].forEach(annotation => {
            let tr = document.createElement('tr'); // Use tr directly
            tr.className = annotation.validated ? 'validated' : 'not-validated';
    
            let imgTd = document.createElement('td');
            let img = document.createElement('img');
            img.src = annotation.img;
            img.className = 'demo-image';
            img.alt = 'Annotation Image';
            imgTd.appendChild(img);
            tr.appendChild(imgTd);
    
            let annotationTd = document.createElement('td');
            annotationTd.textContent = annotation.annotation;
            tr.appendChild(annotationTd);
    
            // Checkbox for validation status
            let validatedCell = document.createElement('td');
            let checkbox = document.createElement('input');
            checkbox.type = 'checkbox';
            checkbox.checked = annotation.validated;
            checkbox.addEventListener('change', (event) => {
                const isChecked = event.target.checked;
                if(isChecked) {
                    validateAnnotation(annotation.id);
                } else {
                    unvalidateAnnotation(annotation.id);
                }
            });
            validatedCell.appendChild(checkbox);
            tr.appendChild(validatedCell); // Correctly append to tr
    
            tbody.appendChild(tr); // Append tr to tbody
        });
    
        // Display the table
        table.style.display = 'block'; 
        toggleTableVisibility('userAnnotations');
    }
    
    
    
    function displayImageAnnotations(language, imgSrc) {
        const table = document.getElementById('imageAnnotations');
        if (!table) {
            console.error('Table #imageAnnotations not found.');
            return; // Exit the function if the table isn't found
        }
    
        // Clear the table body
        const tbody = table.querySelector('tbody');
        tbody.innerHTML = ''; // Clear any existing rows
    
        // Fetch the image annotations based on the selected image
        for (let user in annotations[language].data) {
            annotations[language].data[user].forEach(annotation => {
                // Check if the annotation has the 'img' property
                if (annotation.img) {
                    // Convert both paths to relative paths for comparison
                    const relativeImgSrc = imgSrc.replace(/^.*[\\\/]/, '');
                    const relativeAnnotationImg = annotation.img.replace(/^.*[\\\/]/, '');
    
                    if (relativeImgSrc === relativeAnnotationImg) {
                        let tr = document.createElement('tr');
                        tr.className = annotation.validated ? 'validated' : 'not-validated';
    
                        // Display the user's name in the first column
                        let userTd = document.createElement('td');
                        userTd.textContent = user;
                        tr.appendChild(userTd);
    
                        // Annotation text
                        let annotationTd = document.createElement('td');
                        annotationTd.textContent = annotation.annotation;
                        tr.appendChild(annotationTd);
    
                        // Checkbox for validation status
                        let validatedCell = document.createElement('td');
                        let checkbox = document.createElement('input');
                        checkbox.type = 'checkbox';
                        checkbox.checked = annotation.validated;
                        checkbox.addEventListener('change', (event) => {
                            const isChecked = event.target.checked;
                            if (isChecked) {
                                validateAnnotation(annotation.id);
                            } else {
                                unvalidateAnnotation(annotation.id);
                            }
                        });
                        validatedCell.appendChild(checkbox);
                        tr.appendChild(validatedCell);
    
                        tbody.appendChild(tr);
                    }
                } else {
                    console.warn('Annotation is missing the "img" property:', annotation);
                    // Handle the case where 'img' property is missing (e.g., skip this annotation)
                }
            });
        }
    
        // Display the table
        table.style.display = 'block';
        toggleTableVisibility('imageAnnotations');
    }
    
    
    
    
    
    
    
    

    function downloadCSV(tableId, filename) {
        const table = document.getElementById(tableId);
        const rows = table.querySelectorAll("tr");
        let csv = [];
    
        for(let i = 0; i < rows.length; i++) {
            const row = [], cols = rows[i].querySelectorAll("td, th");
            
            for(let j = 0; j < cols.length; j++) {
                let data = cols[j].innerText.replace(/"/g, '""'); // Escape double quotes
                data = '"' + data + '"'; // Quote each entry
                row.push(data);
            }
    
            csv.push(row.join(","));
        }
    
        const csvString = csv.join("\n");
        const blob = new Blob([csvString], { type: "text/csv" });
        const url = URL.createObjectURL(blob);
        const link = document.createElement("a");
    
        link.href = url;
        link.download = filename;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }

    function downloadMultipleAnnotations() {
        // Collect all selected user IDs and image IDs
        let selectedUsers = [...document.getElementById("annotatorList").selectedOptions].map(opt => opt.value);
        let selectedImages = [...document.getElementById("imageList").selectedOptions].map(opt => opt.value);
    
        // Fetch and combine annotations for all selected users and images
        let combinedAnnotations = [];
    
        for(let userId of selectedUsers) {
            // Fetch annotations for the user
            let userAnnotations = getUserAnnotationsById(userId); // You would need to implement this or similar function
            combinedAnnotations.push(...userAnnotations);
        }
    
        for(let imageId of selectedImages) {
            // Fetch annotations for the image
            let imageAnnotations = getImageAnnotationsById(imageId); // You would need to implement this or similar function
            combinedAnnotations.push(...imageAnnotations);
        }
    
        // Convert combinedAnnotations to CSV and download
        downloadAnnotationsAsCSV(combinedAnnotations, 'combined_annotations.csv');
    }
    function slide(direction) {
    var container = document.getElementById('sliderContainer');
    scrollCompleted = 0;
    var slideVar = setInterval(function(){
        if(direction == 'left') {
            container.scrollLeft -= 10;
        } else {
            container.scrollLeft += 10;
        }
        scrollCompleted += 10;
        if(scrollCompleted >= 100) {
            window.clearInterval(slideVar);
        }
    }, 50);
    }

    function loadUsersForLanguage(language) {
        // Fetch users for the given language and populate the annotatorList with checkboxes
        let users = getUsersForLanguage(language); // This function should return a list of users for the given language
    
        let userListElement = document.getElementById('annotatorList');
        userListElement.innerHTML = '';
        
        for (let user of users) {
            let listItem = document.createElement('li');
            let checkbox = document.createElement('input');
            checkbox.type = 'checkbox';
            checkbox.value = user.id;
            checkbox.id = 'user_' + user.id;
            
            let label = document.createElement('label');
            label.htmlFor = checkbox.id;
            label.textContent = user.name;
    
            listItem.appendChild(checkbox);
            listItem.appendChild(label);
            userListElement.appendChild(listItem);
        }
    
        // Show the download button
        document.getElementById('downloadUserAnnotations').style.display = 'block';
    }
    
    function loadImagesForLanguage(language) {
        // Similar function to load images for the given language and populate imageList with checkboxes
        //...
        // Show the download button
        document.getElementById('downloadImageAnnotations').style.display = 'block';
    }

    // Initial load
    loadAnnotations();

    function fetchAnnotatorsForLanguage(languageName) {
        fetch(`/get-annotators-for-language?language_name=${languageName}`)
        .then(response => response.json())
        .then(data => {
            const annotatorsList = document.getElementById('annotatorList');
            annotatorsList.innerHTML = ''; // Clear existing list
            data.annotators.forEach(annotator => {
                const li = document.createElement('li');
                li.textContent = annotator.username;
                li.setAttribute('data-annotator-id', annotator.id);
                li.addEventListener('click', () => {
                    fetchAnnotationsByAnnotator(annotator.id);
                });
                annotatorsList.appendChild(li);
                
            });
        });
    }

    function fetchAnnotationsByAnnotator(annotatorId) {
        fetch(`/get-annotations-by-annotator/${annotatorId}`)
        .then(response => response.json())
        .then(data => {
            // Use `data` to update your front-end
            // This could involve displaying the images and annotations in the format you've set up in your HTML
        });
    }
    
        // Add an event listener to the download all button
    document.getElementById('downloadAllButton').addEventListener('click', function() {
        // Call the function to download all annotations for the selected language
        downloadAllAnnotations();
    });

    // Function to download all annotations for the selected language
    function downloadAllAnnotations() {
        const selectedLanguage = languageSelect.value; // Assuming languageSelect is your language dropdown

        // Check if a language is selected
        if (!selectedLanguage) {
            alert('Please select a language first.');
            return;
        }

        // Fetch annotations for the selected language
        fetch(`/newapp/get_annotation_data/${selectedLanguage}/`)
            .then(response => response.json())
            .then(data => {
                const { annotators, images, data: annotationData } = data;
        
                // Combine all annotations for the selected language into a single array
                const allAnnotations = [].concat(...Object.values(annotationData).map(arr => arr));
        
                // Create a CSV string from the combined annotations
                const csvContent = allAnnotations.map(annotation => {
                    // Enclose annotation within double quotes to handle commas correctly
                    const annotatedImage = `"${annotation.img}","${annotation.annotation}"`;
                    return annotatedImage;
                }).join('\n');
        
                // Create a Blob and create a link to trigger the download
                const blob = new Blob([csvContent], { type: 'text/csv' });
                const link = document.createElement('a');
                link.href = window.URL.createObjectURL(blob);
                link.download = `all_${selectedLanguage}_annotations.csv`;
        
                // Append the link to the document and trigger the click event
                document.body.appendChild(link);
                link.click();
        
                // Remove the link from the document
                document.body.removeChild(link);
            })
            .catch(error => console.error('Error fetching data:', error));
    
        }


    
    
    

    // Function to retrieve CSRF token from cookies
    function getCookie(name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) return parts.pop().split(';').shift();
    }

    // Function to validate annotation
    function validateAnnotation(annotationId) {
        const csrftoken = getCookie('csrftoken'); // Retrieve CSRF token from cookies
        const userIdElement = document.getElementById('userId');
        const userId = userIdElement ? userIdElement.dataset.userId : null; // Retrieve user ID
        
        if (!userId) {
            console.error('User ID is not available.');
            return;
        }
        
        if (!annotationId) {
            console.error('Invalid annotation ID:', annotationId);
            return;
        }
        
        fetch('/newapp/validate_annotation/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': csrftoken // Include CSRF token in headers
            },
            body: `annotation_id=${annotationId}&validated_by_id=${userId}`
        })
        .then(response => {
            if (response.ok) {
                return response.json();
            }
            throw new Error('Network response was not ok.');
        })
        .then(data => {
            if (data.success) {
                console.log('Annotation validated');
                // Optionally, refresh the annotations list to reflect the change
            } else {
                console.error('Error validating annotation:', data.error);
            }
        })
        .catch(error => {
            console.error('Error validating annotation:', error);
        });
    }
    

    // Function to unvalidate annotation
    function unvalidateAnnotation(annotationId) {
        const csrftoken = getCookie('csrftoken'); // Retrieve CSRF token from cookies
        
        if (!annotationId) {
            console.error('Invalid annotation ID:', annotationId);
            return;
        }
        
        fetch('/newapp/unvalidate_annotation/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': csrftoken // Include CSRF token in headers
            },
            body: `annotation_id=${annotationId}`
        })
        .then(response => {
            if (response.ok) {
                return response.json();
            }
            throw new Error('Network response was not ok.');
        })
        .then(data => {
            if (data.success) {
                console.log('Annotation unvalidated');
                // Optionally, refresh the annotations list to reflect the change
            } else {
                console.error('Error unvalidating annotation:', data.error);
            }
        })
        .catch(error => {
            console.error('Error unvalidating annotation:', error);
        });
    }
    

    function toggleSection(section) {
        const checkAnnotationSection = document.getElementById('checkAnnotationSection');
        const assignValidationSection = document.getElementById('assignValidationSection');

        if (section === 'checkAnnotation') {
            checkAnnotationSection.style.display = 'block';
            assignValidationSection.style.display = 'none';
        } else if (section === 'assignValidation') {
            checkAnnotationSection.style.display = 'none';
            assignValidationSection.style.display = 'block';
        }
    }
    const langSelect = document.getElementById('langSelect');
    const validatorsDropdown = document.getElementById('validatorsDropdown');
    const filterInput = document.getElementById('filterInput');
    const sortInput = document.getElementById('sortInput');
    const bulkAssignBtn = document.getElementById('bulkAssignBtn');
    const validatorLanguage = langSelect.value;
    // Add an event listener to the language dropdown
    langSelect.addEventListener('change', function() {
        // Get the selected language from the dropdown
        const validatorLanguage = langSelect.value;

        // Check if a language is selected
        if (!validatorLanguage) {
            alert('Please select a language.');
            return;
        }

        // Call the fetchValidators function with the selected language
        fetchValidators(validatorLanguage);
        displayAnnotationsOfSelectedLanguage(validatorLanguage);
        updateAnnotations(validatorLanguage);
    });

    function fetchValidators(validatorLanguage) {
        // Make an AJAX request to fetch validators for the selected language
        fetch(`/newapp/get_validators/${validatorLanguage}/`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Failed to fetch validators');
                }
                return response.json();
            })
            .then(data => {
                // Display validators in the validators dropdown
                const validatorsDropdown = document.getElementById('validatorsDropdown');
                validatorsDropdown.innerHTML = ''; // Clear previous content
    
                const validators = data.validators;
                if (validators.length > 0) {
                    let validatorsHtml = '<h3>Validators:</h3><select id="validatorsDropdown">';
                    validators.forEach(validator => {
                        validatorsHtml += `<option value="${validator.id}">${validator.username}</option>`;
                    });
                    validatorsHtml += '</select>';
                    validatorsHtml += '<button onclick="assignAnnotations()">Assign Annotations</button>';
                    validatorsDropdown.innerHTML = validatorsHtml;
                } else {
                    validatorsDropdown.innerHTML = '<p>No validators found for the selected language.</p>';
                }
            })
                
            .catch(error => {
                console.error('Error fetching validators:', error);
            });
    }

    function displayAnnotationsOfSelectedLanguage(validatorLanguage, selectedValidatorId) {
        fetch(`/newapp/get_annotations/${validatorLanguage}/`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Failed to fetch annotations');
                }
                return response.json();
            })
            .then(data => {
                const annotationsTableBody = document.getElementById('annotationsTableBody');
                annotationsTableBody.innerHTML = '';
    
                const annotations = data.annotations;
                if (annotations.length > 0) {
                    annotations.forEach(annotation => {
                        const row = annotationsTableBody.insertRow();
                        row.id = `annotation-${annotation.id}`; // Set the ID for the row element
                        row.className = annotation.validated ? 'validated' : 'not-validated'; // Use className to set the style
    
                        const imageCell = row.insertCell(0);
                        const annotationCell = row.insertCell(1);
                        const annotatorCell = row.insertCell(2);
    
                        const imageName = annotation.image.title;
                        const imagePreview = `<img src="${annotation.image.url}" alt="${imageName}" style="max-width: 100px; max-height: 100px;">`;
                        imageCell.innerHTML = `<div>${imageName}</div>${imagePreview}`;
    
                        // Check if the annotation is assigned to the selected validator
                        const isAssignedToSelectedValidator = annotation.validator_id === parseInt(selectedValidatorId);
                        const assignmentTag = isAssignedToSelectedValidator ? '<span class="tag assigned-tag">Assigned</span>' : '';
    
                        // Check if the assigned annotation is validated
                        const validationTag = annotation.validated ? '<span class="tag validated-tag">Validated</span>' : '<span class="tag not-validated-tag">Not Validated</span>';
    
                        annotationCell.innerHTML = `${assignmentTag}${validationTag}${annotation.text}`;
                        annotatorCell.textContent = annotation.annotator.username;
                    });
                } else {
                    const row = annotationsTableBody.insertRow();
                    const noDataCell = row.insertCell(0);
                    noDataCell.colSpan = 3;
                    noDataCell.textContent = 'No annotations found for the selected language.';
                }
            })
            .catch(error => {
                console.error('Error fetching annotations:', error);
            });
    }
    
    function updateValidationStatusForRow(annotationId, isValidated) {
        const row = document.getElementById(`annotation-${annotationId}`);
        if (row) {
            // Assuming the validation status is shown in the second cell (index 1)
            const validationCell = row.cells[1]; // Might need to adjust index based on actual table layout
            validationCell.innerHTML = isValidated ? '<span class="tag validated-tag">Validated</span>' : '<span class="tag not-validated-tag">Not Validated</span>';
            row.className = isValidated ? 'validated' : 'not-validated'; // Update the class to change the color
        }
    }
    
    // Use this function to update the status for a particular annotation
    function updateAnnotations(annotationId, isValidated) {
        updateValidationStatusForRow(annotationId, isValidated);
    }
    
    // You can call `updateAnnotations` with the annotation ID and a boolean indicating the validation status whenever needed.
    
    
    
    
    
    

    

    function getRandomAnnotations(annotations, numberToAssign) {
        // Shuffle the array of annotations
        const shuffledAnnotations = annotations.sort(() => Math.random() - 0.5);
        
        // Slice the array to get the desired number of random annotations
        return shuffledAnnotations.slice(0, numberToAssign);
    }
    
    function bulkAssignAnnotations() {
        const validatorId = document.getElementById('validatorsDropdown').value;
        // Get the number of annotations from the input field
        const numberOfAnnotationsInput = document.getElementById('numberOfAnnotations');
        const numberOfAnnotations = numberOfAnnotationsInput.value;
        
        if (validatorId && numberOfAnnotations) {
            // Get the CSRF token from the cookie
            const csrftoken = getCookie('csrftoken');
    
            // Make an AJAX request to fetch a list of unassigned annotations
            fetch(`/newapp/get_unassigned_annotations/${validatorId}/${numberOfAnnotations}/`)
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Failed to fetch unassigned annotations');
                    }
                    return response.json();
                })
                .then(data => {
                    const unassignedAnnotations = data.unassignedAnnotations;
    
                    if (unassignedAnnotations.length > 0) {
                        // Check if the requested number of annotations is valid
                        const maxAnnotations = Math.min(unassignedAnnotations.length, parseInt(numberOfAnnotations));
                        if (maxAnnotations < numberOfAnnotations) {
                            alert(`We only have ${maxAnnotations} unassigned annotations. Please enter a number less than or equal to ${maxAnnotations}.`);
                            return;
                        }
    
                        // Get a random selection of annotations
                        const randomAnnotations = getRandomAnnotations(unassignedAnnotations, maxAnnotations);
    
                        // Make an AJAX request to assign the selected annotations to the validator
                        fetch(`/newapp/bulk_assign_annotations/`, {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                                'X-CSRFToken': csrftoken,  // Include the CSRF token in the headers
                            },
                            body: JSON.stringify({
                                validatorId: validatorId,
                                annotations: randomAnnotations.map(annotation => annotation.id),
                            }),
                        })
                            .then(response => {
                                if (!response.ok) {
                                    throw new Error('Failed to assign annotations');
                                }
                                return response.json();
                            })
                            .then(assignResponse => {
                                // Handle success, update the display, or show a confirmation message
                                console.log('Annotations assigned successfully:', assignResponse);
                                updateAnnotations(validatorLanguage);
                            })
                            .catch(assignError => {
                                console.error('Error assigning annotations:', assignError.message);
                            });
                    } else {
                        console.log('No unassigned annotations found.');
                    }
                })
                .catch(error => {
                    console.error('Error fetching unassigned annotations:', error.message);
                });
        }
    }
    
    filterInput.addEventListener('input', function() {
        const searchCriteria = filterInput.value.toLowerCase();
        filterAnnotations(searchCriteria);
    });

    function filterAnnotations(searchCriteria) {
        const annotationsTableBody = document.getElementById('annotationsTableBody');
        const rows = annotationsTableBody.getElementsByTagName('tr');

        for (let i = 0; i < rows.length; i++) {
            const imageCell = rows[i].getElementsByTagName('td')[0];
            const annotatorCell = rows[i].getElementsByTagName('td')[2];

            const shouldDisplay = (
                imageCell.textContent.toLowerCase().includes(searchCriteria) ||
                annotatorCell.textContent.toLowerCase().includes(searchCriteria)
            );

            rows[i].style.display = shouldDisplay ? '' : 'none';
        }
    }

    function selectAnnotations(row) {
        if (row.classList.contains('selected')) {
            // Deselect the row
            row.classList.remove('selected');
        } else {
            // Select the row
            row.classList.add('selected');
        }
    }

    function selectAllAnnotations() {
        const annotationsTableBody = document.getElementById('annotationsTableBody');
        const rows = annotationsTableBody.getElementsByTagName('tr');

        for (const row of rows) {
            if (row.style.display !== 'none') {
                // Toggle the selection for each visible row
                if (row.classList.contains('selected')) {
                    row.classList.remove('selected');
                } else {
                    row.classList.add('selected');
                }
            }
        }
    }

    function getSelectedAnnotations() {
        const selectedAnnotations = [];
        const annotationsTableBody = document.getElementById('annotationsTableBody');
        const rows = annotationsTableBody.getElementsByTagName('tr');
    
        for (const row of rows) {
            if (row.classList.contains('selected')) {
                // Get the annotation ID from the row's dataset
                const annotationId = row.dataset.annotationId;
                selectedAnnotations.push(annotationId);
            }
        }
    
        return selectedAnnotations;
    }
    

    // Add event listeners to your buttons
    bulkAssignBtn.addEventListener('click', function () {
        bulkAssignAnnotations();
    });

    const assignAnnotationsBtn = document.getElementById('assignAnnotationsBtn');
    assignAnnotationsBtn.addEventListener('click', function () {
        // Example: Get selected annotations and assign to the selected validator
        const selectedAnnotations = getSelectedAnnotations();
        const validatorId = document.getElementById('validatorsDropdown').value;
    
        // Ensure a validator is selected
        if (!validatorId) {
            alert('Please select a validator.');
            return;
        }
    
        // Ensure at least one annotation is selected
        if (selectedAnnotations.length === 0) {
            alert('Please select at least one annotation.');
            return;
        }
    
        // Send the data to the server, including the CSRF token
        const csrftoken = getCookie('csrftoken');  // Implement getCookie function (see below)
    
        fetch('/newapp/assign_annotations/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'), // Include CSRF token
            },
            body: JSON.stringify({
                validator_id: validatorId,
                annotation_ids: selectedAnnotations,
            }),
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Failed to assign annotations');
                }
                return response.json();
            })
            .then(assignResponse => {
                // Check if the response contains valid data
                if (assignResponse && assignResponse.success) {
                    console.log('Annotations assigned successfully:', assignResponse);
                    updateAnnotations(validatorLanguage);
                    console.log("yess") // Call updateAnnotations if data is valid
                } else {
                    console.error('Error assigning annotations: Invalid response data');
                }
            })
            .catch(assignError => {
                console.error('Error assigning annotations:', assignError);
            });
    });
    
    // Function to get CSRF cookie
    function getCookie(name) {
        const cookieValue = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
        return cookieValue ? cookieValue.pop() : '';
    }
    
    

    const selectAllBtn = document.getElementById('selectAllBtn');
    selectAllBtn.addEventListener('click', function () {
        selectAllAnnotations();
    });

    // Add this event listener to your existing code
    annotationsTableBody.addEventListener('click', function (event) {
        const target = event.target;
        if (target.tagName.toLowerCase() === 'td') {
            // Check if the click is on a table cell
            const row = target.parentElement;
            selectAnnotations(row);
        }
    });

