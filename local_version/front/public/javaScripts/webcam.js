var canvas = document.querySelector("canvas");
var context = canvas.getContext("2d");
const video = document.querySelector('#myVidPlayer');

//w-width,h-height
var w, h;
canvas.style.display = "none";

// converts an base64 Image to a Blob 
// input: base64Image, mime type, output: Blob, mime type
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

// Gets the current frame of the webcam and sends it together with the form data (filter) to the server
function snapshot(name) {
    // Canvas creation
    context.fillRect(0, 0, w, h); // Give a proper size to the canvas
    context.drawImage(video, 0, 0, w, h); // Fill the canvas with the current frame
    canvas.style.display = "block"; // Show the canvas on the html site

    // Convert canvas contents (image) to a base64 string
    base64Image = canvas.toDataURL({
        format: 'jpeg',
        quality: 0.01
    });

    console.log("base64: " + base64Image.length)

    // Convert base64 image to an image blob (image object)
    var base64ImageContent = base64Image.replace(/^data:image\/(png|jpeg);base64,/, "");
    var blob = base64ToBlob(base64ImageContent, 'image/jpeg');

    console.log("blob: " + blob.toString.length)

    // This is the form that is going to be received by the server
    var formData = new FormData();
    formData.append('image', blob); // Add the image to the form to send


    filterValue = ""
    if (document.getElementById("1").checked) {
        filterValue = "1"
    }
    else if (document.getElementById("2").checked) {
        filterValue = "2"
    }
    else if (document.getElementById("3").checked) {
        filterValue = "3"
    }
    else if (document.getElementById("4").checked) {
        filterValue = "4"
    }
    else if (document.getElementById("5").checked) {
        filterValue = "5"
    }
    else if (document.getElementById("6").checked) {
        filterValue = "6"
    }
    else if (document.getElementById("7").checked) {
        filterValue = "7"
    }
    else if (document.getElementById("8").checked) {
        filterValue = "8"
    }
    else if (document.getElementById("9").checked) {
        filterValue = "9"
    }
    else if (document.getElementById("10").checked) {
        filterValue = "10"
    }
    else if (document.getElementById("11").checked) {
        filterValue = "11"
    }
    else if (document.getElementById("12").checked) {
        filterValue = "12"
    }
    else if (document.getElementById("13").checked) {
        filterValue = "13"
    }
    else if (document.getElementById("14").checked) {
        filterValue = "14"
    }
    else if (document.getElementById("15").checked) {
        filterValue = "15"
    }
    else if (document.getElementById("16").checked) {
        filterValue = "16"
    }
    else if (document.getElementById("17").checked) {
        filterValue = "17"
    }
    else if (document.getElementById("18").checked) {
        filterValue = "18"
    }
    else if (document.getElementById("19").checked) {
        filterValue = "19"
    }
    else if (document.getElementById("20").checked) {
        filterValue = "20"
    }
    formData.append('filter', filterValue);
    formData.append('submit', name);

    // Create a connection and then send the form to the server with the POST method
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/upload', false); //creates a conection to the URL
    //xhr.send("test");
    xhr.send(formData);
    var sended = new Date();
    var currentdate = new Date();
    console.log("Client -> Server: "
        + currentdate.getMinutes() + ":"
        + currentdate.getSeconds() + ":"
        + currentdate.getMilliseconds())
}

// fuction to start recording with the webcam
var intervalId
function record() {
    intervalId = window.setInterval(function () {
         snapshot("stream")
    }, 40);
}

// function to stop the video record
function stop_record() {
    clearInterval(intervalId)
    //the button was pushed -> send message to server 
    var formData = new FormData();
    formData.append('submit', "stopStream");
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/upload', false); //creates a conection to the URL
    xhr.send(formData);
}


window.navigator.mediaDevices.getUserMedia({ video: true, audio: true })
    .then(stream => {
        video.srcObject = stream;
        video.onloadedmetadata = (e) => {
            video.play();

            //new
            w = 700;
            h = 500

            canvas.width = w;
            canvas.height = h;
        };
    })
    .catch(error => {
        alert('You have to enable the mike and the camera');
    });

