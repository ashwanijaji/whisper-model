const audioFile = document.getElementById('audioFile');
const transcribeButton = document.getElementById('transcribeButton');
const uploadProgress = document.getElementById('uploadProgress');
const result = document.getElementById('result');

transcribeButton.addEventListener('click', () => {
    const file = audioFile.files[0];
    if (!file) {
        alert("Please select an audio file to transcribe.");
        return;
    }

    const formData = new FormData();
    formData.append('file', file);

    const xhr = new XMLHttpRequest();
    xhr.upload.onprogress = (event) => {
        const percentComplete = (event.loaded / event.total) * 100;
        uploadProgress.value = percentComplete;
        uploadProgress.style.animation = ''; // Restarts the animation with the original settings

    };
    
    

    xhr.onload = () => {
        if (xhr.status === 200) {
            const response = JSON.parse(xhr.responseText);
            result.value = response.text;
            
         if (response.success) {  
            uploadProgress.value = 0; // Reset progress bar
            uploadProgress.style.animation = 'none'; // Stop the animation
         } 
        } else {
            console.error('Transcription error:', xhr.responseText);
            alert("An error occurred during transcription. Please try again.");
        }
    };
   // Add a download button element to your HTML (assuming an element with id="download-btn")
document.getElementById('download-btn').addEventListener('click', function() {
    const textToDownload = document.getElementById('result').textContent;

    // Send text to backend for download
    fetch('/download_text', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: textToDownload })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Download failed');
        } 
    })
    .catch(error => {
        console.error('Error downloading:', error);
        alert('There was a problem downloading the transcript.');
    });
});


    xhr.open('POST', '/transcribe');
    xhr.send(formData);
});
