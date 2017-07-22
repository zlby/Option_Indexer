<template>
  <div class="infoborder">
    <el-alert title="" type="success" :closable="false" class="infotitle" >
    <div class="notification">
    <span style="position:relative;top:0px;">系统通知<el-tag color="#ff4949">{{no_readCount}}</el-tag></span>  
    <el-button size="small" @click="unread" class="button_group " type="danger" >未读</el-button>
    <el-button size="small" @click="read" class="button_group" type="success" >已读</el-button>
    <el-button size="small" @click="all" class="button_group" type="info" >全部</el-button>
    </div>
    </el-alert>

    <template v-for="(value,key,index) in notifs" >
    <el-alert title="买进卖出提醒" type="info" :closable="false" class="info" v-if="if_read[key]==currentStatus||currentStatus=='all'">
      <el-button color="#ff4949" size="mini" type="danger" v-if="if_read[key]=='no_read'" class="read-notice" @click="change2Read($event)" :msgid="notifs[key].id">未读</el-button>
      <el-tag color="#13ce66" v-if="if_read[key]=='read'" class="read-notice" @click="change2Read($event)" :msgid="notifs[key].id">已读</el-tag>
      <div>时间:{{notifs[key].time}}</div>
      <div>
        <div class="buyin">
        买入股份：{{notifs[key].buy_option}} <el-tag color="#13ce66">{{notifs[key].buy_lot}}手</el-tag>
        </div>
        <div class="soldout">
        卖出股份：{{notifs[key].sell_option}} <el-tag color="#ff4949">{{notifs[key].sell_lot}}手</el-tag>
        </div>
      </div>
    </el-alert>
    </template>
</div>
</template>


<script>
  import api from '../api'
  import axios from 'axios'
  import Bus from '../bus'
  export default{
    data(){
      return{
        currentStatus:"all",
        no_readCount:0,
      }
    },
    computed: {
      if_read(){
        this.no_readCount=this.countNoRead();
        return this.$store.state.login.if_read;
      },
      buy_time(){
        return this.$store.state.login.buy_time;
      },
      buy_option(){
        return this.$store.state.login.buy_option;
      },
      sell_option(){
        return this.$store.state.login.sell_option;
      },
      buy_lot(){
        return this.$store.state.login.buy_lot;
      },
      sell_lot(){
        return this.$store.state.login.sell_lot;
      },
      notifs () {
        this.no_readCount=this.countNoRead();
        return this.$store.state.login.notifs
      }
    },

    mounted:function() {
      this.$store.dispatch('getNotification');
    },

    methods:{
      unread:function(){
        this.currentStatus="no_read";
        this.no_readCount=this.countNoRead();
      },
      read:function(){
        this.currentStatus="read";
        this.no_readCount=this.countNoRead();
      },
      all:function(){
        this.currentStatus="all";
        this.no_readCount=this.countNoRead();
      },
      countNoRead:function(){
        var count=0;
        for(var i=0;i<this.$store.state.login.if_read.length;i++){
          if(this.$store.state.login.if_read[i]==="no_read"){
            count++;
          }
        }
        Bus.$emit("getno-read", {count:count});
        return count;
      },
      change2Read:function(event){
        if(event.target.tagName=="SPAN"){
          var e=event.target.parentNode;
        }else{
          var e=event.target;
        }
        var saveThis=this
        axios.put('/client/notification/'+e.getAttribute("msgId")+'/read/').then(function(res){
          console.log(res);
            if(res.data.status.code=="0"){
                saveThis.$store.dispatch('getNotification');
                e.classList.remove("el-button--danger");
                e.classList.add("el-button--success");
                e.innerHTML="<span>已读</span>";
            }else{
               alert("网络问题")
            }
        })
      }
    }
}
</script>

<style lang="less" scoped>

  @import '../style/common';
  .info{
    margin-top: 15px;
    padding: 20px;
    font-size:20px;
  }
  .infotitle{
    margin-top: 10px;
  }

  .infoborder{
    margin-left: 10px;
    margin-right: 10px;
  // background-image: url("../assets/background1_副本.png");
}


.el-alert{
  background-color: #FFFFFF;
  color: #222222;
}
.read-notice{
  float:right;
  cursor: pointer;
}
.button_group{
  float: right;
  margin-left: 10px;
}

.notification{
  
}
</style>