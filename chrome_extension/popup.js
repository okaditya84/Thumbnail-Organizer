document.getElementById('download_button').addEventListener('click', function() {
    const youtubeUrl = document.getElementById('youtube_url').value;
    
    if (youtubeUrl) {
        // Send the URL to the Flask server
        fetch('http://localhost:5000/download_thumbnail', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ youtube_url: youtubeUrl }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Show the downloaded thumbnail
                const img = document.getElementById('thumbnail');
                img.src = data.thumbnail_url;
                img.style.display = 'block';
                document.getElementById('message').innerText = "Thumbnail downloaded!";
            } else {
                document.getElementById('message').innerText = "Failed to download thumbnail.";
            }
        })
        .catch(error => {
            console.error('Error:', error);
            document.getElementById('message').innerText = "Error downloading thumbnail.";
        });
    } else {
        document.getElementById('message').innerText = "Please enter a YouTube URL.";
    }
});
