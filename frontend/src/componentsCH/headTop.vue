<template>
  <div class="shade">
   <div class = "navigate">
     <el-row>
      <el-menu class="el-menu-demo1" mode="horizontal" router>

      <el-col :span="1" :offset="2">
         <el-menu-item index="/zh-cn">
          <img src="../assets/未标题-1.png" class="touxiang">
        </el-menu-item>
      </el-col>

      <el-col :span="7" :offset="8" :xs="7" :md="7" :lg="7" :sm="7" class="main-page-group">
       <el-menu-item class="el-col el-col-xs-6 el-col-md-6 el-col-sm-6 el-col-lg-6 main-page-btn" index="/zh-cn">首页</el-menu-item>

       <el-menu-item index="/zh-cn" class="el-col el-col-xs-6 el-col-md-6 el-col-sm-6 el-col-lg-6 main-page-btn" v-if="loggedin==true">
        <el-dropdown menu-align="start">
          <span class="el-dropdown-link1">套期保值
          </span>
          <el-dropdown-menu slot="dropdown"  class="main-page-dropdown" style="background-color:#404040; border:0px;">
            <el-dropdown-item>
            <el-button type="text" @click="toBeanGroup">豆粕资产组合损益图</el-button>
            </el-dropdown-item>
            <el-dropdown-item>
              <el-button type="text" @click="toCrop">豆粕资产组合套期保值</el-button>
            </el-dropdown-item>
            <el-dropdown-item>
              <el-button type="text" @click="toAccess">农作物跨品种套期保值</el-button>
            </el-dropdown-item>
          </el-dropdown-menu>
        </el-dropdown>
      </el-menu-item>



      <el-menu-item index="/zh-cn/productIntro" class="el-col el-col-xs-6 el-col-md-6 el-col-sm-6 el-col-lg-6 main-page-btn" v-if="loggedin==true">策略套利</el-menu-item>
        <el-menu-item index="/zh-cn/login" class="el-col el-col-xs-6 el-col-md-6 el-col-sm-6 el-col-lg-6 main-page-btn" v-else>策略套利</el-menu-item>
        <el-menu-item index="/zh-cn" class="el-col el-col-xs-6 el-col-md-6 el-col-sm-6 el-col-lg-6 main-page-btn">
        <el-dropdown menu-align="start">
          <span class="el-dropdown-link1">帮助
          </span>
          <el-dropdown-menu slot="dropdown"  class="main-page-dropdown" style="background-color:#404040; border:0px;">
            <el-dropdown-item>
            <a href="/static/pdf/INDEXER.pdf" class="normalize_font">用户手册</a>
            </el-dropdown-item>
            <el-dropdown-item>
            <a href="/static/video/INDEXER.mp4" class="normalize_font">演示视频</a>
            </el-dropdown-item>
            <el-dropdown-item >
              <router-link to="/en" class="normalize_font">English</router-link>
            </el-dropdown-item>
          </el-dropdown-menu>
        </el-dropdown>
      </el-menu-item>
    </el-col>



     <el-col :span="5" :offset="1" :xs="5" :md="5" :lg="5" :sm="5" v-if="loggedin==false">
       <el-menu-item index= "/zh-cn/login" class="el-col el-col-xs-12 el-col-sm-12 el-col-md-12 el-col-lg-12 main-page-btn">登录</el-menu-item>
       <el-menu-item index="/zh-cn/register" class="el-col el-col-xs-12 el-col-sm-12 el-col-md-12 el-col-lg-12 main-page-btn">注册</el-menu-item>
     </el-col>

     <el-col :span="5" :offset="1" :xs="5" :md="5" :lg="5" :sm="5" v-else>
      <el-menu-item  index="/zh-cn/homepageIndividual/infoReminder"  class="el-col  main-page-btn" style="width:40%;">
      <el-badge :value="no_readCount" class="item">
        <i class="el-icon-message"></i>
      </el-badge>
      </el-menu-item>

      <el-menu-item  index="/zh-cn" class="el-col main-page-btn avatar" style="width:30%">
      <img style="width: 50px; height: 50px;" src="../assets/bigtouxiang.png">
      </el-menu-item>
      <el-menu-item  index="/zh-cn" class="el-col main-page-btn" style="width:30%">
        <el-dropdown style="margin-left:10px">
          <span class="el-dropdown-link1">
            {{name}}<i class="el-icon-caret-bottom el-icon--right"></i>
          </span>

          <el-dropdown-menu slot="dropdown" style="background-color:#404040; border:0px;margin-left:40px">
            <el-dropdown-item><i class="el-icon-document" style="color:white"></i>
              <el-button type="text" @click="homepageIndividual">个人主页</el-button>
            </el-dropdown-item>
            <el-dropdown-item><i class="el-icon-edit" style="color:white"></i>
              <el-button type="text" @click="change">切换账号</el-button>
            </el-dropdown-item>
            <el-dropdown-item><i class="el-icon-arrow-left" style="color:white"></i>
              <el-button type="text" @click="logout">注销</el-button>
            </el-dropdown-item>
          </el-dropdown-menu>
        </el-dropdown>

      </el-menu-item>
    </el-col>

  </el-menu>
</el-row>
</div>
</div>


</template>

<script>
  import {mapGetters} from 'vuex'
  import Bus from '../bus'
  export default {
   data() {
    return {
      no_readCount:0,
      dialogFormVisible: false,
      form: {
              // username: '',
              old_password: '',
              new_password: '',
              email: '',
              phone: ''
            },
            formLabelWidth: '120px'
          };
        },
        computed: {
         loggedin () {
          return this.$store.state.login.loggedin;
        },
        name () {
          return this.$store.state.login.username;
        }
      },
      created(){
        Bus.$on('getno-read', Obj=>{
            this.no_readCount=Obj.count;
        })
      },
      methods: {
       logout: function() {
        this.$store.dispatch('UserLogout_ch');
      },
      dj: function(){
        this.$store.dispatch('UserNewpassword', {old_password:this.form.old_password,
          new_password:this.form.new_password});
        this.$store.dispatch('UserNewemailphone',{email:this.form.email,
          phone:this.form.phone});
      },
      change: function(){
        this.$store.dispatch('UserChange_ch');
      },
      homepageIndividual: function(){
        this.$router.push({ path: '/zh-cn/homepageIndividual' })
      },
      toBeanGroup: function(){
        this.$router.push({ path: '/zh-cn/beanGroup'})
      },
      toCal: function(){
        this.$router.push({ path: '/zh-cn/calculator'})
      },
      toCrop: function(){
        this.$router.push({ path: '/zh-cn/crop'})
      },
      toAccess: function(){
        this.$router.push({ path: '/zh-cn/assess'})
      },
      toLogin:function () {
        this.$router.push({ path: '/zh-cn/login'})
      },
      toPdf:function(){
        window.open("/static/pdf/INDEXER.pdf")
      },
      toVideo:function(){
        window.open("/static/video/INDEXER.mp4")
      },
      watch: {
        dialogFormVisible: function(val){
          if(val===false){ // 要隐藏

          }
        }
      }
    },
  }
</script>

<style lang="less">

	@import '../style/common';

	.el-menu-demo1{
		width:100%;
    background-repeat:no-repeat;
    background-size:100% 100%;
    -moz-background-size:100% 100%;
    padding-left: 0px;
    padding-right: 0px;
    height: 60px;
    z-index: 3;
    background-color:#404040;
  }
  .el-menu-item{
    color:#fff;
    vertical-align:baseline;
  }
  .el-dropdown-link1{
    color:white;
    font-size: 18px;
  }

  .el-menu--horizontal .el-menu-item:hover, .el-menu--horizontal .el-submenu__title:hover {
    background-color: #eef1f600;
  }


  .main-page-btn{
    max-width:120px;
    text-align: center;
  }
  .main-page-btn:hover{
    color:#3476C8
  }


  .main-page-group{
    //min-width:400px;
  }

  .touxiang{
    width: 90px;
    height: 60px;
 }

 .avatar{
   vertical-align:middle;
 }
 .bigtouxiang{
  width: 58px;
  height: 58px;
}

.touxiang1{
	color:white;
	-webkit-filter: drop-shadow(#FFFFFF 0px 0);filter: drop-shadow(#FFFFFF 0px 0);
}

// .navigate{
//   z-index: 998;
//   width: 100%;
//   height: 100%;
//   background-color: white;
//   position: absolute;
// }

#username{
	opacity:0.90;
}

#password{
	opacity: 0.90;
}

// .item{
//   // margin-top: 30px;
//   height: 40px;
// }

.el-badge{
  margin-top: 5px;
}

.el-badge__content{
  margin-top: 15px;
}
.normalize_font{
  text-decoration: none;
  color:#20a0e0;
}
</style>
