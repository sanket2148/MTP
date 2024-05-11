const annotations = {};
        const languageSelect = document.getElementById('languageSelect');
        let selectedLanguage = ''; // Initialize with an empty string

        // Add an event listener to the language dropdown to update the selectedLanguage variable
        languageSelect.addEventListener('change', function () {
            selectedLanguage = languageSelect.value;
            if (selectedLanguage) {
                fetch(`/newapp/get_annotation_data_validator/${selectedLanguage}/`)
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
    fetch(`/newapp/get_annotation_data_validator/${selectedLanguage}/`)
        .then(response => response.json())
        .then(data => {
            const { annotators, images, data: annotationData } = data;

            // Combine all annotations for the selected language into a single array
            const allAnnotations = [].concat(...Object.values(annotationData).map(arr => arr));

            // Create a CSV string from the combined annotations
            const csvContent = allAnnotations.map(annotation => {
                return `${annotation.img},${annotation.annotation}`;
            }).join('\n');

            // Create a Blob and create a link to trigger the download
            const blob = new Blob([csvContent], { type: 'text/csv' });
            const link = document.createElement('a');
            link.href = window.URL.createObjectURL(blob);
            link.download = `all_annotations_${selectedLanguage}.csv`;

            // Append the link to the document and trigger the click event
            document.body.appendChild(link);
            link.click();

            // Remove the link from the document
            document.body.removeChild(link);
        })
        .catch(error => console.error('Error fetching data:', error));
}
// Add an event listener to the download button
document.getElementById('downloadButton').addEventListener('click', function() {
    // Call the function to download annotations
    downloadAnnotations();
});

// Function to download annotations from the table
function downloadAnnotations() {
    // Get the table element
    const table = document.getElementById('userAnnotations'); // Update with your table ID

    // Create a CSV string from the table data
    const csvContent = Array.from(table.querySelectorAll('tr')).map(row => {
        const columns = Array.from(row.children).map(column => column.innerText);
        return columns.join(',');
    }).join('\n');

    // Create a Blob and create a link to trigger the download
    const blob = new Blob([csvContent], { type: 'text/csv' });
    const link = document.createElement('a');
    link.href = window.URL.createObjectURL(blob);
    link.download = 'annotations.csv';

    // Append the link to the document and trigger the click event
    document.body.appendChild(link);
    link.click();

    // Remove the link from the document
    document.body.removeChild(link);
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
    