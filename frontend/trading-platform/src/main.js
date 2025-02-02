import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import { createPinia } from 'pinia';

import './style.css'; // Import the global theme

const app = createApp(App);

const pinia = createPinia();
app.use(pinia);
app.use(router);
app.mount('#app');