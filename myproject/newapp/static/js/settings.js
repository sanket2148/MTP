
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

    document.addEventListener("DOMContentLoaded", function() {
        var deleteAccountBtn = document.getElementById("delete-account-btn");
        var confirmDeleteBtn = document.getElementById("confirm-delete-btn");
        var generateOtpBtn = document.getElementById("generate-otp-btn");
        var closeModalBtn = document.querySelector(".close");
        var modal = document.getElementById("delete-account-modal");
        var confirmationInput = document.getElementById("confirm-delete-input");
        var otpInput = document.getElementById("otp-input");
    
        closeModalBtn.onclick = function() {
            modal.style.display = "none";
        };
    
        window.onclick = function(event) {
            if (event.target == modal) {
                modal.style.display = "none";
            }
        };
    
        function hideModal() {
            if (modal) modal.style.display = "none";
        }
    
        deleteAccountBtn.onclick = function() {
            if (modal) modal.style.display = "block";
        };
    
        closeModalBtn.onclick = function() {
            hideModal();
        };
    
        window.onclick = function(event) {
            if (event.target == modal) {
                hideModal();
            }
        };
    
        confirmationInput.onkeyup = function() {
            if (confirmationInput.value.trim() === "DELETE MY ACCOUNT") {
                generateOtpBtn.style.display = "block";
            } else {
                generateOtpBtn.style.display = "none";
            }
        };
    
        generateOtpBtn.onclick = function() {
            fetch('/newapp/delete_account/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': getCookie('csrftoken'),
                },
                body: 'request_otp=true'
            })
            .then(response => response.json())
            .then(data => {
                console.log(data);
                if (data.success) {
                    alert("OTP has been sent to your email.");
                    otpInput.style.display = "block";
                    otpInput.focus();
                } else {
                    alert(data.error);
                }
            })
            .catch(error => {
                console.error('There was a problem with the OTP request:', error);
            });
        };
    
        confirmDeleteBtn.onclick = function() {
            if (confirmationInput.value.trim() === "DELETE MY ACCOUNT" && otpInput.value.trim()) {
                fetch('/newapp/delete_account/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                        'X-CSRFToken': getCookie('csrftoken'),
                    },
                    body: `confirmation_phrase=DELETE MY ACCOUNT&otp=${otpInput.value.trim()}`
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        alert(data.message);
                        window.location.href = "/newapp/create_account/";
                    } else {
                        alert(data.error);
                    }
                })
                .catch(error => {
                    console.error('There has been a problem with your fetch operation:', error);
                });
            } else {
                alert("Please type 'DELETE MY ACCOUNT' and enter the OTP.");
            }
        };
    });
    

    
    
    function changePreferredLanguage() {
        // Collect all checkbox inputs
        var selectedLanguages = document.querySelectorAll('input[name="languages"]:checked');
        var languageIds = Array.from(selectedLanguages).map(function(checkbox) {
            return checkbox.value;
        });
    
        // Use fetch to submit the form data to the server
        fetch('/newapp/change_preferred_language/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),
            },
            body: JSON.stringify({ language_ids: languageIds }),
        })
        .then(response => {
            if (response.ok) {
                alert("Preferred languages updated successfully!");
                // Optionally, refresh the page or redirect
            } else {
                alert("Failed to update preferred languages. Please try again.");
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert("An error occurred while updating preferred languages. Please try again later.");
        });
    }
    
