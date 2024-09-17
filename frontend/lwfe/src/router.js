import { createRouter, createWebHistory } from 'vue-router';
import UserLogin from './pages/UserLogin.vue';
import UserRegister from './pages/UserRegister.vue';
import UserHome from './pages/UserHome.vue';
const routes = [
    { path: '/login', component: UserLogin },
    { path: '/register', component: UserRegister },
    {path: '/home', component: UserHome},
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;