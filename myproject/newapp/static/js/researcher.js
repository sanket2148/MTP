
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
        document.querySelectorAll('.folder-button-link').forEach(folder => {
            folder.addEventListener('click', function(event) {
                const languageName = this.querySelector('.folder-label').textContent.trim();
                // Use the languageName to redirect or perform an action
                window.location.href = `/language_folder_researcher/${languageName}/`; // Update the URL as per your routing setup
            });
        });
  