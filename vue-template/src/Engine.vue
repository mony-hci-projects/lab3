<script setup>
import $ from 'jquery'

function fun(){
  $('#load').show();
  $("form").submit(function(evt){
    evt.preventDefault();
    var searchresults = document.getElementById("searchresults");

    //$('#loader-icon').show();
    var formData = new FormData($(this)[0]);

    $.ajax({
      url: 'imgUpload',
      type: 'POST',
      data: formData,
      //async: false,
      cache: false,
      contentType: false,
      enctype: 'multipart/form-data',
      processData: false,

      success: function (response) {
        $('#load').hide();
        $('#row1').show();
        //$('#clear').show();
        $("#searchresults").empty();
        for (var i = 0; /*i < 9 &&*/ i < response.images.length; i++) {
          var new_img = document.createElement("img");
          new_img.src = response.images[i];
          new_img.alt = "Norway";

          var img_div = document.createElement("div");
          img_div.className = "tdofimg";
          img_div.appendChild(new_img)

          searchresults.appendChild(img_div);
        }
        $('#table').show();
        $('#clear').show();
      }
    });
    return false;
  })
};
</script>

<template>
  <header>
    <img
    alt="logo"
    class="logo"
    src="@/assets/tju.ico"
    width="32"
    height="32"
  />
    <h1>Image Search Engine Demo</h1>
  </header>

  <div id="main" class="container">
    <form method=post enctype=multipart/form-data>
      <input type="file" name="file" required @change="myFunction()"/>
      <input type=submit value ="Search!" @click="fun()">
      <span width="36em"></span>
    </form>
    <a href=""><button id="clear">Clear</button></a>
  </div>
  <center>
    <img id="load" src="@/assets/ajax-loader.gif" style="height:100px;weight:100px;display:none;" >
  </center>
  <div id="searchresults" class="container"></div>
</template>

<style scoped>
header {
  line-height: 1.5;
  max-height: 100vh;
}

.logo {
  display: block;
  margin: 0 auto 1rem;
}
</style>
