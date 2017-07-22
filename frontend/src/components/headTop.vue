<template>
  <div class="shade">
   <div class = "navigate">
     <el-row>
      <el-menu class="el-menu-demo1" mode="horizontal" router>

        <el-col :span="1" :offset="2">
         <el-menu-item index="/">
          <img src="../assets/LOGOQ.png" class="touxiang">
        </el-menu-item>	
      </el-col>

      <el-col :span="7" :offset="8" :xs="7" :md="7" :lg="7" :sm="7" class="main-page-group">
       <el-menu-item class="el-col el-col-xs-8 el-col-md-8 el-col-sm-8 el-col-lg-8 main-page-btn" index="/">首页</el-menu-item>		
       <el-menu-item index="/productIntro" class="el-col el-col-xs-8 el-col-md-8 el-col-sm-8 el-col-lg-8 main-page-btn" >策略套利</el-menu-item>
       <el-menu-item index="/use"  class="el-col el-col-xs-8 el-col-md-8 el-col-sm-8 el-col-lg-8 main-page-btn">信息资源</el-menu-item>
     </el-col>


     <el-col :span="6" :xs="6" :md="6" :lg="6" :sm="6" v-if="loggedin==false">
       <el-menu-item index= "/login" class="el-col el-col-xs-12 el-col-sm-12 el-col-md-12 el-col-lg-12 main-page-btn">登录</el-menu-item>
       <el-menu-item index="/register" class="el-col el-col-xs-12 el-col-sm-12 el-col-md-12 el-col-lg-12 main-page-btn">注册</el-menu-item>	
     </el-col>

     <el-col :span="6"  :xs="6" :md="6" :lg="6" :sm="6" v-else>
      <el-menu-item  index="/homepageIndividual/infoReminder"  class="el-col el-col-xs-8 el-col-sm-8 el-col-md-8 el-col-lg-8 main-page-btn">
      <el-badge :value="no_readCount" class="item">
        <i class="el-icon-message"></i>
      </el-badge>
      </el-menu-item>
      <el-menu-item  class="el-col el-col-xs-8 el-col-sm-8 el-col-md-8 el-col-lg-8 main-page-btn"><img style="width: 60px; height: 60px;" src="../assets/bigtouxiang.png"></el-menu-item>
      <el-menu-item  class="el-col el-col-xs-8 el-col-sm-8 el-col-md-8 el-col-lg-8 main-page-btn">
        <el-dropdown>
          <span class="el-dropdown-link1">
            {{name}}<i class="el-icon-caret-bottom el-icon--right"></i>
          </span>
          <el-dropdown-menu slot="dropdown">
            <el-dropdown-item><i class="el-icon-document"></i>
              <el-button type="text" @click="homepageIndividual">个人主页</el-button>
            </el-dropdown-item>
  <!--           <el-dropdown-item><i class="el-icon-setting"></i>
              <el-button type="text" @click="dialogFormVisible = true">个人信息设置</el-button>
            </el-dropdown-item> -->
            <el-dropdown-item><i class="el-icon-edit"></i>
              <el-button type="text" @click="change">切换账号</el-button>
            </el-dropdown-item>
            <el-dropdown-item><i class="el-icon-arrow-left"></i>
              <el-button type="text" @click="logout">注销</el-button>
            </el-dropdown-item>
          </el-dropdown-menu>


<!--           <el-dialog class="tanchu" title="信息修改" :visible.sync="dialogFormVisible" :modal-append-to-body="false" :before-close="handleClose" style="z-index:999;">


            <el-form :model="form">
              <el-form-item>
                <el-input v-model="form.old_password" type="password" id= "old_password" placeholder="Password"></el-input>
              </el-form-item>
              <el-form-item>
                <el-input v-model="form.new_password" type="password" id= "new_password" placeholder="newPassword"></el-input>
              </el-form-item>
        <el-form-item prop="email" class="input_form">
          <div class="el-col el-col-12 el-col-xs-12 el-col-sm-12 el-col-md-12 el-col-lg-12">{{email}}</div>
          <input v-model="form.email" class="el-input__inner" :value="email" type="email" placeholder="newEmail"></input>
        </el-form-item>
        <el-form-item prop="phone" class="input_form">
          <div class="el-col el-col-12 el-col-xs-12 el-col-sm-12 el-col-md-12 el-col-lg-12">{{phone}}</div>
          <input v-model="form.phone" :value="phone" type="phone" class="el-input__inner" placeholder="newPhone"></input>
        </el-form-item>
            </el-form>
            <div slot="footer" class="dialog-footer">
              <el-button @click="dialogFormVisible = false">取 消</el-button>
              <el-button type="primary" @click="dj">确 定</el-button>
            </div>


          </el-dialog> -->
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
        this.$store.dispatch('UserLogout');
      },
      dj: function(){
        this.$store.dispatch('UserNewpassword', {old_password:this.form.old_password,
          new_password:this.form.new_password});
        this.$store.dispatch('UserNewemailphone',{email:this.form.email,
          phone:this.form.phone});
      },
      change: function(){
        this.$store.dispatch('UserChange');
      },
      homepageIndividual: function(){
        this.$router.push({ path: '/homepageIndividual' })
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
  }
  .el-dropdown-link1{
    color:white;
  }

  .el-menu--horizontal .el-menu-item:hover, .el-menu--horizontal .el-submenu__title:hover {
    background-color: #eef1f600;
  }


  .main-page-btn{
    max-width:120px;
    text-align: center;
  }

  .main-page-group{
    //min-width:400px;
  }

  .touxiang{
   width: 58px;
   height: 58px;
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

</style>