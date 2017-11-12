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
  title: [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],
  time: [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],
  content: [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],
  new_email: '',
  new_phone: '',
  notification: [],
  OptionComboList: [],
  comboId: [],
  futureBalance: [],
  optionBalance: [],
  futureTimetable: {},
};

const mutations = {
  login (state, obj) {
    state.loggedin = true
    state.username = obj.username
     // state.new_email = obj.email
     // state.new_phone = obj.phone
  },
  updateUserInfo (state, obj) {
    state.username = obj.username
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
  getNews(state, obj) {
    var news = obj.news // 1d
    var page = obj.page_number
    var titles = news.map(function(o){
      return o.title
    })
    var times = news.map(function(o){
      return o.time
    })
    var contents = news.map(function(o){
      return o.content
    })
    state.title.splice(page-1, 1, titles)
    state.time.splice(page-1, 1, times)
    state.content.splice(page-1, 1, contents)
  },
  new_emai_or_phone(state, obj){
    state.new_phone = obj.new_phone;
    state.new_email = obj.new_email;
  },
  getNotification(state,obj){
    state.if_read=obj.map(function(o){
      if(o.if_read==true){
          return "read"
      }else{
          return "no_read"
      }
    })
    state.buy_time = obj.map(function(o){
      return o.time
    })
    state.buy_option = obj.map(function(o){
      return o.buy_option
    })
    state.sell_option = obj.map(function(o){
      return o.sell_option
    })
    state.buy_lot = obj.map(function(o){
      return o.buy_lot
    })
    state.sell_lot = obj.map(function(o){
      return o.sell_lot
    })
    state.msgid=obj.map(function(o){
      return o.id
    })
    state.notifs = obj
  },
  getOptionCombo(state,obj){
    state.positive_option = obj.map(function(o){
      return o.positive_option
    })
    state.negative_option = obj.map(function(o){
      return o.negative_option
    })
    state.OptionComboList = obj
    state.comboId=obj.map(function(o){
      return o.id;
    })
  },
  deleteCombo(state, obj){
    var idx = obj.index
    state.OptionComboList.splice(idx, 1)
    state.comboId.splice(idx,1);
  },
  getFutureListBalance(state,obj){
    state.futureBalance=obj.map(function(o){
      return o.code
    })
    var timetable={};
    for(var i=0;i<obj.length;i++){
        timetable[obj[i].code]=new Date(obj[i].delivery_day).getTime();
    }
    state.futureTimetable=timetable;
  },
  getOptionListBalance(state,obj){
    var optionList=[];
    for(var i=0;i<obj.future_list.length;i++){
      optionList=optionList.concat(obj.future_list[i].options)
    }
    state.optionBalance=optionList;
    
  }

};

export default {
  state,
  mutations
}
