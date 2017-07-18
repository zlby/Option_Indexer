import Vue from 'Vue'
import axios from 'axios'

Vue.use(axios);
export default {
  localLogin: function (data) {
    return axios.post('/client/login/',data)
  },
  localLogout: function (data) {
  	return axios.post('/client/logout/')
  },
  localRegister: function (data) {
  	return axios.post('/client/register/',data)
  },
  localNewpassword: function (data){
  	return axios.post('/client/set_new_password/',data)
  },
  localChange: function (data){
    return axios.post('/client/logout/')
  },

}
