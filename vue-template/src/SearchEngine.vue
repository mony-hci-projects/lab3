<script setup>
import { ref } from "vue";
import $ from "jquery";

const images = ref([]);
const display_clear = ref(false);
const is_loading = ref(false);

function clear() {
  images.value.length = 0;
  display_clear.value = false;
}

function fun() {
  is_loading.value = true;
  $("form").submit(function (event) {
    event.preventDefault();

    var formData = new FormData($(this)[0]);

    $.ajax({
      url: "imgUpload",
      type: "POST",
      data: formData,
      //async: false,
      cache: false,
      contentType: false,
      enctype: "multipart/form-data",
      processData: false,

      success: function (response) {
        images.value.length = 0;
        for (var i = 0; i < response.images.length; i++) {
          images.value[i] = response.images[i];
        }
        is_loading.value = false;
        display_clear.value = true;
      },
    });
    return false;
  });
}
</script>

<template>
  <header>
    <h1>Image Search Engine Demo</h1>
    <img
      alt="logo"
      class="logo"
      src="@/assets/tju.ico"
      width="32"
      height="32"
    />
  </header>

  <div id="main" class="container">
    <form method="post" enctype="multipart/form-data">
      <input type="file" name="file" @change="myFunction()" required />
      <input type="submit" value="Search!" @click="fun()" />
      <span width="36em"></span>
    </form>
    <a><button v-if="display_clear" @click="clear()">Clear</button></a>
  </div>
  <center v-if="is_loading">
    <img
      id="load"
      src="@/assets/ajax-loader.gif"
      height="100px"
      width="100px"
    />
  </center>
  <div id="searchresults" class="container" v-if="images.length > 0">
    <div id="resultscount">共搜索到 {{ images.length }} 条相关结果</div>
    <div class="results" v-for="image in images" :key="image.id">
      <img :src="image" class="tdofimg" />
    </div>
  </div>
</template>

<style scoped>
header {
  line-height: 1.5;
  max-height: 100vh;
  margin-top: 1rem;
}

.logo {
  display: block;
  margin: 0 auto 1rem;
}

.container {
  display: block;
}

.results {
  display: flex;
  flex-wrap: wrap;
}

#resultscount {
  display: block;
  margin: 0 auto 1rem;
}

#searchresults {
  border: 1px;
  width: 70%;
  display: grid;
  grid-template-columns: 1fr;
  -ms-grid-column-align: center;
}

.tdofimg {
  box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
  transition: 0.3s;
  width: 200px;
  height: 200px;
  padding-top: 0px;
  padding-bottom: 0px;
  padding-right: 0px;
  padding-left: 0px;
  border-left-width: 1px;
  border-bottom-width: 1px;
  border-right-width: 1px;
}

.tdofimg img {
  all: inherit;
  /*box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
transition: 0.3s;
width: 200px;
height: 200px;*/
  padding-top: 5px;
  padding-bottom: 5px;
  padding-right: 0px;
  padding-left: 5px;
  border-left-width: 0px;
  border-bottom-width: 0px;
  border-right-width: 0px;
}
</style>
