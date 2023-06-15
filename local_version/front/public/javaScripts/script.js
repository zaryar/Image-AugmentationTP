// shows the uploaded image on the website
const image_input = document.querySelector("#image_input");
const video_input = document.querySelector("#video_input");
    var uploaded_image = "";
    var uploaded_video = "";
    image_input.addEventListener("change", function(){
        const reader = new FileReader();
        reader.addEventListener("load", () => {
            uploaded_image = reader.result;
            document.querySelector("#display_image").style.backgroundImage = `url(${uploaded_image})`;
        });
        reader.readAsDataURL(this.files[0]);
    })
    video_input.addEventListener("change", function(){
      const reader = new FileReader();
      reader.addEventListener("load", () => {
          uploaded_video = reader.result;
          document.querySelector("#display_image").style.backgroundImage = `url(${uploaded_video})`;
      });
      reader.readAsDataURL(this.files[0]);
  })



// javascript for dropdown menu    
var checkList = document.getElementById('list1');
checkList.getElementsByClassName('anchor')[0].onclick = function(evt) {
  if (checkList.classList.contains('visible'))
    checkList.classList.remove('visible');
  else
    checkList.classList.add('visible');
}
