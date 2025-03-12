document.addEventListener('DOMContentLoaded', function() {
    const micButton = document.querySelector('.mic-button');
    const waveContainer = document.querySelector('.wave-container');
    const recognizedText = document.querySelector('.recognized-text');
    const assistantResponse = document.querySelector('.assistant-response');
    const wave = document.querySelector('.wave');
    let isListening = false;

    // Function to start wave animation
    function startWaveAnimation() {
        wave.style.animation = 'wave 1.5s ease-in-out infinite';
        waveContainer.style.display = 'block';
    }

    // Function to stop wave animation
    function stopWaveAnimation() {
        wave.style.animation = 'none';
        waveContainer.style.display = 'none';
    }

    micButton.addEventListener('click', async function() {
        if (!isListening) {
            // Start listening
            isListening = true;
            micButton.classList.add('listening');
            recognizedText.textContent = 'Listening...';
            assistantResponse.textContent = '';
            startWaveAnimation();

            try {
                const response = await fetch('/process', {
                    method: 'POST'
                });
                const data = await response.json();

                if (data.error) {
                    recognizedText.textContent = data.error;
                    assistantResponse.textContent = '';
                } else {
                    recognizedText.textContent = data.user_input;
                    assistantResponse.textContent = data.response;
                }
            } catch (error) {
                recognizedText.textContent = 'Error: Could not process request';
                assistantResponse.textContent = '';
            } finally {
                // Stop listening state
                isListening = false;
                micButton.classList.remove('listening');
                stopWaveAnimation();
            }
        }
    });
});

document.getElementById("recordButton").addEventListener("click", function () {
    // Show waves and start listening
    document.getElementById("recognizedText").innerText = "Listening...";
    document.querySelectorAll(".wave").forEach(wave => wave.style.opacity = "1");

    // Call backend API to trigger Python code
    fetch("/process", { method: "POST" })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                document.getElementById("recognizedText").innerText = "Error: " + data.error;
            } else {
                document.getElementById("recognizedText").innerText = `You said: "${data.user_input}"`;
                document.getElementById("assistantResponse").innerText = "Assistant: " + data.response;
            }
            // Hide waves after getting response
            document.querySelectorAll(".wave").forEach(wave => wave.style.opacity = "0");
        })
        .catch(error => {
            // Hide waves if there's an error
            document.querySelectorAll(".wave").forEach(wave => wave.style.opacity = "0");
            document.getElementById("recognizedText").innerText = "Error: Could not process request";
        });
});
