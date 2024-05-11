document.querySelectorAll('.folder-button-link').forEach(folder => {
    folder.addEventListener('click', function(event) {
        const languageName = this.querySelector('.folder-label').textContent.trim();
        // Use the languageName to redirect or perform an action
        window.location.href = `/language_folder/${languageName}/`; // Update the URL as per your routing setup
    });
});
    
    
    function addNewLanguage() {
        const dropdown = document.getElementById('manage-language-dropdown');
        const selectedLanguage = dropdown.options[dropdown.selectedIndex].text;
        const languageList = document.getElementById('language-list');
    
        // Fetch CSRF token
        const csrfToken = getCsrfToken();
    
        // Send AJAX request to Django backend to check if a new language can be added
        fetch('/newapp/add_language/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken,
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 'language_name': selectedLanguage }),
        })
        .then(response => response.json())
        .then(data => {
            if(data.exists) {
                alert("This language already exists.");
            } else {
                // The language does not exist in the backend, add it to the frontend
                const newLi = document.createElement('li');
                newLi.innerHTML = `<a href="language_folder/${selectedLanguage}" class="folder-button-link">
                                        <div class="folder-button">
                                            <div class="folder-icon">
                                                <img src="/static/images/wired-outline-54-photo-picturelandscape-gallery.gif" alt="Folder Icon">
                                            </div>
                                            <div class="folder-label">${selectedLanguage}</div>
                                        </div>
                                    </a>`;
                languageList.appendChild(newLi);
                addToLanguageTable(selectedLanguage);
            }
        })
        .catch(error => {
            console.error("Error adding language:", error);
        });
    }
    
    // Function to get CSRF token from cookies
    function getCsrfToken() {
        const cookies = document.cookie.split(';');
        for(let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            const parts = cookie.split('=');
            if (parts[0] === 'csrftoken') {
                return parts[1];
            }
        }
        return '';
    }
    
    // Assuming you have a function 'addToLanguageTable' to update the table
    // Define or update 'addToLanguageTable' as required
    

    function removeSelectedLanguage() {
        const dropdown = document.getElementById('manage-language-dropdown');
        const selectedLanguage = dropdown.options[dropdown.selectedIndex].text;
        const languageList = document.getElementById('language-list');
        const languageName = dropdown.options[dropdown.selectedIndex].value; 
        const liToRemove = Array.from(languageList.querySelectorAll('li')).find(li => li.textContent.trim() === selectedLanguage);
        if (!liToRemove) {
            alert(`${selectedLanguage} is not in the list.`);
            return;
        }
    
        const confirmation = confirm(`Are you sure you want to remove ${selectedLanguage}?`);
        if (confirmation) {
            // Fetch CSRF token
            const csrfToken = getCsrfToken();
    
            // Send AJAX request to Django backend to remove a language
            fetch('/newapp/remove_language/', {  // Update this URL to the correct Django URL for removing a language
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken,
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ 'language_name': languageName }),
            })
            .then(response => {
                if(response.ok) {
                    // Remove the language from the list in the frontend only if the backend operation was successful
                    liToRemove.parentNode.removeChild(liToRemove);
                    removeFromLanguageTable(selectedLanguage);
                } else {
                    alert('Failed to remove language. Please try again.');
                }
            })
            .catch(error => {
                console.error("Error removing language:", error);
            });
        }
    }
    function addToLanguageTable(language) {
        const tableBody = document.getElementById('language-table-body');
        const rows = tableBody.querySelectorAll('tr');
        let foundRow = null;
    
        for (let row of rows) {
            if (row && row.firstElementChild && row.firstElementChild.textContent.trim() === language) {
                foundRow = row;
                break;
            }
        }
    
        if (foundRow) {
            const annotationsCell = foundRow.children[1];
            if (annotationsCell) { // Additional check before modifying the textContent
                annotationsCell.textContent = parseInt(annotationsCell.textContent, 10) + 1;
            }
        } else {
            const newRow = document.createElement('tr');
            let languageCell = document.createElement('td');
            languageCell.textContent = language;
            newRow.appendChild(languageCell);
    
            ['0', '0', '0'].forEach(defaultValue => {
                let cell = document.createElement('td');
                cell.textContent = defaultValue;
                newRow.appendChild(cell);
            });
    
            tableBody.appendChild(newRow);
        }
    }
    function removeFromLanguageTable(language) {
        const tableBody = document.getElementById('language-table-body');
        const rows = tableBody.querySelectorAll('tr');
        for (let row of rows) {
            if (row && row.firstElementChild && row.firstElementChild.textContent.trim() === language) {
                tableBody.removeChild(row);
                return; // Exit once found
            }
        }
    }
    function checkLanguageStatus() {
        const dropdown = document.getElementById('manage-language-dropdown');
        const selectedLanguage = dropdown.options[dropdown.selectedIndex].text;
        const languageList = document.getElementById('language-list');
        
        if (!dropdown || !languageList) {
            alert("Error: Cannot find necessary DOM elements.");
            return;
        }
        
        let languageExists = Array.from(languageList.querySelectorAll('li')).some(li => li.textContent.trim() === selectedLanguage);
        
       
    }


    document.querySelectorAll('.folder-button-link').forEach(folder => {
        folder.addEventListener('click', function(event) {
            const languageName = this.querySelector('.folder-label').textContent.trim();
            // Redirect to the language folder
            window.location.href = `/newapp/admin_home_page/language_folder/${languageName}/`;
        });
    });
    
    function onLanguageFolderClick(languageName) {
        // Fetch images for the selected language
        console.log("Fetching images for:", languageName);
        fetch(`/newapp/get_images/${languageName}/`)
        .then(response => response.json())
        .then(data => {
            console.log("Received data:", data);
            if(data.status === 'success') {
                displayImages(data.images, languageName);
            } else {
                alert('Failed to load images.');
            }
        })
        .catch(error => console.error('Error loading images:', error));
    }
    

        // ... existing code ...

    /*function openFolder(language) {
        // Fetch the contents of the folder
        fetch(`/getImagesForLanguage?language=${language}`)
            .then(response => response.json())
            .then(data => {
                displayImages(data.images, language);
                
                // Display the image upload input
                const uploadInput = document.getElementById('image-upload-input');
                uploadInput.setAttribute('onchange', `handleImageUpload(this.files, '${language}')`);
                uploadInput.style.display = 'block';
                
            })
            .catch(error => {
                console.error("There was an error fetching the images:", error);
            });*/


    /*function displayImages(images, languageName) {
        const imagesContainer = document.getElementById('images-container'); // Ensure this container exists in your HTML
        imagesContainer.innerHTML = '';
    
        images.forEach(image => {
            const imgElement = document.createElement('img');
            imgElement.src = image.url;
            imgElement.alt = image.name;
            imgElement.classList.add('language-image');
    
            imgElement.addEventListener('click', () => deleteImage(image.id, languageName));
    
            imagesContainer.appendChild(imgElement);
        });
    
        const uploadButton = document.createElement('button');
        uploadButton.textContent = 'Upload New Image';
        uploadButton.addEventListener('click', () => uploadImage(languageName));
        imagesContainer.appendChild(uploadButton);
    }
    

    // ... existing code ...

    function updateImageGallery() {
        const imageGallery = document.getElementById('image-gallery');
        imageGallery.innerHTML = ''; // Clear existing images
    
        // Fetch image URLs (this is just an example, adapt as needed)
        fetch('/path-to-get-images')
        .then(response => response.json())
        .then(images => {
            images.forEach(imageSrc => {
                const imgDiv = document.createElement('div');
                const img = document.createElement('img');
                img.src = imageSrc; // Set the source of the image
                img.style.maxWidth = '150px'; // Example styling
                img.style.height = 'auto';
                imgDiv.appendChild(img);
                imageGallery.appendChild(imgDiv);
            });
        })
        .catch(error => console.error('Error:', error));
    }
    
    // Call this function after images are uploaded
    // updateImageGallery();*/
    
