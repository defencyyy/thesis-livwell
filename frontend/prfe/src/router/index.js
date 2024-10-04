import { createRouter, createWebHashHistory } from 'vue-router';
import BrokLogin from '@/views/BrokLogin.vue';
import BrokMainPage from '@/views/BrokMainPage.vue';
import DevMainPage from '@/views/DevMainPage.vue';
import DevLogin from '@/views/DevLogin.vue';
import BrokForgotPass from '@/views/BrokForgotPass.vue'; // Import your forgot password component
import BrokResetPass from '@/views/BrokResetPass.vue'; // Import your reset password component

const routes = [
    { path: '/broklogin', name: 'BrokLogin', component: BrokLogin },
    { path: '/brokmain', name: 'BrokMain', component: BrokMainPage },
    { path: '/devlogin', name: 'DevLogin', component: DevLogin },
    { path: '/devmain', name: 'DevMain', component: DevMainPage },
    { path: '/brokforgotpass', name: 'BrokForgotPass', component: BrokForgotPass },
    //{ path: '/brokresetpass', name: 'BrokResetPass', component: BrokResetPass }, // Moved to the top
    { path: '/brokresetpass/:uid/:token', name: 'BrokResetPass', component: BrokResetPass }, // Moved to the top
    { path: '/', redirect: '/broklogin' },
];

const router = createRouter({
    history: createWebHashHistory(),
    routes,
});



export default router;
