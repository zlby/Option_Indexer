import Vue from 'Vue'
import axios from 'axios'
import VueAxios from 'vue-axios'

Vue.use(VueAxios,axios);

var instance = axios.create();

export default {
  localLogin: function (data) {
    return Vue.axios.post('/api/login',data)
  },
  localLogout: function (data) {
    return instance.post('/api/logout',data)
  },
  localReg: function (data) {
    return Vue.axios.post('/api/reg',data)
  }
}
