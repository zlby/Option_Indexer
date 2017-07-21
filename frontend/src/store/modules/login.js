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
  username: '名字',
  title: [],
  time: [],
  context: [],
  new_email: '21',
  new_phone: '121'
};

const mutations = {
  login (state, obj) {
    state.loggedin = true;
    state.username = obj.username;
  },
  updateUserInfo (state, obj) {
    state.new_email = obj.email
    state.new_phone = obj.phone
  },
  logout (state) {
    state.loggedin = false;
  },
  new_password (state, obj){
    // state.old_password = 
    state.new_password = obj.new_password;
  },
  change(state) {
    state.loggedin = false;
  },
  getNews(state,obj) {
    state.title = obj.map(function(o){
      return o.title
    });
    state.time = obj.map(function(o){
      return o.time
    });;
    state.context = obj.map(function(o){
      return o.context
    });
  },
  new_emai_or_phone(state, obj){
    state.new_phone = obj.new_phone;
    state.new_email = obj.new_email;
  }
};

export default {
  state,
  mutations
}
