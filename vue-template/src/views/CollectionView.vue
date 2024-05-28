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
    <el-space wrap>
      <el-card
        class="collection-card"
        v-for="(image, index) in collections"
        :key="image.id"
      >
        <div class="collection-div">
          <el-image
            class="collection-image"
            fit="contain"
            :src="image"
            :preview-src-list="collections"
            :initial-index="index"
          />
          <el-button type="danger" @click="removeColletion(image)" round>
            取消收藏
          </el-button>
        </div>
      </el-card>
    </el-space>
  </div>
</template>

<style scoped>
.collection-card {
  background: var(--vt-c-white);
  border: none;
}

.collection-div {
  display: grid;
  grid-template-columns: 1fr;
  justify-items: center;
}

.collection-image {
  transition: 0.3s;
  border-radius: 10px;
  width: auto;
  height: 200px;
  margin-bottom: 1rem;
}

@media (prefers-color-scheme: dark) {
  .collection-card {
    background: var(--vt-c-black);
  }
}
</style>
