<script setup lang="ts">
import { ref } from "vue";
import { genFileId } from "element-plus";
import type { UploadInstance, UploadProps, UploadRawFile } from "element-plus";

const images = ref([]);
const display_clear = ref(false);
const is_loading = ref(false);
const is_error = ref(false);
const error_prompt = ref("不支持的图片格式：仅支持 PNG，JPG 或 JPEG 格式的图片查询");

const upload = ref<UploadInstance>();

const handleExceed: UploadProps['onExceed'] = (files) => {
  upload.value.clearFiles();
  const file = files[0] as UploadRawFile;
  file.uid = genFileId();
  upload.value!.handleStart(file);
}

const submitUpload = () => {
  is_loading.value = true;
  upload.value!.submit();
}

const handleSuccess = (response) => {
  images.value.length = 0;
  for (let i = 0; i < response.images.length; i++) {
    images.value[i] = response.images[i];
  }
  is_loading.value = false;
  is_error.value = false;
  display_clear.value = true;
}

const handleError = (response, file) => {
  is_loading.value = false;
  clear();
  is_error.value = true;
}

const handlePreview: UploadProps['onPreview'] = (file) => {
  console.log(file);
}

function clear() {
  images.value.length = 0;
  display_clear.value = false;
  is_error.value = false;
}
</script>

<template>
  <div id="main" class="container">
    <el-upload
      ref="upload"
      class="upload-demo"
      action="imgUpload"
      :limit="1"
      :auto-upload="false"
      :on-exceed="handleExceed"
      :on-success="handleSuccess"
      :on-error="handleError"
      :on-preview="handlePreview"
      list-type="picture"
    >
      <template #trigger>
        <el-button type="primary" round>选择一个文件</el-button>
      </template>
      <span v-for="i in 10" :key="i">&nbsp;</span>
      <el-button class="ml-3" type="success" @click="submitUpload" round>
        上传至服务器
      </el-button>
      <template #tip>
        <div class="el-upload__tip">
          limit 1 file, new file will cover the old file.
        </div>
      </template>
    </el-upload>
    <div>
      <el-button type="danger" v-if="display_clear" @click="clear()" plain>Clear</el-button>
    </div>
  </div>
  <center v-if="is_loading">
    <img id="loader_gif" src="@/assets/ajax-loader.gif" />
  </center>
  <div id="searchresults" class="container" v-if="images.length > 0">
    <div id="resultscount">共搜索到 {{ images.length }} 条相关结果</div>
    <div class="results">
      <img v-for="image in images" :src="image" :key="image.id" class="tdofimg" />
    </div>
  </div>
  <div id="searchresults" class="container" v-else-if="is_error">
    {{ error_prompt }}
  </div>
</template>

<style scoped>
.container {
  display: block;
}

.results {
  display: flex;
  flex-wrap: wrap;
}

.tdofimg {
  box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
  transition: 0.3s;
  width: 200px;
  height: 200px;
  padding-top: 10px;
  padding-bottom: 10px;
  padding-right: 10px;
  padding-left: 10px;
}

#resultscount {
  display: block;
  margin: 0 auto 1rem;
}

#searchresults {
  border: 1px;
  display: grid;
  grid-template-columns: 1fr;
  justify-items: center;
}

#loader_gif {
  height: 50px;
  width: 50px;
}
</style>
