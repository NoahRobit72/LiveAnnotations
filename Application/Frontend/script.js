// script.js


const video = document.getElementById('video');

navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => {
        video.srcObject = stream;
    })
    .catch(error => {
        console.error('Error accessing the camera: ', error);
    });

async function fetchAndUpdatePosition() {
    try {
        // Fetch the API response
        const response = await fetch('http://127.0.0.1:8080/update_coordinates');
        if (!response.ok) {
            throw new Error('Network response was not ok ' + response.statusText);
        }

        // Parse the JSON data
        const data = await response.json();
        console.log(data)

        // Extract x and y from the data
        // const { x, y } = data;
        const x = data["left"]
        const y = data["top"]


        // Get the overlay element
        const overlayElement = document.getElementById('overlay');

        // Update the top and left attributes
        overlayElement.style.top = `${y}px`;
        overlayElement.style.left = `${x}px`;

    } catch (error) {
        console.error('There has been a problem with your fetch operation:', error);
    }
}

// Fetch new coordinates every 5 seconds
setInterval(fetchAndUpdatePosition, 1000);