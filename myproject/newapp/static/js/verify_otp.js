    let countdown = 120; // Countdown duration in seconds
    const timerDisplay = document.getElementById("timer");
    let timerInterval;

    function countdownTimer() {
        const minutes = Math.floor(countdown / 60);
        const seconds = countdown % 60;

        // Update the display with the current time
        timerDisplay.textContent = `Resend OTP in: ${minutes}m ${seconds.toString().padStart(2, '0')}s`;

        if (countdown <= 0) {
            clearInterval(timerInterval); // Stop the countdown
            document.getElementById("resendOTP").disabled = false; // Enable the resend button
            timerDisplay.textContent = ""; // Clear the countdown display
        } else {
            countdown--; // Decrease the countdown
        }
    }

    function resendOTP() {
        fetch('/newapp/resend_otp/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'), // Ensure CSRF token is sent
                'Content-Type': 'application/json'
            },
        })
        .then(response => response.json())
        .then(data => {
            if(data.status === 'success') {
                alert("OTP has been resent. Please check your email.");
            } else {
                alert("Failed to resend OTP. Please try again later.");
            }
        })
        .catch((error) => {
            console.error('Error:', error);
            alert("Failed to resend OTP. Please try again later.");
        });
    }
    
    // Helper function to get CSRF token
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


    // Call the countdownTimer function to start the countdown immediately
    countdownTimer();
