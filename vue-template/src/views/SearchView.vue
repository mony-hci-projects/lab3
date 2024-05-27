<script setup lang="ts">
import { ref } from "vue";
import { genFileId } from "element-plus";
import { Star } from "@element-plus/icons-vue";
import axios from "axios";
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
  // upload.value.clearFiles();
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

const collectNewImage = async (image) => {
  try {
    const response = await axios.post("collect", image);
    return response.data;
  } catch (error) {
    console.error(error);
  }
}

function collectImage(image) {
  console.log(image);
  // JS 异步： https://segmentfault.com/a/1190000016788484
  // https://cloud.tencent.com/developer/article/2299760
  // GET 请求
  (async () => {
    try {
      const response = await axios.get("/collect?image=" + image);
      return response.data;
    } catch (error) {
      console.error(error);
      console.log("over");
    }
  })().then(data => {
      console.log(data);
    })

  // POST 请求
  collectNewImage({
    image: image,
  });
}
</script>

<template>
  <div>
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
    </div>
    <div id="loader" v-if="is_loading">
      <img id="loader_gif" src="@/assets/ajax-loader.gif" />
    </div>
    <div class="clear-button" v-if="display_clear">
      <el-button type="danger" @click="clear()" round>清空搜索结果</el-button>
    </div>
    <div id="searchresults" class="container" v-if="images.length > 0">
      <div id="resultscount">共搜索到 {{ images.length }} 条相关结果</div>
      <div class="results">
        <div
          class="result-div"
          v-for="(image, index) in images"
          :key="image.id"
        >
          <el-image
            class="result-image"
            fit="contain"
            :src="image"
            :preview-src-list="images"
            :initial-index="index"
          />
          <!--@contextmenu.prevent="console.log('clicked')"-->
          <el-button
            class="collect-button"
            type="warning"
            :icon="Star"
            @click="collectImage(image)"
            circle
          />
        </div>
      </div>
    </div>
    <div id="searchresults" class="container" v-else-if="is_error">
      {{ error_prompt }}
    </div>
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

.result-div {
  display: grid;
  grid-template-columns: 1fr;
  justify-items: center;
  margin: 10px;
}

.result-image {
  box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
  transition: 0.3s;
  border-radius: 10px;
  width: 200px;
  height: 200px;
}

.clear-button {
  display: grid;
  justify-items: center;
  padding: 2rem;
}

.collect-button {
  margin-top: 10px;
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

#loader {
  display: grid;
  justify-items: center;
  margin: 3rem auto;
}

#loader_gif {
  height: 50px;
  width: 50px;
}
</style>
