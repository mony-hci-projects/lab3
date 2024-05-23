import { createApp } from "vue";
//import App from "./App.vue";
import Engine from "./Engine.vue";
import router from "./router";

import "./assets/main.css";

const app = createApp(Engine); //createApp(App);

app.use(router);

app.mount("#app");
