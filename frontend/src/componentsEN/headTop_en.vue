<template>
  <div class="shade">
   <div class = "navigate">
     <el-row>
      <el-menu class="el-menu-demo1" mode="horizontal" router>

      <el-col :span="1" :offset="2">
         <el-menu-item index="/en">
          <img src="../assets/未标题-1.png" class="touxiang">
        </el-menu-item>
      </el-col>

      <el-col :span="7" :offset="8" :xs="7" :md="7" :lg="7" :sm="7" class="main-page-group">
       <el-menu-item class="el-col el-col-xs-6 el-col-md-6 el-col-sm-6 el-col-lg-6 main-page-btn" index="/en">Mainpage</el-menu-item>

       <el-menu-item index="/en" class="el-col el-col-xs-6 el-col-md-6 el-col-sm-6 el-col-lg-6 main-page-btn" v-if="loggedin==true">
        <el-dropdown menu-align="start">
          <span class="el-dropdown-link1">Hedge
          </span>
          <el-dropdown-menu slot="dropdown"  class="main-page-dropdown" style="background-color:#404040; border:0px;">
            <el-dropdown-item>
            <el-button type="text" @click="toBeanGroup">Portfolio Value Map</el-button>
            </el-dropdown-item>
            <el-dropdown-item>
              <el-button type="text" @click="toCrop">Portfolio Hedge</el-button>
            </el-dropdown-item>
            <el-dropdown-item>
              <el-button type="text" @click="toAccess">Cross Hedge</el-button>
            </el-dropdown-item>
          </el-dropdown-menu>
        </el-dropdown>
      </el-menu-item>



      <el-menu-item index="/en/productIntro" class="el-col el-col-xs-6 el-col-md-6 el-col-sm-6 el-col-lg-6 main-page-btn" v-if="loggedin==true">Arbitrage</el-menu-item>
        <el-menu-item index="/en/login" class="el-col el-col-xs-6 el-col-md-6 el-col-sm-6 el-col-lg-6 main-page-btn" v-else>Arbitrage</el-menu-item>
        <el-menu-item index="/en" class="el-col el-col-xs-6 el-col-md-6 el-col-sm-6 el-col-lg-6 main-page-btn">
        <el-dropdown menu-align="start">
          <span class="el-dropdown-link1">Help
          </span>
          <el-dropdown-menu slot="dropdown"  class="main-page-dropdown" style="background-color:#404040; border:0px;">
            <el-dropdown-item>
            <a href="/static/pdf/INDEXER.pdf" class="normalize_font">User Manual</a>
            </el-dropdown-item>
            <el-dropdown-item>
            <a href="/static/video/INDEXER.mp4" class="normalize_font">Demo Video</a>
            </el-dropdown-item>
            <el-dropdown-item >
              <router-link to="/zh-cn" class="normalize_font">中文版</router-link>
            </el-dropdown-item>
          </el-dropdown-menu>
        </el-dropdown>
      </el-menu-item>
    </el-col>



     <el-col :span="5" :offset="1" :xs="5" :md="5" :lg="5" :sm="5" v-if="loggedin==false">
       <el-menu-item index= "/en/login" class="el-col el-col-xs-12 el-col-sm-12 el-col-md-12 el-col-lg-12 main-page-btn">Login</el-menu-item>
       <el-menu-item index="/en/register" class="el-col el-col-xs-12 el-col-sm-12 el-col-md-12 el-col-lg-12 main-page-btn">Register</el-menu-item>
     </el-col>

     <el-col :span="5" :offset="1" :xs="5" :md="5" :lg="5" :sm="5" v-else>
      <el-menu-item  index="/en/homepageIndividual/infoReminder"  class="el-col  main-page-btn" style="width:40%;">
      <el-badge :value="no_readCount" class="item">
        <i class="el-icon-message"></i>
      </el-badge>
      </el-menu-item>

      <el-menu-item  index="/en" class="el-col main-page-btn avatar" style="width:30%">
      <img style="width: 50px; height: 50px;margin-top:0px" src="../assets/bigtouxiang.png">
      </el-menu-item>
      <el-menu-item  index="/en" class="el-col main-page-btn" style="width:30%">
        <el-dropdown style="margin-left:10px">
          <span class="el-dropdown-link1">
            {{name}}<i class="el-icon-caret-bottom el-icon--right"></i>
          </span>

          <el-dropdown-menu slot="dropdown" style="background-color:#404040; border:0px;margin-left:40px">
            <el-dropdown-item><i class="el-icon-document" style="color:white"></i>
              <el-button type="text" @click="homepageIndividual">Homepage</el-button>
            </el-dropdown-item>
            <el-dropdown-item><i class="el-icon-edit" style="color:white"></i>
              <el-button type="text" @click="change">Switch accounts</el-button>
            </el-dropdown-item>
            <el-dropdown-item><i class="el-icon-arrow-left" style="color:white"></i>
              <el-button type="text" @click="logout">Log out</el-button>
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
        this.$store.dispatch('UserLogout_en');
      },
      dj: function(){
        this.$store.dispatch('UserNewpassword', {old_password:this.form.old_password,
          new_password:this.form.new_password});
        this.$store.dispatch('UserNewemailphone',{email:this.form.email,
          phone:this.form.phone});
      },
      change: function(){
        this.$store.dispatch('UserChange_en');
      },
      homepageIndividual: function(){
        this.$router.push({ path: '/en/homepageIndividual' })
      },
      toBeanGroup: function(){
        this.$router.push({ path: '/en/beanGroup'})
      },
      toCal: function(){
        this.$router.push({ path: '/en/calculator'})
      },
      toCrop: function(){
        this.$router.push({ path: '/en/crop'})
      },
      toAccess: function(){
        this.$router.push({ path: '/en/assess'})
      },
      toLogin:function () {
        this.$router.push({ path: '/en/login'})
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

  .avatar{
    vertical-align:middle;
  }

  .touxiang{
    width: 90px;
    height: 60px;
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
