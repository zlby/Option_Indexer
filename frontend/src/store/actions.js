import api from '../api'
import router from '../router'

export const UserNewpassword = ({ commit }, data) =>{
  api.localNewpassword(data).then(function (res){
    res = res.data
    if(res.status.code == '0'){
      commit('new_password', {new_password: data.new_password});
      // commit('logout');
      // router.push({path:'/login'})
    }else{
      alert('密码修改失败!')
    }
  })
  .catch(function (error){
    alert('密码修改失败!')
  })
};



export const UserRegister = ({ commit }, data) => {
  api.localRegister(data).then(function (res) {
    res = res.data
    if (res.status.code == '0') {
      router.push({path:'/homepageIndividual'})
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
      router.push({path:'/homepageIndividual'})
      commit('login', {username: data.username});
    } else {
      alert('登录失败！')
    }
  })
  .catch(function (error) {
    alert('登录失败！')
  })
};

export const UpdateUserInfo = ({ commit }) => {
  api.localUpdateUserInfo().then(function (res) {
    res = res.data
    if (res.status.code == '0') {
      console.log(res)
      commit('updateUserInfo', {username: res.username, email: res.email, phone: res.phone});
    } else {
      console.log('获取用户信息失败！')
    }
  })
  .catch(function (error) {
    console.log('获取用户信息失败！！')
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
    api.localNews({page_number: obj.page_number}).then(function (res){
      res = res.data
      if  (res.status.code == '0'){
        
        commit('getNews', {news: res.news, page_number: obj.page_number})
      }else{
        alert('获取新闻失败！')
      }
    }).catch(function (error){
      alert('获取新闻失败！')
    })
  };

export const UserNewemailphone = ({ commit }, data) =>{
  api.localnewphone_email({email:data.email,phone:data.phone}).then(function (res){
    res = res.data
    if(res.status.code == '0'){
      commit('new_emai_or_phone', {new_email: data.new_email,
        new_phone: data.new_phone});
      alert('修改成功!')
    }else{
      alert('修改!')
    }
  })
  .catch(function (error){
    alert('修改失败1!')
  })
};

export const getNotification = ({ commit }, obj)=>{
  api.localgetNotification().then(function(res){
    console.log(res);
    res = res.data
    if (res.status.code == '0'){
      commit('getNotification',res.notification_list)
    }else{
      alert('获取消息失败 code不为0')
      }
    }).catch(function (error){
      alert('获取消息失败！ ')
      console.log(error)
    })
};
