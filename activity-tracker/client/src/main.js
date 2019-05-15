import BootstrapVue from 'bootstrap-vue';
import Notifications from 'vue-notification';
import 'bootstrap/dist/css/bootstrap.css';
import Vue from 'vue';
import App from './App.vue';
import router from './router';

Vue.use(BootstrapVue);
Vue.use(Notifications);
Vue.config.productionTip = false;

new Vue({
  router,
  render: h => h(App),
}).$mount('#app');
