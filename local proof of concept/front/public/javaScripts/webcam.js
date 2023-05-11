var canvas = document.querySelector("canvas");
var context = canvas.getContext("2d");
const video = document.querySelector('#myVidPlayer');

//w-width,h-height
var w, h;
canvas.style.display = "none";

function base64ToBlob(base64, mime) {
    mime = mime || '';
    var sliceSize = 1024;
    var byteChars = window.atob(base64);
    var byteArrays = [];

    for (var offset = 0, len = byteChars.length; offset < len; offset += sliceSize) {
        var slice = byteChars.slice(offset, offset + sliceSize);

        var byteNumbers = new Array(slice.length);
        for (var i = 0; i < slice.length; i++) {
            byteNumbers[i] = slice.charCodeAt(i);
        }

        var byteArray = new Uint8Array(byteNumbers);

        byteArrays.push(byteArray);
    }

    return new Blob(byteArrays, { type: mime });
}


function snapshot() {
    // Canvas creation
    context.fillRect(0, 0, w, h); // Give a proper size to the canvas
    context.drawImage(video, 0, 0, w, h); // Fill the canvas with the current frame
    canvas.style.display = "block"; // Show the canvas on the html site

    // Convert canvas contents (image) to a base64 string
    base64Image = canvas.toDataURL('image/png')
    // Convert base64 image to an image blob (image object)
    var base64ImageContent = base64Image.replace(/^data:image\/(png|jpg);base64,/, "");
    var blob = base64ToBlob(base64ImageContent, 'image/png');

    // This is the form that is going to be received by the server
    var formData = new FormData();
    formData.append('image', blob); // Add the image to the form to send
    filterValue = ""
    if(document.querySelector("#filter1").checked){
        filterValue = "filter1"
    }
    else if(document.querySelector("#filter2").checked){
        filterValue = "filter2"
    }
    else if(document.querySelector("#filter3").checked){
        filterValue = "filter3"
    }
    formData.append('filter', filterValue);
    formData.append('submit', "stream"); 

    // Create a connection and then send the form to the server with the POST method
    var xhr = new XMLHttpRequest();
    xhr.open('POST','/upload', false); //creates a conection to the URL
    xhr.send(formData);
}

// fuction to start recording with the webcam
var intervalId
function record(){
    intervalId = window.setInterval(function(){
        snapshot()
      }, 500);
}

// function to stop the video record
function stop_record(){
    clearInterval(intervalId)
}


window.navigator.mediaDevices.getUserMedia({ video: true, audio: true })
    .then(stream => {
        video.srcObject = stream;
        video.onloadedmetadata = (e) => {
            video.play();

            //new
            w = video.videoWidth;
            h = video.videoHeight

            canvas.width = w;
            canvas.height = h;
        };
    })
    .catch(error => {
        alert('You have to enable the mike and the camera');
    });

