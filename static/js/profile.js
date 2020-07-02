function encodeBase64ImgFile(e) {
  let files = e.target.files;
  let filesArr = Array.prototype.slice.call(files);

  filesArr.forEach(function(f) {
    let reader = new FileReader();

    reader.onload = function(e) {
      $("#profile_img").attr('src', e.target.result).css({"display": "unset"});
      $("#profile").attr("value", e.target.result);
      console.log(e.target.result);
    }
    reader.readAsDataURL(f);
  });
}

document.addEventListener("DOMContentLoaded", function() {
  $("#profile").on("change", encodeBase64ImgFile);
});