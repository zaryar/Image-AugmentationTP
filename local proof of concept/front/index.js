const express = require("express");
const app = express();
const path = require('path');
const fs = require("fs");
app.use(express.static('public'));  /* tells expressJS where to find css and js files */

const multer = require('multer');
const storage = multer.diskStorage({
    destination: (req, file, cb) => {
        cb(null, 'public/images/input')
    },
    filename: (req, file, cb) => {
        console.log(file)
        // cb(null, Date.now() + path.extname(file.originalname))
        if (path.extname(file.originalname).length > 0) {
            cb(null, "test" + path.extname(file.originalname))
        } else {
            cb(null, "test.png")
        }
    }
})

const upload = multer({ storage: storage })

app.get("/upload", (req, res) => {
    res.sendFile(__dirname + '/main.html');
});


var updateData = ""
var updateFilter = ""
app.post("/upload", upload.single('image') ,(req, res) => {
    // res.send("Image Uploader");
    // res.status(204).send();
    if(req.body.submit == "image"){
         updateData = "image"
         if(req.body.filter == "filter1")
         {
            updateFilter = "filter1"
         }else if (req.body.filter == "filter2") {
            updateFilter = "filter2"
         }else{
            updateFilter = "filter3"
         }
    }
    if(req.body.submit == "video"){
        updateData = "video"
        if(req.body.filter == "filter1")
         {
            updateFilter = "filter1"
         }else if (req.body.filter == "filter2") {
            updateFilter = "filter2"
         }else{
            updateFilter = "filter3"
         }
   }
    fs.writeFile("public/configData.txt", updateData + " ," + updateFilter , err => {
        if(err){
            console.err;
            return;
        }
    })
    res.sendFile(__dirname + '/main.html');
})


app.use(express.static('public'));

app.listen(3001);
console.log("3001 is the port");