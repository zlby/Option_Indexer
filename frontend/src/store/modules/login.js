var isLoggedIn = function() {
  var token = localStorage.getItem('user');
  if (token) {
    var payload = JSON.parse(window.atob(token.split('.')[1]));
    if( payload.exp > Date.now() / 1000 ){
      return JSON.parse(localStorage.getItem('user'))
    }
  } else {
    return false;
  }
};

const state = {
  loggedin: false,
  username: '名字'
};

const mutations = {
  login (state, obj) {
    state.loggedin = true;
    state.username = obj.username;
  },
  logout (state) {
    state.loggedin = false;
  }
};

export default {
  state,
  mutations
}
