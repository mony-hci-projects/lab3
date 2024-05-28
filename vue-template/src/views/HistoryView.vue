<script lang="ts" setup>
import { onMounted, ref } from "vue";
import axios from "axios";

const history = ref([]);

const loadHistory = async () => {
  await axios
    .get("/getHistory")
    .then((response) => {
      console.log(response);
      if (response.status === 200) {
        history.value = response.data.history.reverse();
      } else {
        throw "Unexpected returned status";
      }
    })
    .catch(function (error) {
      console.error(error);
    });
};

onMounted(() => {
  loadHistory();
});
</script>

<template>
  <div class="history">
    <el-image
      v-for="(image, index) in history"
      fit="contain"
      :src="'/history/' + image"
      :preview-src-list="history"
      :initial-index="index"
      :key="image.id"
    />
    <!-- TODO: 使用历史记录进行查询 -->
    <!-- TODO: 删除历史记录 -->
  </div>
</template>

<style scoped>
.collections {
  display: flex;
  flex-wrap: wrap;
}
</style>
