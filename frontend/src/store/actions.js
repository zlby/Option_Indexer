import api from '../api'
import router from '../router'

export const UserNewpassword = ({ commit }, data) =>{
  api.localNewpassword(data).then(function (res){
    res = res.data
    if(res.status.code == '0'){
      commit('new_password', {new_password: data.new_password});
      commit('logout');
      router.push({path:'/login'})
    }else{
      alert('修改失败!')
    }
  })
  .catch(function (error){
    alert('修改失败!')
  })
};


export const UserRegister = ({ commit }, data) => {
  api.localRegister(data).then(function (res) {
      res = res.data
      if (res.status.code == '0') {
        router.push({path:'/productIntro'})
        commit('login', {username: data.username});
      } else if(res.status.code == '-3'){
        alert('用户名已经注册！')
      } else{
        alert('请输入完整的账号密码！')
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
        commit('logout')
      } else { // 注销失败
        alert('注销失败！')
      } 
  }).catch(function (error) {
    alert('注销失败！')
  })
};

export const UserChange = ({ commit }) => {
  api.localLogout().then(function (res) {
    res = res.data
    if (res.status.code == '0') { // 注销成功，返回首页
        commit('logout')
        router.push({path:'/login'})
      } else { // 注销失败
        alert('账号切换失败！')
      } 
  }).catch(function (error) {
    alert('账号切换失败！')
  })
};

export const News = ({ commit }, obj) => {
  api.localNews(obj).then(function (res){
    res = res.data
    if  (res.status.code == '0'){
      console.log('成功1')
      commit('getNews', {title: data.title, context: data.context, time: data.time})
      console.log('成功2');
    }else{
      alert('获取新闻失败！')
       console.log('失败1');
    }
  }).catch(function (error){
    alert('获取新闻失败！')
     console.log('失败2');
  })
};
