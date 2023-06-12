//libraries
const path = require('path');
const fs = require("fs");
const { convertArrayToCSV } = require('convert-array-to-csv');

// create express server
const express = require('express');
const app = express();
const http = require('http');
const server = http.createServer(app);

// create socket.io
const { Server } = require("socket.io");
const io = new Server(server);

// function to tell the socket what to do if a user connects 
io.on('connection', (socket) => {
    console.log('a user connected');

    setInterval(sendLatestFile, 40);
});



app.use(express.static('public'));  /* tells expressJS where to find css and js files */

// function that gives the name to the new files added to input
const multer = require('multer');
const { Console } = require('console');
const { type } = require('os');
var i = 0;
const storage = multer.diskStorage({
    destination: (req, file, cb) => {
        cb(null, 'public/images/input')
    },
    filename: (req, file, cb) => {
        if (path.extname(file.originalname) == ".mp4"){
            cb(null, "video" + path.extname(file.originalname))
            console.log("saved video");
        }
        else if (path.extname(file.originalname).length > 0) {
            cb(null, "image" + path.extname(file.originalname))
            console.log("saved img");
        } else {
            if (!fs.existsSync('public/images/input/frame.png')) {
                console.log(file)
                console.log("frame created")
                cb(null, "frame.png")
            }
            else {
                console.log("frame allready there" + i)
                i++
                cb(null, ".ignore")

            }
        }
    }
})

const upload = multer({ storage: storage }) //function to save the image sent

app.get("/upload", (req, res) => {
    res.sendFile(__dirname + '/main.html'); //function send the user to main.html when they open the webpage
});

// Gets called when a post request is send 

var updateData = ""
var updateFilter = ""
app.post("/upload", upload.single('image'), (req, res) => {
    if (req.body.submit == "normal_image" || req.body.submit == "stream" || req.body.submit == "video") {
        updateData = req.body.submit
        filterNumber = req.body.filter
        
        if (typeof filterNumber === 'string') {
            updateFilter = filterNumber
        }else{
            updateFilter = "none"
        }
    }

    const header = [updateData];
    var dataArrays = [
        [updateFilter]
    ];
    
    const csvFromArrayOfArrays = convertArrayToCSV(dataArrays, {
        header,
        separator: ','
    });

    //create stopStream.txt file
    if (req.body.submit == "stopStream") {
        fs.writeFile("public/stopStream.txt", ",", err => {
            if (err) {
                console.err;
                return;
            }
        })
    }
    
    fs.writeFile("public/config.csv", csvFromArrayOfArrays, err => {
        if (err) {
            console.err;
            return;
        }
    })

    if (updateData != "stream") {

        setTimeout(function () {
            res.sendFile(__dirname + '/main.html');
        }, 1000);
    } else {
        // In case of a stream, we donÇt want the website to reload
        res.send(null)
    }
})

// upload images in livetime
let filePath = __dirname + '/public/images/output/frame.png';

//fs.watchFile(filePath, { interval: 70 }, sendLatestFile);


function sendLatestFile() {
    fs.readFile(filePath, function (err, buf) {
        if (fs.existsSync("public/images/output/frame.png")) {
            //console.log("512313");
            try {
                let imgData = buf.toString('base64');
                io.emit('update', { image: imgData });
                fs.unlinkSync("public/images/output/frame.png");
            } catch (error) {
                console.error(error);
            }

        }
    });
}

app.use(express.static('public'));

server.listen(3001);
console.log("3001 is the port");