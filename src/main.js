import { createApp } from 'vue';
import App from './App.vue';
import { createRouter, createWebHistory } from 'vue-router';
import Header from './components/Header.vue';
import Home from './components/Home.vue';
import Projects from './components/Projects.vue';
import Thesis from './components/Thesis.vue';
import Books from './components/Books.vue';
import Workout from './components/Workout.vue';

const routes = [
  { path: '/', component: Home },
  { path: '/projects', component: Projects },
  { path: '/thesis', component: Thesis },
  { path: '/books', component: Books },
  { path: '/workout', component: Workout },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

const app = createApp(App);
app.use(router);
app.component('AppHeader', Header);

app.mount('#app');
