import { createApp } from "vue";
//import App from "./App.vue";
import SearchEngine from "./SearchEngine.vue";
import router from "./router";
import axios from "axios";
import VueAxios from "vue-axios";

import "./assets/main.css";

const app = createApp(SearchEngine);
//const app = createApp(App);

app.use(router);
app.use(VueAxios, axios);
app.provide("axios", app.config.globalProperties.axios);

app.mount("#app");
