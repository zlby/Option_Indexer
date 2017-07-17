import Vue from 'Vue'
import axios from 'axios'

Vue.use(axios);
export default {
  localLogin: function (data) {
  	alert("sajdjasd")
    return axios.post('/client/login/',data)
  }
}

