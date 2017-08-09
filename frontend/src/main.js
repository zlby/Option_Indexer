// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.

import Vue from 'vue'
import App from './App'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-default/index.css'
import router from './router'
import Vuex from 'vuex'
import store from './store/index'




// Vue.prototype.$http = axios;
// Vue.config.productionTip = false;

/* eslint-disable no-new */
Vue.use(ElementUI);
Vue.use(Vuex);

new Vue({
  el: '#app',
  router,
  store,
  template: '<App/>',
  components: { App }
})

