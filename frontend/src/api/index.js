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
  }
}
