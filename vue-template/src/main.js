import { createApp } from "vue";
//import App from "./App.vue";
import SearchEngine from "./SearchEngine.vue";
import router from "./router";

import "./assets/main.css";

const app = createApp(SearchEngine); //createApp(App);

app.use(router);

app.mount("#app");
