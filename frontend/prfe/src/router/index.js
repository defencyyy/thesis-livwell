import { createRouter, createWebHashHistory } from 'vue-router'
import BrokLogin from '@/views/BrokLogin.vue';
import MainPage from '@/views/MainPage.vue';

const routes = [
  { path: '/login', name: 'Login', component: BrokLogin },
  { path: '/main', name: 'Main', component: MainPage }
];


const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router
