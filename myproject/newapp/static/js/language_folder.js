
            document.addEventListener('DOMContentLoaded', function() {
                // Ensure the correct ID is used for your form
                document.getElementById('image-upload-form').addEventListener('submit', function(event) {
                    event.preventDefault();
                    const formData = new FormData(this);
                    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        
                    fetch(this.action, {
                        method: 'POST',
                        body: formData,
                        headers: {
                            'X-CSRFToken': csrfToken
                        }
                    })
                    .then(response => response.json())
                    .then(data => {
                        if (data.status === 'success') {
                            updateImageGallery();
                        } else {
                            console.error('Error:', data.message);
                        }
                    })
                    .catch(error => console.error('Error:', error));
                });
            });
        
            function updateImageGallery() {
                console.log("Updating gallery");
                fetch(`/newapp/get_latest_images/?language_name=${encodeURIComponent('{{ language_name }}')}`)
                .then(response => response.json())
                .then(data => {
                    console.log("Received data:", data);
                    const gallery = document.querySelector('.gallery');
                    gallery.innerHTML = ''; // Clear existing images
        
                    data.images.forEach(image => {
                        const imageCard = document.createElement('div');
                        imageCard.classList.add('gallery-item');
        
                        const img = document.createElement('img');
                        img.src = image.url;
                        img.alt = image.title;
                        img.classList.add('gallery-image');
        
                        const imageDetails = document.createElement('div');
                        imageDetails.classList.add('gallery-item-info');
                        imageDetails.innerHTML = `
                            <div class="item-name">${image.title}</div>
                            <div class="item-date">${image.created_at}</div>
                        `;
        
                        imageCard.appendChild(img);
                        imageCard.appendChild(imageDetails);
                        gallery.appendChild(imageCard);
                        window.location.reload();
                    });
                })
                .catch(error => console.error('Error:', error));
            }

            function deleteSelectedImages() {
                if (selectedImages.size === 0) {
                    alert('Please select at least one image to delete.');
                    return;
                }
            
                // Show confirmation dialog
                const isConfirmed = window.confirm('Selected images will be permanently deleted. Are you sure?');
                if (!isConfirmed) {
                    return; // Stop if the user cancels
                }
            
                // Prepare data to send to the server
                const selectedImageIds = Array.from(selectedImages);
                const requestData = { selectedImageIds };
            
                // Send a POST request to the server
                fetch('/newapp/delete_selected_images/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken'),
                    },
                    body: JSON.stringify(requestData),
                    credentials: 'same-origin',
                })
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'success') {
                        // Reload the page or update the gallery to reflect the deletion
                        selectedImages.clear();
                        updateSelectedInfo();
                        updateImageGallery(); // Assuming this function reloads the image gallery
                    } else {
                        alert('Error deleting images: ' + data.message);
                    }
                })
                .catch(error => console.error('Error:', error));
            }
            
            
            function downloadSelectedImages() {
                if (selectedImages.size === 0) {
                    alert('Please select at least one image to download.');
                    return;
                }
                console.log('selectedImages ', selectedImages)
                const selectedImageIds = Array.from(selectedImages);
                fetch('/newapp/download_selected_images/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken'),
                    },
                    body: JSON.stringify({ selectedImageIds: Array.from(selectedImages) }),
                    credentials: 'same-origin',
                })
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }
                    return response.blob();
                })
                .then(blob => {
                    const url = window.URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = 'selected_images.zip';
                    document.body.appendChild(a);
                    a.click();
                    window.URL.revokeObjectURL(url);
                })
                .catch(error => console.error('Error:', error));
            }
            


            let selectedImages = new Set();

            function toggleSelection(item, imageId) {
                if (selectedImages.has(imageId)) {
                    selectedImages.delete(imageId);
                    item.classList.remove('selected');
                } else {
                    selectedImages.add(imageId);
                    item.classList.add('selected');
                }
                updateSelectedInfo();
            }

            function updateSelectedInfo() {
                document.getElementById('selected-count').innerText = selectedImages.size;
            }

            // Initialize total count on page load
            document.addEventListener('DOMContentLoaded', function() {
                updateSelectedInfo();
            });

            function selectAllImages() {
                const allItems = document.querySelectorAll('.gallery-item');
                const allSelected = selectedImages.size === allItems.length;
                
                allItems.forEach(item => {
                    const imageId = item.getAttribute('data-image-id');
                    
                    if (!allSelected) {
                        selectedImages.add(imageId);
                        item.classList.add('selected');
                    } else {
                        selectedImages.delete(imageId);
                        item.classList.remove('selected');
                    }
                });
                
                updateSelectedInfo(); // Update the count of selected images
            }
            
            
            
                    
    //  updateSelectedInfo();Update the count of selected images

        function toggleCheckboxSelection(checkbox, imageId) {
            if (checkbox.checked) {
                selectedImages.add(imageId);
            } else {
                selectedImages.delete(imageId);
            }
            updateSelectedInfo();
        }

        function updateConfidentiality(isConfidential) {
            if (selectedImages.size === 0) {
                alert('Please select at least one image.');
                return;
            }
            
            fetch('/newapp/update_image_confidentiality/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken'),
                },
                body: JSON.stringify({
                    image_ids: Array.from(selectedImages),
                    is_confidential: isConfidential
                }),
                credentials: 'same-origin',
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    alert('Confidentiality updated successfully.');
                    selectedImages.clear();
                    updateSelectedInfo();
                    // Optionally, refresh the gallery to reflect changes
                } else {
                    alert('Error updating confidentiality.');
                }
            })
            .catch(error => console.error('Error:', error));
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

// Then include 'X-CSRFToken': getCookie('csrftoken'), in your fetch headers
