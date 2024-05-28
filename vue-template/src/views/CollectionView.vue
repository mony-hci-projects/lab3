<script lang="ts" setup>
import { onMounted, ref } from "vue";
import axios from "axios";

const collections = ref([]);

const loadCollection = async () => {
  await axios
    .get("/getCollection")
    .then((response) => {
      console.log(response);
      if (response.status === 200) {
        collections.value = response.data.collection;
      } else {
        throw "Unexpected returned status";
      }
    })
    .catch(function (error) {
      console.error(error);
    });
};

const removeColletion = (image) => {
  // TODO: 修改 static 目录地址
  axios
    .get(`/changeCollection?image=${image}&operation=remove`)
    .then((response) => {
      console.log(response);
    })
    .catch(function (error) {
      console.error(error);
    });
  loadCollection();
};

onMounted(() => {
  loadCollection();
});
</script>

<template>
  <div class="collections">
    <el-space>
      <el-card v-for="(image, index) in collections" :key="image.id">
        <el-image
          fit="contain"
          :src="image"
          :preview-src-list="collections"
          :initial-index="index"
        />
        <el-button type="danger" @click="removeColletion(image)" round>
          取消收藏
        </el-button>
      </el-card>
    </el-space>
    <!-- TODO: 删除收藏 -->
  </div>
</template>

<style scoped>
.collections {
  display: flex;
  flex-wrap: wrap;
}
</style>
