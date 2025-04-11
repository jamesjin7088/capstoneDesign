import { createRouter, createWebHistory } from 'vue-router';
import MainPage from '@/views/MainPage.vue';
import SecondPage from '@/views/SecondPage.vue';
import ThirdPage from '@/views/ThirdPage.vue';
import FourthPage from '@/views/FourthPage.vue';
import FifthPage from '@/views/FifthPage.vue';

import Test from '@/views/test.vue';

const routes = [
  { path: '/', component: MainPage },
  { path: '/second', component: SecondPage },
  { path: '/third', component: ThirdPage },
  { path: '/fourth', component: FourthPage },
  { path: '/fifth', component: FifthPage },

  { path: '/test', component: Test },
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;