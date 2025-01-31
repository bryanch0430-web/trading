
import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import './style.css'; // Import the global theme

createApp(App).use(router).mount('#app');