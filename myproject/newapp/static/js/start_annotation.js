
    const imageUpload = document.getElementById('imageUpload');
    const previewImage = document.getElementById('previewImage');
    let imageFiles = [];
    let currentImageIndex = -1;
    let deletedImagesStack = [];
    let deletedRows = [];
    

    

    function isDuplicateAnnotation(imageName, userText) {
        const table = document.getElementById('annotationsTable');
        for (let i = 1; i < table.rows.length; i++) {
            if (table.rows[i].cells[0].textContent === imageName && table.rows[i].cells[1].textContent === userText) {
                return true;
            }
        }
        return false;
    }

    function addEntryToTable() {
        if (currentImageIndex < 0 || currentImageIndex >= imageFiles.length) {
            alert("Please select an image first.");
            return;
        }
    
        const table = document.getElementById('annotationsTable').getElementsByTagName('tbody')[0];
        const imageId = imageFiles[currentImageIndex].id;
        const imageName = imageFiles[currentImageIndex].title || imageFiles[currentImageIndex].src.split('/').pop();
        const userText = document.getElementById('voiceTextInput').value;
        const languageName = document.getElementById('imagelanguageSelect').value;
    
        // Generate the created_at timestamp in ISO 8601 format
        const now = new Date();
        const created_at = now.toISOString();
    
        if (isDuplicateAnnotation(imageName, userText)) {
            alert("This annotation already exists!");
            return;
        }
        
        if (typeof imageId === 'undefined') {
            console.error("Image ID is undefined, index:", currentImageIndex);
            console.log("Image files loaded:", imageFiles);
        } else {
            submitAnnotation(created_at, imageId, userText, languageName).then(annotation => { // Include annotation data in response
                const newRow = table.insertRow();
    
                let createdAtCell = newRow.insertCell(0);
                createdAtCell.textContent = created_at; // Display the created_at timestamp in the table
    
                let imageCell = newRow.insertCell(1);
                imageCell.textContent = imageName;
    
                let textCell = newRow.insertCell(2);
                textCell.textContent = userText;
    
                let validationStatusCell = newRow.insertCell(3); // New column for validation status
                validationStatusCell.textContent = annotation.validated ? 'Validated' : 'Not Validated'; // Display validation status
    
                let actionCell = newRow.insertCell(4);
                // Add action buttons if necessary
                const editButton = document.createElement('button');
                editButton.innerText = "Edit";
                editButton.onclick = function() {
                    // Define edit behavior
                    editAnnotation(newRow);
                };
                actionCell.appendChild(editButton);
    
                const deleteButton = document.createElement('button');
                deleteButton.innerText = "Delete";
                deleteButton.onclick = function() {
                    // Define delete behavior
                    const annotationId = this.getAttribute('data-annotation-id');
                    deleteAnnotation(annotationId);
                };
                actionCell.appendChild(deleteButton);
    
                alert("Annotation saved successfully.");
    
            }).catch(error => {
                console.error('Error submitting annotation:', error);
                alert("Failed to save annotation.");
            });
        }
    }
    
    function submitAnnotation(created_at ,imageId, annotationText, languageName, isValidated) {
        const data = new FormData();
        console.log("Submitting Image ID:", imageId);
        data.append('created_at', created_at)
        data.append('image_id', imageId);
        data.append('annotation', annotationText);
        data.append('language', languageName);
        data.append('validated', isValidated);
        return fetch('/newapp/create_annotation/', {
            method: 'POST',
            body: data,
            credentials: 'include',
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        });
    }
    
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    

//     function deleteAnnotation(annotationId) {
//     if (confirm("Are you sure you want to delete this annotation?")) {
//         // Retrieve CSRF token from meta tag
//         const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
        
//         // Prepare the request body with the annotation ID
//         const requestData = JSON.stringify({
//             annotationId: annotationId
//         });

//         fetch('/newapp/delete_annotation/', { // Ensure the URL is correct
//             method: 'POST',
//             headers: {
//                 'Content-Type': 'application/json',
//                 'X-CSRFToken': csrfToken, // Include CSRF token in the request headers
//             },
//             body: requestData,
//             credentials: 'include' // This may be necessary depending on your Django configuration
//         })
//         .then(response => {
//             if (response.ok) {
//                 // Optionally, remove the annotation from the UI or refresh the page
//                 console.log("Annotation deleted successfully.");
//                 // For example, if you have a function to refresh the annotations list, call it here
//                 // refreshAnnotationsList();
//             } else {
//                 response.json().then(data => console.error(data.error));
//                 alert("Failed to delete annotation.");
//             }
//         })
//         .catch(error => console.error('Error:', error));
//     }
// }



function deleteAnnotation(annotationId) {
    if (!annotationId) {
        console.error("Error: No annotation ID provided.");
        return; // Stop the function if no ID is provided
    }

    if (confirm("Are you sure you want to delete this annotation?")) {
        const csrfToken = getCookie('csrftoken'); // Using the getCookie function to retrieve the CSRF token

        const requestData = JSON.stringify({
            annotationId: annotationId
        });

        console.log("Attempting to delete annotation with ID:", annotationId); // Log the ID being sent

        fetch('/newapp/delete_annotation/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
            },
            body: requestData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                console.log("Annotation deleted successfully.");
                alert("Annotation deleted successfully.");
                location.reload();
                fetchAndDisplayAnnotations(); // Refresh the page or update the UI
            } else {
                throw new Error(data.error || 'Failed to delete annotation.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error deleting annotation: ' + error.message);
        });
    }
}

    

    
    

    /*function undoDeletedImage() {
        if (deletedImagesStack.length > 0) {
            const restoredImage = deletedImagesStack.pop(); // Get the last deleted image
            imageFiles.push(restoredImage); // Restore it to the imageFiles array
            currentImageIndex = imageFiles.length - 1; // Update current index to restored image
            updateFocusedImage(restoredImage.src); // Update the focused image display
            updateImageGallery(); // If you have a function to update the whole gallery
        } else {
            alert('No images to restore.');
        }
    }*/

    function undoDeletedImage() {
        if (deletedImagesStack.length > 0) {
            const { imageFile, container } = deletedImagesStack.pop();
    
            // Add the image file back to the imageFiles array
            imageFiles.push(imageFile);
    
            // Restore the container by setting its display property
            container.style.display = 'inline-block';
    
            // Update the image gallery
            updateImageGallery();
        } else {
            alert('No images to undo');
        }
    }
    

    function downloadImagesAsZip() {
        try {
            if (imageFiles.length === 0) {
                alert("There are no images to download.");
                return;
            }

            const zip = new JSZip();
            const folder = zip.folder("images");

            imageFiles.forEach(file => {
                folder.file(file.name, file);
            });

            zip.generateAsync({ type: "blob" })
            .then(content => {
                const url = URL.createObjectURL(content);
                const a = document.createElement("a");
                a.href = url;
                a.download = "images.zip";
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
            });
        } catch (error) {
            console.error("Error generating ZIP:", error);
            alert("There was an error generating the ZIP. Please try again.");
        }
    }

    function updateImageGallery() {
        const focusedImageDiv = document.getElementById('focused-image');
        const imageListDiv = document.getElementById('image-list');
        focusedImageDiv.innerHTML = '';
        imageListDiv.innerHTML = ''; // Clear existing thumbnails

        // Helper function to create thumbnail
        function createThumbnail(image, isFetched = false) {
            const imgContainer = document.createElement('div');
            imgContainer.className = 'imgContainer';

            const thumbnail = document.createElement('img');
            thumbnail.src = isFetched ? image.src : URL.createObjectURL(image);
            imgContainer.appendChild(thumbnail);

            const imgLabel = document.createElement('div');
            imgLabel.innerText = image.name;
            imgLabel.className = 'imgLabel';
            imgContainer.appendChild(imgLabel);

            thumbnail.onclick = function() {
                // Ensure you update this function to handle showing fetched images correctly
                updateFocusedImage(thumbnail.src);
            };

            if (!isFetched) { // Assuming delete functionality is for uploaded images only
                const deleteBtn = document.createElement('button');
                deleteBtn.className = 'delete-button';
                deleteBtn.innerText = 'X';
                deleteBtn.onclick = function() {
                    deleteImage(image); // Ensure this function can handle both uploaded and fetched images
                };
                imgContainer.appendChild(deleteBtn);
            }

            imageListDiv.appendChild(imgContainer);
        }

        // Loop through uploaded images
        imageFiles.forEach(file => {
            createThumbnail(file);
        });

        // Loop through fetched images
        fetchedImageFiles.forEach(file => {
            createThumbnail(file, true);
        });
    }

    



    


    
    function searchImages() {
        var input, filter, imgContainers, img, i, imgLabel, txtValue;
    input = document.getElementById("searchBar");
    filter = input.value.toUpperCase();
    imgContainers = document.getElementById("image-list").getElementsByClassName('imgContainer');

    // Search and display images
    for (i = 0; i < imgContainers.length; i++) {
        img = imgContainers[i].getElementsByTagName('img')[0]; // Get the image inside the container
        imgLabel = imgContainers[i].getElementsByClassName('imgLabel')[0]; // Get the label inside the container
        txtValue = img.alt || imgLabel.innerText; // Use alt attribute or the innerText of the label
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
            imgContainers[i].style.display = "";
        } else {
            imgContainers[i].style.display = "none";
        }
    }

    // Hide all annotation containers initially
    var annotationContainers = document.getElementsByClassName('annotationContainer');
    for (i = 0; i < annotationContainers.length; i++) {
        annotationContainers[i].style.display = "none";
    }

    // Show annotations related to the searched image
    var searchedImage = filter.trim(); // Get the searched image name
    var relatedAnnotations = document.querySelectorAll('[data-image-name="' + searchedImage + '"]');
    for (i = 0; i < relatedAnnotations.length; i++) {
        relatedAnnotations[i].style.display = "";
    }
}
    

    

    function deleteImage(index) {
        if (index >= 0 && index < imageFiles.length) {
            // Remove the image file from the array
            const deletedImage = imageFiles.splice(index, 1)[0]; // Remove and get the deleted image
    
            // Adjust the current image index if necessary
            if (currentImageIndex >= index) {
                currentImageIndex--;
            }
    
            // Create an object to store the deleted image and its container
            const deletedImageInfo = {
                imageFile: deletedImage,
                container: document.querySelector(".thumbnail-container:nth-child(" + (index + 2) + ")") // Adjust the index
            };
    
            // Push the deleted image info to the deletedImagesStack
            deletedImagesStack.push(deletedImageInfo);
    
            // Update the image gallery
            updateImageGallery();
        }
    }
    

    function showNextImage() {
        if (currentImageIndex < imageFiles.length - 1) {
            currentImageIndex++;
            updateFocusedImage(imageFiles[currentImageIndex].src); // Assuming each image file has a .src property
        } else {
            alert('You are at the last image.');
        }
    }
    

    function showPreviousImage() {
        if (currentImageIndex > 0) {
            currentImageIndex--;
            updateFocusedImage(imageFiles[currentImageIndex].src); // Assuming each image file has a .src property
        } else {
            alert('You are at the first image.');
        }
    }

    // Other JavaScript code...
    
    


    function downloadAnnotations() {
        try {
            const table = document.getElementById('annotationsTable');
            
            if (table.rows.length <= 1) { // Assuming there's a header row
                alert("There are no annotations to download.");
                return;
            }
            
            let csv = [];
            for (let i = 0, row; row = table.rows[i]; i++) {
                let tmpCol = [];
                for (let j = 0, col; col = row.cells[j]; j++) {
                    tmpCol.push(col.textContent);
                }
                csv.push(tmpCol.join(","));
            }
            const csvData = csv.join("\n");
            const blob = new Blob([csvData], { type: 'text/csv' });
            const url = window.URL.createObjectURL(blob);
    
            const a = document.createElement('a');
            a.setAttribute('hidden', '');
            a.setAttribute('href', url);
            a.setAttribute('download', 'annotations.csv');
    
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
        } catch (error) {
            console.error("Error downloading annotations:", error);
            alert("There was an error downloading the annotations. Please try again.");
        }
    }
    
    let recognition;
    let final_transcript = '';
    let mediaRecorder;
    let audioChunks = [];

    if (window.hasOwnProperty('webkitSpeechRecognition')) {
        recognition = new webkitSpeechRecognition();
        recognition.continuous = true;
        recognition.interimResults = true;
        recognition.lang = "en-US";

        recognition.onresult = function (event) {
            let interim_transcript = '';

            for (let i = event.resultIndex; i < event.results.length; ++i) {
                if (event.results[i].isFinal) {
                    final_transcript += event.results[i][0].transcript;
                } else {
                    interim_transcript += event.results[i][0].transcript;
                }
            }

            document.getElementById('voiceTextInput').value = final_transcript + interim_transcript;
        };

        recognition.onerror = function (event) {
            console.error('Speech recognition error:', event.error);
            switch (event.error) {
                case 'not-allowed':
                    alert('Microphone access is not allowed. Please enable microphone permissions in your browser settings.');
                    break;
                case 'no-speech':
                    alert('No speech was detected. Please try speaking again.');
                    break;
                case 'audio-capture':
                    alert('No microphone was found. Ensure that a microphone is installed and that microphone settings are configured correctly.');
                    break;
                case 'network':
                    alert('Network communication required for speech recognition failed.');
                    break;
                default:
                    alert('Error occurred in speech recognition: ' + event.error);
                    break;
            }
            stopDictation(); // Consider whether stopping dictation here is always the appropriate action
        };
        

    } else {
        alert("Your browser does not support voice recognition. Please try in Chrome.");
    }

    // Function to start recording and send data to Vosk server for speech recognition

    function setupRecognition() {
        if (window.hasOwnProperty('webkitSpeechRecognition')) {
            recognition = new webkitSpeechRecognition();
            recognition.continuous = true;
            recognition.interimResults = true;
            recognition.lang = document.getElementById('languageSelect').value;
    
            recognition.onresult = function (event) {
                let interim_transcript = '';
                for (let i = event.resultIndex; i < event.results.length; ++i) {
                    if (event.results[i].isFinal) {
                        final_transcript += event.results[i][0].transcript;
                    } else {
                        interim_transcript += event.results[i][0].transcript;
                    }
                }
                document.getElementById('voiceTextInput').value = final_transcript + interim_transcript;
            };
    
            recognition.onerror = function (event) {
                console.error('Speech recognition error:', event);
                stopDictation();
            };
    
        } else {
            alert("Your browser does not support voice recognition. Please try in Chrome.");
        }
    }
    
function startDictation() {
    final_transcript = '';
    setupRecognition(); // Set up recognition with the selected language
    if (recognition) {
        recognition.start();
    }
}


function pauseDictation() {
    if (recognition) {
        recognition.stop();
    }
}

function stopDictation() {
    if (recognition) {
        recognition.stop();
        final_transcript = '';
    }
}


function displayFetchedImages(images) {
    const imageListDiv = document.getElementById('image-list');
    imageListDiv.innerHTML = ''; // Clear existing images
    imageFiles = []; // Reset the imageFiles array for new fetched images

    images.forEach((imageData, index) => {
        // Ensure imageData has the properties you expect
        if (imageData && imageData.image) { // Use imageData.image instead of imageData.src
            const imgContainer = document.createElement('div');
            imgContainer.className = 'imgContainer';

            const thumbnail = document.createElement('img');
            thumbnail.src = '/media/' + imageData.image; // Use the image property for the image source
            thumbnail.alt = imageData.title || 'Image'; // Fallback title if none provided
            imgContainer.appendChild(thumbnail);

            const imgLabel = document.createElement('div');
            imgLabel.innerText = imageData.title || 'Default Title';
            imgLabel.className = 'imgLabel';
            imgContainer.appendChild(imgLabel);

            // Add event listener to update focused image on click
            thumbnail.onclick = function() {
                currentImageIndex = index; // Set current image index to this image
                updateFocusedImage(imageData.image); // Update the focused image using imageData.image
            };

            imageListDiv.appendChild(imgContainer); // Append the container to the image list div

            // Add the image data to the imageFiles array
            imageFiles.push({
                id: imageData.id, 
                src: imageData.image, // Use imageData.image here
                title: imageData.title || 'Image' // Optional: include title or other metadata
            });
        }
    });

    if (images.length > 0) {
        // Set the first image as the focused image initially
        currentImageIndex = 0;
        updateFocusedImage(imageFiles[0].src);
    }
}


function updateFocusedImage(src) {
    const focusedImageDiv = document.getElementById('focused-image');
    focusedImageDiv.innerHTML = ''; // Clear the current preview
    const img = document.createElement('img');
    img.src = '/media/' + src;
    focusedImageDiv.appendChild(img);
}



    

   document.addEventListener('DOMContentLoaded', function() {
    // Get the select element
    const languageSelect = document.getElementById('imagelanguageSelect');

    // Fetch images when the language selection changes
    languageSelect.addEventListener('change', function() {
        const selectedLanguage = this.value;
        fetchImagesFromLanguageFolder(selectedLanguage);
    });

    // Optionally, fetch images for the initially selected language
    // Remove this line if you don't want to fetch images until the user makes a selection
    //fetchImagesFromLanguageFolder(languageSelect.value);
});
    
    function fetchImagesFromLanguageFolder(language) {
        fetch(`/newapp/get_images_from_language?language=${language}`, {
            method: 'GET',
            headers: {
                'X-CSRFToken': getCsrfToken(), // Ensure CSRF token is included for Django
            },
        })
        .then(response => {
            if (response.ok) {
                return response.json();
            } else {
                console.error('Server returned an error response:', response);
            }
        })
        .then(data => {
            if (data && data.images) {
                console.log("Daata to display:", data.images);
                if(data.images == 0){
                    alert("You dont have images for selected language")
                }

                displayFetchedImages(data.images);
            }
            else {
                // Handle case where images are not in the expected format or path
                console.error('Images array is missing or undefined in the response:', data);
            }
        })
        .catch((error) => {
             console.error('Error:', error);
            
        });
    }
    function getCsrfToken() {
        // Assuming you have a meta tag with name="csrf-token" in your HTML
        const csrfTokenMetaTag = document.querySelector('meta[name="csrf-token"]');
        
        if (csrfTokenMetaTag) {
            return csrfTokenMetaTag.content;
        } else {
            console.error('CSRF token not found.');
            return null;
        }
    }
   

    


function fetchAndDisplayAnnotations(language) {
    fetch(`/newapp/get_annotations_from_language/?language=${language}`, {
        method: 'GET',
        headers: {
            'X-CSRFToken': getCsrfToken(), // Ensure CSRF token is included
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.annotations) {
            updateAnnotationsTable(data.annotations);
        }
    })
    .catch(error => console.error('Error fetching annotations:', error));
}

function updateAnnotationsTable(annotations) {
    const tableBody = document.getElementById('annotationsTable').getElementsByTagName('tbody')[0];
    tableBody.innerHTML = ''; // Clear existing rows
    
    annotations.forEach(annotation => {
        const newRow = tableBody.insertRow();
        
        let created_atCell = newRow.insertCell(0)
        created_atCell.textContent = annotation.created_at;

        let imageCell = newRow.insertCell(1);
        imageCell.textContent = annotation.image__title;
        
        let textCell = newRow.insertCell(2);
        textCell.textContent = annotation.annotation;
        
        let validationStatusCell = newRow.insertCell(3);
        validationStatusCell.textContent = annotation.validated ? 'Validated' : 'Not Validated'; // Display validation status
        
        let actionCell = newRow.insertCell(4);
        
        const editButton = document.createElement('button');
        editButton.innerText = "Edit";
        editButton.onclick = function() {
            // Define edit behavior
            editAnnotation(newRow);
        };
        actionCell.appendChild(editButton);

        const deleteButton = document.createElement('button');
        deleteButton.innerText = "Delete";
        deleteButton.onclick = function() {
            // Define delete behavior
            const annotationId = this.getAttribute('data-annotation-id');
            deleteAnnotation(annotationId);
        };
        actionCell.appendChild(deleteButton);

        // Add any desired buttons/actions for each annotation row here
        
        // Initially show all rows
        newRow.style.display = ""; 
    });
}



// Listen for language selection changes and fetch annotations
document.getElementById('imagelanguageSelect').addEventListener('change', function() {
    const selectedLanguage = this.value;
    fetchAndDisplayAnnotations(selectedLanguage);
});








