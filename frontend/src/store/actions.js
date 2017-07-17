import api from '../api'
export const UserLogin = ({ commit }, data) => {
  api.localLogin(data).then(function (res) {
      // commit(USER_SIGNIN, response.data.token);
      // window.location = '/person'
      res = res.data
        if (res.status.code == '0') { // 注册成功，自动登录
          router.push({path:'/productIntro'})
        } else { // 注册失败
          alert('登录失败！')
        }
    })
  .catch(function (error) {
    alert('登录失败！')
    console.log(error);
  });
};