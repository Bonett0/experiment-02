

import { createRouter, createWebHistory } from 'vue-router';
import PersonalInformationView from '../views/PersonalInformationView.vue';
import WelcomePageView from '../views/WelcomePageView.vue';
import ExperimentView from '../views/ExperimentView.vue';
import EndView from '../views/EndView.vue';

const routes = [
  { path: '/', name: 'welcome', component: WelcomePageView },
  { path: '/personal-info', component: PersonalInformationView },
  { path: '/experiment/:participantData', name: 'Experiment', component: ExperimentView },
  { path: '/end-view', component: EndView },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
