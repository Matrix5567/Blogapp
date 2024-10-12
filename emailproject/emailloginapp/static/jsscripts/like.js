function  function1(id) {
console.log("bicalled>>>>>>>>>",id)
$.get("http://localhost:3000/sample", function(data,status)   //get
{
const imgcontainer  = document.getElementById("image-container")
data.forEach(image => {
  const img = document.createElement("img")
  img.src = image
  imgcontainer.appendChild(img)
  });
});
}