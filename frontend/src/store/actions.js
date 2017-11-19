import api from '../api'
import router from '../router'
import Bus from '../bus'

export const UserNewpassword = ({ commit }, data) =>{
  return new Promise((resolve, reject) => {
    api.localNewpassword(data).then(function (res){
      res = res.data
      if(res.status.code == '0'){
        commit('new_password', {new_password: data.new_password});
        resolve()
      }else{
        reject()
      }
    })
    .catch(function (error){
      reject()
    })
  })
};



export const UserRegister_en = ({ commit }, data) => {
  return new Promise((resolve, reject) => {
    api.localRegister(data).then(function (res) {
      res = res.data
      if (res.status.code == '0') {
        router.push({path:'/en'})
        commit('login', {username: data.username});
        resolve()
      } else if(res.status.code == '-3'){
        reject()
      } else{
        reject()
      }
    })
    .catch(function (error) {
      reject()
    })
  })
};

export const UserRegister_ch = ({ commit }, data) => {
  return new Promise((resolve, reject) => {
    api.localRegister(data).then(function (res) {
      res = res.data
      if (res.status.code == '0') {
        router.push({path:'/zh-cn'})
        commit('login', {username: data.username});
        resolve()
      } else if(res.status.code == '-3'){
        reject()
      } else{
        reject()
      }
    })
    .catch(function (error) {
      reject()
    })
  })
};

export const UserLogin_en = ({ commit }, data) => {
  return new Promise((resolve, reject) => {
    api.localLogin(data).then(function (res) {
      res = res.data
      if (res.status.code == '0') {
        router.push({path:'/en'})
        commit('login', {username: data.username});
        resolve()
      } else {
        // alert('登录失败！')
        reject()
      }
    })
    .catch(function (error) {
      // alert('登录失败！!')
      reject()
    })
  })
};

export const UserLogin_ch = ({ commit }, data) => {
  return new Promise((resolve, reject) => {
    api.localLogin(data).then(function (res) {
      res = res.data
      if (res.status.code == '0') {
        router.push({path:'/zh-cn'})
        commit('login', {username: data.username});
        resolve()
      } else {
        // alert('登录失败！')
        reject()
      }
    })
    .catch(function (error) {
      // alert('登录失败！!')
      reject()
    })
  })
};

export const UpdateUserInfo = ({ commit }) => {
  api.localUpdateUserInfo().then(function (res) {
    res = res.data
    if (res.status.code == '0') {
      console.log(res)
      commit('updateUserInfo', {username: res.username, email: res.email, phone: res.phone});
    } else {
      console.log('Wrong Information！')
    }
  })
  .catch(function (error) {
    console.log('Wrong Information！')
  })
};



export const UserLogout_en = ({ commit }) => {
  api.localLogout().then(function (res) {
    res = res.data
    if (res.status.code == '0') { // 注销成功，返回首页
      commit('logout')
      router.push({path:'/en'})
      } else { // 注销失败
        console.log('注销失败！')
      }
    }).catch(function (error) {
      console.log('注销失败！')
    })
  };

export const UserLogout_ch = ({ commit }) => {
  api.localLogout().then(function (res) {
    res = res.data
    if (res.status.code == '0') { // 注销成功，返回首页
      commit('logout')
      router.push({path:'/zh-ch'})
      } else { // 注销失败
        console.log('注销失败！')
      }
    }).catch(function (error) {
      console.log('注销失败！')
    })
  };

  export const UserChange_ch = ({ commit }) => {
    api.localLogout().then(function (res) {
      res = res.data
    if (res.status.code == '0') { // 注销成功，返回首页
      commit('logout')
      router.push({path:'/zh-cn/login'})
      } else { // 注销失败
        console.log('账号切换失败！')
      }
    }).catch(function (error) {
      console.log('账号切换失败！')
    })
  };

    export const UserChange_en = ({ commit }) => {
    api.localLogout().then(function (res) {
      res = res.data
    if (res.status.code == '0') { // 注销成功，返回首页
      commit('logout')
      router.push({path:'/en/login'})
      } else { // 注销失败
        console.log('账号切换失败！')
      }
    }).catch(function (error) {
      console.log('账号切换失败！')
    })
  };

  export const News = ({ commit }, obj) => {
    api.localNews({page_number: obj.page_number}).then(function (res){
      res = res.data
      if  (res.status.code == '0'){

        commit('getNews', {news: res.news, page_number: obj.page_number})
      }else{
        console.log('获取新闻失败！')
      }
    }).catch(function (error){
      console.log('获取新闻失败！')
    })
  };

export const UserNewemailphone = ({ commit }, data) =>{
  return new Promise((resolve, reject) => {
    api.localnewphone_email({email:data.email,phone:data.phone})
    .then(function (res){
      res = res.data
      if(res.status.code == '0'){
        commit('new_emai_or_phone', {new_email: data.new_email, new_phone: data.new_phone});
        resolve()
        // alert('邮箱或手机修改成功，请重新登录!')
      }else{
        reject()
        // alert('邮箱或手机修改失败！')
      }
    })
    .catch(function (error){
      reject()
      // alert('邮箱或手机修改失败！！')
    })
  })

};

export const getNotification = ({ commit }, obj)=>{
  api.localgetNotification().then(function(res){
    res = res.data
    if (res.status.code == '0'){
      commit('getNotification',res.notification_list)
      var count = 0
      for (var i = res.notification_list.length - 1; i >= 0; i--) {
        if (res.notification_list[i].if_read) {
          count++
        }
      }
      Bus.$emit("getno-read", {count:count});
    }else{
      console.log('获取消息失败 code不为0')
      }
    }).catch(function (error){
      console.log('获取消息失败！ ')
      console.log(error)
    })
};

export const getOptionCombo = ({ commit }, obj)=>{
  api.localOptionCombination().then(function(res){
    res = res.data
    if (res.status.code == '0'){
      commit('getOptionCombo',res.combo_list)
    }else{
      console.log('获取消息失败 code不为0')
      }
    }).catch(function (error){
      console.log('获取消息失败！ ')
      console.log(error)
    })
};

export const getFutureListBalance = ({ commit }, obj)=>{
  api.localFutureListBalance().then(function(res){
    res = res.data
    if (res.status.code == '0'){
      commit('getFutureListBalance',res.future_list)
    }else{
      console.log('获取消息失败 code不为0')
      }
    }).catch(function (error){
      console.log('获取消息失败！ ')
      console.log(error)
    })
};
export const getOptionListBalance = ({ commit }, obj)=>{
  var future=[];
  api.localFutureListBalance().then(function(res){
    res=res.data;
    future=res.future_list;
  })

  api.localOptionListBalance().then(function(res){
    res = res.data
    if (res.status.code == '0'){
      commit('getOptionListBalance',{time:future,future_list:res.future_list})
    }else{
      console.log('获取消息失败 code不为0')
      }
    }).catch(function (error){
      console.log('获取消息失败！ ')
      console.log(error)
    })
};
