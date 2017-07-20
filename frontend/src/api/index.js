import Vue from 'vue'
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
  localNews: function (paramObj){
    return axios.get('/market/news/',{params:{page_number:this.page_number}})
  },
  localnewphone_email: function (paramObj){
    return axios.put('/client/set_new_email_or_phone/',{email:paramObj.email,phone:paramObj.phone})
  }
}
