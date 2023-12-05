

import { createRouter, createWebHistory } from 'vue-router';
import PersonalInformationView from '../views/PersonalInformationView.vue';
import WelcomePageView from '../views/WelcomePageView.vue';
import ExperimentView from '../views/ExperimentView.vue';

const routes = [
  { path: '/', component: WelcomePageView },
  { path: '/personal-info', component: PersonalInformationView },
  { path: '/experiment', component: ExperimentView },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
