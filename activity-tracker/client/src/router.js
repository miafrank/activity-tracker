import Vue from 'vue';
import Router from 'vue-router';
import Activities from './components/Activities.vue';

Vue.use(Router);

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/activities',
      name: 'activities',
      component: Activities,
    },
  ],
});
