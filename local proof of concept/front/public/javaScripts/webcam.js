// window.onload = function () { //function that makes the js code wait until the html code finishes loading//
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

//new
function snapshot() {
    context.fillRect(0, 0, w, h);
    context.drawImage(video, 0, 0, w, h);
    canvas.style.display = "block";

    // Canvas has a base64 image now
    base64Image = canvas.toDataURL('image/png')
    var base64ImageContent = base64Image.replace(/^data:image\/(png|jpg);base64,/, "");
    var blob = base64ToBlob(base64ImageContent, 'image/png');


    var formData = new FormData();
    formData.append('image', blob);

    var xhr = new XMLHttpRequest();
    xhr.open('POST','/upload', false);
    xhr.send(formData);

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

// };