import Vue from 'vue'
import axios from 'axios'

Vue.use(axios);
export default {
  localLogin: function (data) {
    return axios.post('/client/login/',data)
  },
  localUpdateUserInfo: function () {
    return axios.get('/client/')
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
    return axios.get('/market/news/',{params:{page_number:paramObj.page_number}})
  },
  localnewphone_email: function (paramObj){
    return axios.put('/client/set_new_email_or_phone/',{email:paramObj.email,phone:paramObj.phone})
  },
  localgetNotification: function (data){
    return axios.get('/client/get_all_notification/',data)
  },
  localOptionCombination:function(paramObj){
    return axios.get('/client/get_all_combo/',paramObj)
  },
  localFutureListBalance:function(paramObj){
    return axios.get("/market/future_time/",paramObj)
  },
  localOptionListBalance:function(paramObj){
    return axios.get("/market/futures/",paramObj)
  }
}
