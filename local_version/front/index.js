//libraries
const path = require('path');
const fs = require("fs");
const { convertArrayToCSV } = require('convert-array-to-csv');

const INPUTFRAME = 'public/images/input/frame.jpg';
const OUTPUTFRAME = 'public/images/output/frame.jpg';
const LOCKOUT = 'public/images/output/lockOut';

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
    //setInterval(sendLatestFile, 40);
});

function Sleep(milliseconds) {
    return new Promise(resolve => setTimeout(resolve, milliseconds));
}



app.use(express.static('public'));  /* tells expressJS where to find css and js files */

// function that gives the name to the new files added to input
const multer = require('multer');
const { Console } = require('console');
const { type } = require('os');
var i = 0;
const storage = multer.diskStorage({
    destination: (req, file, cb) => {
        cb(null, 'public/images/input');
    },
    filename: async (req, file, cb) => {
        if (path.extname(file.originalname).length > 0) {
            const extension = path.extname(file.originalname).substring(1).toLowerCase();
            if (['mp4', 'mov', 'avi', 'mkv'].includes(extension)) {
                cb(null, 'video' + path.extname(file.originalname));
                console.log('Saved video');
            } else {
                cb(null, 'image' + path.extname(file.originalname));
                console.log('Saved image');
            }
        } else {
            // saves Frame if its not found in input (this happends when the python script is done using the image)
            if (!fs.existsSync(INPUTFRAME)) {
                console.log(file)

                cb(null, "frame.jpg")
                console.log("frame ")
            // else it ignores the frame
            }
            else {
                console.log("frame allready there" + i)
                i++
                cb(null, ".ignore")

            }
        }
        sendLatestFile()
    }
});

const upload = multer({ storage: storage }) //function to save the image sent

app.get("/upload", (req, res) => {
    res.sendFile(__dirname + '/main.html'); //function send the user to main.html when they open the webpage
});

// Gets called when a post request is send, fills the config.csv with information about the filter and the type of data
var updateData = ""
var updateFilter = ""
var filterCategory = ""
app.post("/upload", upload.single('image'), (req, res) => {
    if (req.body.submit == "image" || req.body.submit == "video" || req.body.submit == "stream") {
        updateData = req.body.submit
        filterNumber = req.body.filter

        if (typeof filterNumber === 'string') {
            updateFilter = "filter" + filterNumber
        } else {
            updateFilter = "none"
        }

        if (parseInt(filterNumber) <= 13) {
            filterCategory = "NormalFilter"
        }
        else if (parseInt(filterNumber) <= 16) {
            filterCategory = "StyleTransfer"
        }
        else {
            filterCategory = "FaceRecognition"
        }
    }

    const header = [updateData];
    var dataArrays = [
        [updateFilter],
        [filterCategory]
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


//fs.watchFile(filePath, { interval: 70 }, sendLatestFile);


function sendLatestFile() {
    fs.readFile(OUTPUTFRAME, function (err, buf) {
        if (fs.existsSync(LOCKOUT)) {
            try {
                let imgData = buf.toString('base64');
                io.emit('update', { image: imgData });
                var currentdate = new Date();
                console.log("serverDisplayedOnCanvis: "
                    + currentdate.getMinutes() + ":"
                    + currentdate.getSeconds() + ":"
                    + currentdate.getMilliseconds())
                fs.unlinkSync(LOCKOUT);
            } catch (error) {
                console.error(error);
            }

        }
    });
}

app.use(express.static('public'));

server.listen(3001);
console.log("3001 is the port");
