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
                    });
                })
                .catch(error => console.error('Error:', error));
            }

            function downloadSelectedImages() {
                const formData = new FormData(document.getElementById('image-actions-form'));
                formData.append('action', 'download');
                fetch('/newapp/download_images/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrftoken, // Ensure you have CSRF token available
                    },
                    body: JSON.stringify({ selectedImageIds }),
                    credentials: 'same-origin', // Necessary for including CSRF token
            
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
                    a.download = "selected_images.zip";
                    document.body.appendChild(a);
                    a.click();
                    window.URL.revokeObjectURL(url);
                    alert('Your download has started.');
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
                    return; // Stop if user cancels
                }
                const formData = new FormData(document.getElementById('image-actions-form'));
                formData.append('action', 'delete');
                fetch('/newapp/delete_images/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrftoken, // Ensure you have CSRF token available
                    },
                    body: formData,
                    credentials: 'same-origin',
                }).then(response => response.json())
                  .then(data => {
                      if (data.status === 'success') {
                          // Reload the page or update the gallery to reflect the deletion
                          selectedImages.clear();
                          location.reload(); // Simplest way to refresh the page
                      } else {
                          alert('There was a error deleting images.');
                      }
                  }).catch(error => console.error('Error:', error));
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
                const allSelected = allItems.length === selectedImages.size;

                allItems.forEach(item => {
                    const imageId = item.getAttribute('data-image-id');
                    
                    if (allSelected) {
                        // If all were selected, deselect them
                        selectedImages.delete(imageId);
                        item.classList.remove('selected');
                    } else {
                        // If not all were selected, select them
                        selectedImages.add(imageId);
                        item.classList.add('selected');
                    }
                });
                    
    //  updateSelectedInfo();Update the count of selected images
}
