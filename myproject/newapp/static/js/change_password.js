var userEmail = "{{ user.email }}"; // Assuming 'user' is the context variable representing the logged-in user.
    
        async function requestOTP() {
            // Use userEmail for the OTP request
            const response = await fetch(`/newapp/request_otp/?email=${userEmail}`);
            const data = await response.json();
            alert(data.message);
        }
    
        async function verifyAndResetPassword() {
            const otp = document.getElementById("otp").value;
            const newPassword = document.getElementById("newPasswordOTP").value;
            const confirmNewPassword = document.getElementById("confirmNewPasswordOTP").value;

            if (newPassword !== confirmNewPassword) {
                alert("New passwords do not match.");
                return;
            }
    
            const response = await fetch('/newapp/verify_reset_password/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken'), // Make sure to handle CSRF token
                },
                body: JSON.stringify({ email: userEmail, otp, newPassword }),
            });
            const data = await response.json();
            alert(data.message);
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
        async function changePasswordWithOld() {
            const oldPassword = document.getElementById("oldPassword").value;
            const newPassword = document.getElementById("newPassword").value;
            const confirmNewPassword = document.getElementById("confirmNewPassword").value;

            if (newPassword !== confirmNewPassword) {
                alert("New passwords do not match.");
                return;
            }
        
            // Assuming you have a URL to change the password with the old password
            const response = await fetch('/newapp/change_password_with_old/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken'),
                },
                body: JSON.stringify({ oldPassword, newPassword }),
            });
            const data = await response.json();
            alert(data.message);
            if (data.status === "success") {
                // Password changed successfully
                location.reload(); // or redirect to a confirmation page
            }
        }