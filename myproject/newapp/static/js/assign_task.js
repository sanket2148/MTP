// document.getElementById('select-language').addEventListener('change', function() {
//     var selectedLanguage = this.value;
//     if (selectedLanguage) {
//         fetchAnnotators(selectedLanguage);
//         fetchImages(selectedLanguage);
//         console.log(typeof selectedLanguage); // Check the type
//         console.log(selectedLanguage); // Check the value

//     }
// });

// function fetchAnnotators(language) {
//     console.log('fetchAnnotators:', typeof language, language); // For debugging
//     fetch(`/newapp/get_selected_annotators/${language}`)
//         .then(response => response.json())
//         .then(data => {
//             if (data.annotators.length === 0) {
//                 alert("No annotators available for this language.");
//             } else {
//                 console.log('fetchAnnotators data:', data);
//                 updateAnnotatorsDropdown(language); // Pass the language string, not the object
//                 updateAnnotatorsTable(data.annotators);
//                 makeImagesDraggable();
                
//             }
//         })
//         .catch(error => console.error('Error fetching annotators:', error));
// }


// function fetchImages(language) {
//     console.log("fetchImages called with language:", language);
//     fetch(`/newapp/get_images_for_language/${language}`)
//         .then(response => response.json())
//         .then(data => {
//             console.log("Images data received:", data);
//             if (data.images.length === 0) {
//                 alert("No images available for this language.");
//                 updateImagesGallery(data.images);
//             } else {
//                 updateImagesGallery(data.images);  // Note the change here
//             }
//         })
//         .catch(error => console.error('Error fetching images:', error));
// }


// function updateAnnotatorsDropdown(language) {
//     console.log('updateAnnotatorsDropdown:', typeof language, language); // For debugging
//     fetch(`/newapp/get_selected_annotators/${language}`)
//         .then(response => response.json())
//         .then(data => {
//             var annotatorSelect = document.getElementById('selected-annotator-random');
//             annotatorSelect.innerHTML = '';
//             data.annotators.forEach(annotator => {
//                 var option = document.createElement('option');
//                 option.value = annotator.username;
//                 option.textContent = annotator.username;
//                 annotatorSelect.appendChild(option);
//             });
//         })
//         .catch(error => console.error('Error fetching annotators:', error));
// }


// function updateImagesGallery(images) {
//     console.log("updateImagesGallery called with images:", images);
//     var imageContainer = document.getElementById('image-container');
//     imageContainer.innerHTML = '';
//     var relativePathToImages = '/media/';
    
//     // Update the total number of images for the selected language
//     document.getElementById('total-images').textContent = images.length;
//     images.forEach(image => {
//         var imageBox = document.createElement('div');
//         imageBox.className = 'image-box';

//         var img = document.createElement('img');
//         img.src = relativePathToImages + image.filename;
//         img.alt = image.title;
//         img.draggable = true;
//         console.log('Image URL:', relativePathToImages + image.filename);

//         img.onerror = function() {
//             console.error('Error loading image:', img.src);
//         };

//         var titleDiv = document.createElement('div');
//         titleDiv.className = 'image-title';
//         titleDiv.textContent = image.title;

//         imageBox.appendChild(img);
//         imageBox.appendChild(titleDiv);
//         imageContainer.appendChild(imageBox);
//     });
// }


//     function updateAnnotatorsTable(annotators) {
//     var tableBody = document.getElementById("annotators-table").getElementsByTagName('tbody')[0];
//     tableBody.innerHTML = '';
    
//     annotators.forEach(annotator => {
//         var row = tableBody.insertRow();
//         var annotatorCell = row.insertCell(0);
//         annotatorCell.textContent = annotator.username;

//         var assignedImagesCell = row.insertCell(1);
//         assignedImagesCell.setAttribute('data-annotator', annotator.username);
//         assignedImagesCell.classList.add('drop-zone');

//         // Fetch assigned images for the annotator
//         fetchAssignedImages(annotator.username)
//             .then(images => {
//                 images.forEach(image => {
//                     // Create a span element to display the image name
//                     var imageSpan = document.createElement('span');
//                     imageSpan.textContent = image; // Assuming 'image' contains the filename
//                     imageSpan.classList.add('clickable'); // Add a class for styling and event binding

//                     // Add a click event listener to remove the image when clicked
//                     imageSpan.addEventListener('click', function() {
//                         removeImageFromAssignment(annotator.username, image);
//                     });

//                     // Append the span element to the assigned images cell
//                     assignedImagesCell.appendChild(imageSpan);
//                     assignedImagesCell.appendChild(document.createTextNode(', '));
//                 });
//             })
//             .catch(error => console.error('Error fetching assigned images:', error));

//         assignedImagesCell.addEventListener('dragover', function(event) {
//             event.preventDefault();
//         });

//         assignedImagesCell.addEventListener('drop', function(event) {
//             event.preventDefault();
//             var imageTitle = event.dataTransfer.getData('text/plain').trim().toLowerCase();
//             var annotator = this.getAttribute('data-annotator'); // Get the annotator from the cell attribute
        
//             // Check if the image is already assigned to the annotator
//             var alreadyAssigned = Array.from(this.querySelectorAll('span')).some(span => span.textContent.trim() === imageTitle);
            
//             if (!alreadyAssigned) {
//                 // Create a new span element for the dropped image title
//                 var imageSpan = document.createElement('span');
//                 imageSpan.textContent = imageTitle;
//                 imageSpan.classList.add('clickable'); // Add a class for styling and event binding
        
//                 // Add a click event listener to remove the image when clicked
//                 imageSpan.addEventListener('click', function() {
//                     removeImageFromAssignment(annotator, imageTitle);
//                 });
        
//                 // Append the span element to the assigned images cell
//                 this.appendChild(imageSpan);
//                 this.appendChild(document.createTextNode(', '));
        
//                 // Save the assignment to the server
//                 // saveAssignmentToServer(annotator, imageTitle);
//             } else {
//                 alert("This image is already assigned to this annotator.");
//             }
//         });
        
//     });
// }


// function removeImageFromAssignment(annotator, imageTitle) {
//     var confirmed = confirm(`Are you sure you want to remove "${imageTitle}" from the assignment?`);
//     if (confirmed) {
//         // Remove the image from the UI
//         var assignedImagesCell = document.querySelector(`[data-annotator='${annotator}']`);
//         var spans = assignedImagesCell.querySelectorAll('span');
//         spans.forEach(span => {
//             if (span.textContent === imageTitle) {
//                 span.parentNode.removeChild(span); // Remove the span element
//             }
//             saveImageAssignment();
//         });

//         // Remove the image from the assigned images array
//         var index = assignedImagesPerAnnotator[annotator].indexOf(imageTitle);
//         if (index !== -1) {
//             assignedImagesPerAnnotator[annotator].splice(index, 1); // Remove the image title from the array
//         }

//         // Send a request to the server to update the assignment
//         fetch('/newapp/remove_assignment/', {
//             method: 'POST',
//             headers: {
//                 'Content-Type': 'application/json',
//                 'X-CSRFToken': getCookie('csrftoken'), // Include CSRF token
//             },
//             body: JSON.stringify({
//                 annotator: annotator,
//                 imageTitle: imageTitle
//             }),
//         })
//         .then(response => {
//             if (!response.ok) {
//                 throw new Error('Failed to remove assignment');
//             }
//             return response.json();
//         })
//         .then(data => {
//             if (data.success) {
//                 console.log('Assignment removed successfully from backend.');
//             } else {
//                 console.error('Error removing assignment from backend.');
//             }
//         })
//         .catch(error => {
//             console.error('Error removing assignment:', error);
//         });
//     }
// }


// function fetchAssignedImages(annotator) {
//     return fetch(`/newapp/get_assigned_images/${annotator}`)
//         .then(response => response.json())
//         .then(data => data.images)
//         .catch(error => {
//             console.error('Error fetching assigned images:', error);
//             return [];
//         });
// }






//             // Example: Making images draggable
//             function makeImagesDraggable() {
//                 var images = document.querySelectorAll('#image-container img');
//                 images.forEach(img => {
//                     img.setAttribute('draggable', true);
//                     img.addEventListener('dragstart', function(event) {
//                         // Set the image title as the drag data
//                         var imageTitle = img.alt; // Assuming the alt attribute holds the image title
//                         event.dataTransfer.setData('text/plain', imageTitle);
//                     });
//                 });
//             }
            

    

//     let assignedImagesPerAnnotator = {};
//     let currentAssignments = new Set();
//     let assignedImagesSet = new Set();

//     function getCurrentAssignments(annotator) {
//         currentAssignments.clear(); 
//         // Find the row for the annotator
//         const rows = document.querySelectorAll("#annotators-table tbody tr");
//         rows.forEach(row => {
//             if (row.cells[0].textContent === annotator) {
//                 // Assuming the second cell contains assigned images
//                 const images = row.cells[1].textContent.split(", ");
//                 images.forEach(img => currentAssignments.add(img.trim().toLowerCase())); // Store titles in lowercase
//             }
//         });
//         return currentAssignments;
//     }
    

//     // Define a map to store assigned images for each annotator

// function assignImagesToAnnotator(images, selectedAnnotator) {
// // Initialize the assigned images array for the selected annotator if not already initialized
// if (!assignedImagesPerAnnotator[selectedAnnotator]) {
// assignedImagesPerAnnotator[selectedAnnotator] = new Set();
// }

// images.forEach(image => {
// const trimmedTitle = image.title.trim().toLowerCase();
// const assignedImagesCell = document.querySelector(`[data-annotator='${selectedAnnotator}']`);

// // Check if the image is already assigned to the selected annotator
// if (!assignedImagesPerAnnotator[selectedAnnotator].has(trimmedTitle)) {
//     var imageSpan = document.createElement('span');
//     imageSpan.textContent = image.title;
//     assignedImagesCell.appendChild(imageSpan);
//     assignedImagesCell.appendChild(document.createTextNode(", "));

//     assignedImagesPerAnnotator[selectedAnnotator].add(trimmedTitle); // Update the assigned images set for the annotator
//     assignedImagesSet.add(trimmedTitle); // Update the unified set with the new assignment

//     // Display a notification for the new assignment
    
// } else {
//     console.log("This image is already assigned to this annotator.");
// }
// });

// // Update the total number of images available for assignment

// }


    
    
    
    

//     function randomlyAssignImages() {
//         var selectedAnnotator = document.getElementById('selected-annotator-random').value;
//         var numberOfImages = parseInt(document.getElementById('number-of-images').value);
//         var selectedLanguage = document.getElementById('select-language').value;
        
//         // Fetch all available images for the selected language
//         fetch(`/newapp/get_images_for_language/${selectedLanguage}`)
//             .then(response => response.json())
//             .then(data => {
//                 // Ensure data.images is an array
//                 var images = Array.isArray(data) ? data : data.images;
//                 if (isNaN(numberOfImages) || numberOfImages < 1 || !selectedAnnotator || numberOfImages > images.length) {
//                     alert("Please enter a valid number of images and ensure you've selected an annotator.");
//                     return;
//                 }
    
//                 var assignedImagesCell = document.querySelector(`[data-annotator='${selectedAnnotator}']`);
//                 var assignedImages = Array.from(assignedImagesCell.querySelectorAll('span')).map(span => span.textContent.trim());

//                 var randomlySelectedImages = [];
//                 var availableImages = images.filter(image => !assignedImages.includes(image.title)); // Filter out already assigned images

//                 while (randomlySelectedImages.length < numberOfImages && availableImages.length > 0) {
//                     var randomIndex = Math.floor(Math.random() * availableImages.length);
//                     randomlySelectedImages.push(availableImages[randomIndex]);
//                     availableImages.splice(randomIndex, 1); // Remove the assigned image from the available list
//                 }
    
//                 // Assign randomly selected images to the chosen annotator
//                 assignImagesToAnnotator(randomlySelectedImages, selectedAnnotator);
//             })
//             .catch(error => console.error('Error:', error));
//     }



    
//     ////////////////////////////////////////////////////////////////////////////////////


//     // Add this function to your script
//     function saveImageAssignment() {
//         var selectedLanguage = document.getElementById('select-language').value;
    
//         // Create an object to store assigned images for each annotator
//         var assignedImages = {};
    
//         // Iterate over each table row
//         var rows = document.querySelectorAll("#annotators-table tbody tr");
//         rows.forEach(row => {
//             var annotator = row.cells[0].textContent;
//             var assignedImagesCell = row.cells[1];
            
//             // Collect assigned image titles for the annotator
//             var images = [];
//             assignedImagesCell.querySelectorAll('span').forEach(span => {
//                 images.push(span.textContent.trim());
//             });
    
//             // Store the assigned images for the annotator
//             assignedImages[annotator] = images;
//         });
    
//         // Send AJAX request to save assignments
//         fetch('/newapp/save_assignments/', {
//             method: 'POST',
//             headers: {
//                 'Content-Type': 'application/json',
//                 'X-CSRFToken': getCookie('csrftoken'),  // Ensure you include CSRF token
//             },
//             body: JSON.stringify({
//                 language: selectedLanguage,
//                 assignedImages: assignedImages,
//             }),
//         })
//         .then(response => {
//             if (!response.ok) {
//                 throw new Error(`HTTP error! Status: ${response.status}`);
//             }
//             return response.json();
//         })
//         .then(data => {
//             if (data.success) {
//                 alert('Assignments saved successfully!');
//                 // Optionally, you can update the UI or perform other actions
//             } else {
//                 alert('Error saving assignments.');
//             }
//         })
//         .catch(error => console.error('Error:', error));
//     }
    

// // Include this function to get CSRF token from cookies
// function getCookie(name) {
// var cookieValue = null;
// if (document.cookie && document.cookie !== '') {
// var cookies = document.cookie.split(';');
// for (var i = 0; i < cookies.length; i++) {
//     var cookie = cookies[i].trim();
//     if (cookie.substring(0, name.length + 1) === (name + '=')) {
//         cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
//         break;
//     }
// }
// }
// return cookieValue;
// }

    