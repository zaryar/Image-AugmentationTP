//library
const express = require("express");
const app = express();
const path = require('path');
const fs = require("fs");
const { convertArrayToCSV } = require('convert-array-to-csv');
//

app.use(express.static('public'));  /* tells expressJS where to find css and js files */

// function that gives the name to the new files added to input
var i = 0;
const multer = require('multer');
const storage = multer.diskStorage({
    destination: (req, file, cb) => {
        cb(null, 'public/images/input')
    },
    filename: (req, file, cb) => {
        console.log(file)
        // cb(null, Date.now() + path.extname(file.originalname))
        if (path.extname(file.originalname).length > 0) {
            cb(null, "image" + path.extname(file.originalname))
        } else {
            cb(null, "frame" + i + ".png")
            i++;
            if(i > 25){
                i = 0
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
    // res.status(204).send();
    //update configData
    if (req.body.submit == "image" || req.body.submit == "snapshot" || req.body.submit == "stream" || req.body.submit == "video") {
        updateData = req.body.submit
        if (req.body.filter == "filter1") {
            updateFilter = "filter1"
        } else if (req.body.filter == "filter2") {
            updateFilter = "filter2"
        } else if (req.body.filter == "filter3"){
            updateFilter = "filter3"
        }else{
            updateFilter = "none"
        }    
    }
    const header = ['format', 'filter'];
    const dataArrays = [
        [updateData, updateFilter]
    ];

    const csvFromArrayOfArrays = convertArrayToCSV(dataArrays, {
        header,
        separator: ','
    });
    
    fs.writeFile("public/config.csv", csvFromArrayOfArrays, err => {
        if (err) {
            console.err;
            return;
        }
    })

    fs.writeFile("public/configData.txt", updateData + " ," + updateFilter, err => {
        if (err) {
            console.err;
            return;
        }
    })
    if (updateData != "stream") {
        res.sendFile(__dirname + '/main.html');
    } else {
        // In case of a stream, we donÇt want the website to reload
        res.send(null)
    }
})

app.use(express.static('public'));

app.listen(3001);
console.log("3001 is the port");