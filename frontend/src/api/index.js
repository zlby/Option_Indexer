import Vue from 'Vue'
import axios from 'axios'
import VueAxios from 'vue-axios'

Vue.use(VueAxios,axios);

var instance = axios.create({

  url:'https://api.example.com',

  transformRequest:[function(data){
    return data;
  }],

  transformResponse:[function(data){
    return data;
  }],

  headers: {'X-Requested-With':'XMLHttpRequest'},

  timeout:1000
});


export default {
  // localLogin: function (data) {
  //   return Vue.axios.post('/api/login',data)
  // },
  // localLogout: function (data) {
  //   return instance.post('/api/logout',data)
  // },
  localReg: function (data) {
    return Vue.axios.post('/api/register',data)
  }
}
