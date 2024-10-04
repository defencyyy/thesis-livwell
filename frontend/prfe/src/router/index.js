import { createRouter, createWebHashHistory } from 'vue-router';
import BrokLogin from '@/views/BrokLogin.vue';
import BrokMainPage from '@/views/BrokMainPage.vue';
import DevMainPage from '@/views/DevMainPage.vue';
import DevLogin from '@/views/DevLogin.vue';
import BrokForgotPass from '@/views/BrokForgotPass.vue'; // Import your new component

const routes = [
  { path: '/broklogin', name: 'BrokLogin', component: BrokLogin },
  { path: '/brokmain', name: 'BrokMain', component: BrokMainPage },
  { path: '/devlogin', name: 'DevLogin', component: DevLogin },
  { path: '/devmain', name: 'DevMain', component: DevMainPage },
  { path: '/brokforgotpass', name: 'BrokForgotPass', component: BrokForgotPass }, // Add your new route
  { path: '/', redirect: '/broklogin' },
];

const router = createRouter({
  history: createWebHashHistory(),
  routes,
});

export default router;
