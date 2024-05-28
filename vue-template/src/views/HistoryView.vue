<script lang="ts" setup>
import { onMounted, ref } from "vue";
import axios from "axios";
import { useRouter } from "vue-router";

const router = useRouter();
const history = ref([]);
const history_path = ref([]);

const loadHistory = async () => {
  await axios
    .get("/getHistory")
    .then((response) => {
      console.log(response);
      if (response.status === 200) {
        history.value = response.data.history.reverse();
        history_path.value.length = 0;
        history.value.forEach((img, i) => {
          history_path.value[i] = `/history/${img}`;
        });
      } else {
        throw "Unexpected returned status";
      }
    })
    .catch(function (error) {
      console.error(error);
    });
};

const requery = (image) => {
  console.log(image);
  router.push({ path: "/", query: { image: image } });
};

const removeHistory = async (image) => {
  await axios
    .get(`/removeHistory?image=${image}`)
    .then((response) => {
      console.log(response);
      if (response.status === 200) {
        history.value = response.data.history.reverse();
        history_path.value.length = 0;
        history.value.forEach((img, i) => {
          history_path.value[i] = `/history/${img}`;
        });
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
    <el-space wrap direction="vertical" alignment="start">
      <el-card
        class="history-card"
        v-for="(image, index) in history_path"
        :key="image.id"
      >
        <div class="history-div">
          <el-image
            class="history-image"
            fit="contain"
            :src="image"
            :preview-src-list="history_path"
            :initial-index="index"
          />
          <el-button type="success" @click="requery(history[index])" round>
            使用该记录重新查询
          </el-button>
          <el-button type="danger" @click="removeHistory(history[index])" round>
            删除该历史记录
          </el-button>
        </div>
      </el-card>
    </el-space>
  </div>
</template>

<style scoped>
.history-card {
  background: var(--vt-c-white);
  border: none;
}

.history-div {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
}

.history-image {
  transition: 0.3s;
  border-radius: 10px;
  width: auto;
  height: 200px;
  margin: 1rem;
}

@media (prefers-color-scheme: dark) {
  .history-card {
    background: var(--vt-c-black);
  }
}
</style>
