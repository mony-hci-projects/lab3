<script setup lang="ts">
import { onMounted, ref } from "vue";
import { genFileId } from "element-plus";
import { Star } from "@element-plus/icons-vue";
import axios from "axios";
import { useRoute } from "vue-router";
import type { UploadInstance, UploadProps, UploadContentProps, UploadRawFile } from "element-plus";

const route = useRoute();
const images = ref([]);
const display_clear = ref(false);
const is_loading = ref(false);
const is_error = ref(false);
const error_prompt = ref("不支持的图片格式：仅支持 PNG，JPG 或 JPEG 格式的图片查询");
const result_number = ref(0);
const relevance = ref(60);

const upload = ref<UploadInstance>();

const handleExceed: UploadProps['onExceed'] = (files) => {
  upload.value.clearFiles();
  const file = files[0] as UploadRawFile;
  file.uid = genFileId();
  upload.value!.handleStart(file);
}

const submitUpload = async () => {
  await axios
    .get(`/newparameters?number=${result_number.value}&relevance=${relevance.value}`)
    .then(response => {console.log(response);})
    .catch(function (error) {
      console.log(error);
    });
  is_loading.value = true;
  upload.value!.submit();
}

const handleSuccess: UploadContentProps['onSuccess'] = (response) => {
  images.value.length = 0;
  for (let i = 0; i < response.images.length; i++) {
    images.value[i] = response.images[i];
  }
  is_loading.value = false;
  is_error.value = false;
  display_clear.value = true;
}

const handleError = (response, file) => {
  switch (response.status) {
    case 400:
      error_prompt.value = "错误请求：可能是图片上传错误或上传了不支持的图片格式。本网站仅支持 PNG，JPG 或 JPEG 格式的图片查询";
      break;
    case 500:
      error_prompt.value = "服务器出现错误，请稍后重试";
      break;
    default:
      error_prompt.value = "未知错误，请稍后重试";
  }
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

function collectImage(image) {
  console.log(image);
  // JS 异步： https://segmentfault.com/a/1190000016788484
  // 一个并不好用的示例： https://cloud.tencent.com/developer/article/2299760
  // GET 请求
  axios
    .get(`/changeCollection?image=${image}&operation=new`)
    .then((response) => {
      console.log(response);
    })
    .catch(function (error) {
      console.error(error);
    });
}

onMounted(() => {
  if (!route.query.image) {
    return ;
  }
  axios
    .get(`/imgUpload?image=${route.query.image}`)
    .then((response) => {
      if (response.status === 200) {
        images.value.length = 0;
        for (let i = 0; i < response.data.images.length; i++) {
          images.value[i] = response.data.images[i];
        }
        is_loading.value = false;
        is_error.value = false;
        display_clear.value = true;
      }
    })
    .catch(function (error) {
      console.error(error);
    });
});
</script>

<template>
  <div>
    <div class="container">
      <el-upload
        ref="upload"
        class="upload-box"
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
        <!--<span v-for="i in 10" :key="i">&nbsp;</span>-->
        <el-button class="ml-3" type="success" @click="submitUpload" round>
          上传至服务器
        </el-button>
        <template #tip>
          <div class="el-upload__tip">
            limit 1 file, new file will cover the old file.
          </div>
        </template>
        <div>
          搜索结果相关性：<el-input-number v-model="relevance" :max="100" :min="40" :step="10" />
        </div>
        <div>
          搜索结果数量限制：<el-input-number v-model="result_number" :min="0" :step="20" />（数量为零时不对搜索结果数量进行限制）
        </div>
        <div class="clear-button" v-if="display_clear">
          <el-button type="danger" @click="clear()" round>清空搜索结果</el-button>
        </div>
      </el-upload>
    </div>
    <div id="loader" v-if="is_loading">
      <img id="loader_gif" src="@/assets/ajax-loader.gif" />
    </div>
    <div id="searchresults" class="container" v-if="images.length > 0">
      <div id="resultscount">共搜索到 {{ images.length }} 条相关结果</div>
      <div class="results">
        <div class="result-div" v-for="(image, index) in images" :key="image.id">
          <el-image
            class="result-image"
            fit="contain"
            :src="image"
            :preview-src-list="images"
            :initial-index="index"
          />
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

.upload-box div, .upload-box button {
  margin: 0.5em 1em;
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
  width: auto;
  height: 200px;
}

/*.clear-button {
  display: grid;
  justify-items: center;
  padding: 2rem;
}*/

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
