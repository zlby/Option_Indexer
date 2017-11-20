<template>
  <div class="infoborder">
    <el-alert title="" type="success" :closable="false" class="infotitle" >
    <div class="notification">
    <span style="position:relative;top:0px;">system notification<el-tag color="#ff4949">{{no_readCount}}</el-tag></span>
    <el-button size="small" @click="unread" class="button_group " type="danger" >unread</el-button>
    <el-button size="small" @click="read" class="button_group" type="success" >read</el-button>
    <el-button size="small" @click="all" class="button_group" type="info" >all</el-button>
    </div>
    </el-alert>

    <div v-for="(value,key,index) in notifs" >
    <el-alert title="Reminder" type="info" :closable="false" class="info" v-if="if_read[key]==currentStatus||currentStatus=='all'">
      <el-button color="#ff4949" size="mini" type="danger" v-if="if_read[key]=='no_read'" class="read-notice" @click="change2Read($event)" :msgid="notifs[key].id">unread</el-button>
      <el-tag color="#13ce66" v-if="if_read[key]=='read'" class="read-notice" @click="change2Read($event)" :msgid="notifs[key].id">read</el-tag>
      <div>Time:{{notifs[key].time}}</div>
      <div>
        <div class="buyin">
        Buy:{{notifs[key].buy_option}}
        </div>
        <div class="soldout">
        Sell:{{notifs[key].sell_option}}
        </div>
        <div class="rate">
          Buy/Sell
          <el-tag color="#13ce66">{{notifs[key].buy_lot}}Contracts</el-tag>/
          <el-tag color="#ff4949">{{notifs[key].sell_lot}}Contracts</el-tag>
        </div>
      </div>
    </el-alert>
    </div>
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
        notifs:this.$store.state.login.notifs,
        if_read:this.$store.state.login.if_read,
        msgid:this.$store.state.login.msgid
      }
    },
    computed: {
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
      }/*,
      notifs () {
        return this.$store.state.login.notifs
      }*/
    },

    mounted:function() {
      this.$store.dispatch('getNotification');
      window.store=this
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
        for(var i=0;i<this.if_read.length;i++){
          if(this.if_read[i]==="no_read"){
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
        var id=e.getAttribute("msgId")
        axios.put('/client/notification/'+id+'/read/').then(function(res){
            if(res.data.status.code=="0"){
                var index=saveThis.msgid.indexOf(parseInt(id));
                console.log(index)
                saveThis.changeStatus(index)
            }else{
               alert("网络问题")
            }
        })
      },
      changeStatus:function(index){
        console.log(index)
        this.if_read.splice(index,1,"read");
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
