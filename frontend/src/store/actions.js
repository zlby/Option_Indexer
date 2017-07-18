import api from '../api'
import router from '../router'
export const UserRegister = ({ commit }, data) => {
  api.localRegister(data).then(function (res) {
      res = res.data
      if (res.status.code == '0') {
        router.push({path:'/productIntro'})
        commit('login', {username: data.username});
      } else {
        alert('登录失败！')
      }
    })
  .catch(function (error) {
    alert('登录失败！')
  })
};

export const UserLogin = ({ commit }, data) => {
  api.localLogin(data).then(function (res) {
      res = res.data
      if (res.status.code == '0') {
        router.push({path:'/productIntro'})
        commit('login', {username: data.username});
      } else {
        alert('登录失败！')
      }
    })
  .catch(function (error) {
    alert('登录失败！')
  })
};

export const UserLogout = ({ commit }) => {
  api.localLogout().then(function (res) {
    res = res.data
    if (res.status.code == '0') { // 注销成功，返回首页
        router.push({path:'/'})
        commit('logout')
      } else { // 注销失败
        alert('注销失败！')
      } 
  }).catch(function (error) {
    alert('注销失败！')
  })
};