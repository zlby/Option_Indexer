<template>
  <div>
    <header class="admin_title"><i class="el-icon-edit"></i>      个人信息</header>
    <div class="admin_set">
    <el-col :span="18">
      <el-form :model="form" ref="form" label-width="100px" class="demo-ruleForm">
        <el-form-item label="昵称" class="input_form">
          <el-input type="name" :value="name" :disabled="true" ></el-input>
        </el-form-item>

        <el-form-item label="旧密码" prop="pass" class="input_form">
          <el-input type="password" v-model="form.old_password" ></el-input>
        </el-form-item>

        <el-form-item label="新密码" prop="checkPass" class="input_form">
          <el-input type="password" v-model="form.new_password"></el-input>
        </el-form-item>

        <el-form-item label="邮箱" class="input_form">
          <el-input v-model="cemail" ></el-input>
<!--           <el-input type="name" :value="name" ></el-input> -->
        </el-form-item>

        <el-form-item label="手机号码" class="input_form">
          <el-input v-model="cphone"></el-input>
        </el-form-item>

        <el-form-item class="input_form">
          <el-button type="primary" @click="dj">提交</el-button>
        </el-form-item>
      </el-form>
    </el-col>
    </div>
  </div>
</template>

<script>

  import {notifi} from '../notif'
  export default{

    data:function(){

      return{
        form: {
          old_password: '',
          new_password: '',
          email: '',
          phone: ''
        },
        emailOrPhoneChanged: false
      }
    },
    computed: {
      name () {
        return this.$store.state.login.username;
      },
      cemail: {
        get: function() {
          return this.$store.state.login.new_email
        },
        set: function(newVal) {
          this.form.email = newVal
          this.emailOrPhoneChanged = true
        }
      },
      cphone: {
        get: function() {
          return this.$store.state.login.new_phone
        },
        set: function(newVal) {
          this.form.phone = newVal
          this.emailOrPhoneChanged = true
        }
      },
    },
    // created: function (){

    //   form.email = this.$store.state.login.new_email,
    //   form.phone = this.$store.state.login.new_phone
    // },


    components:{
    },

    methods:{
      dj: function(){
        var context = this
        if (this.form.new_password != '') {
          this.$store.dispatch('UserNewpassword', {old_password:this.form.old_password, new_password:this.form.new_password})
          .then(function success(){
            notifi('修改成功', '密码修改成功，请重新登录！', 'success', context)
          }, function fail(){
            context.notif('修改失败', '密码修改失败，请重新登录！', 'error')
          })
        }
        if (this.emailOrPhoneChanged) {
          this.$store.dispatch('UserNewemailphone',{email:this.form.email, phone:this.form.phone})
          .then(function success(){
            context.notif('修改成功', '邮箱或手机修改成功，请重新登录！', 'success')
          }, function fail(){
            context.notif('修改失败', '邮箱或手机修改失败，请重新登录！', 'error')
          })
        }
        
        this.$store.dispatch('UserLogout');
        this.$router.push({ path: '/' })
      },
      notif: function(title, msg, type){
        this.$notify({
          title: title,
          message: msg,
          type: type
        });
      }
    }

  }


</script>

<style lang="less" scoped>

  @import '../style/common';

  .explain_text{
    margin-top: 20px;
    text-align: center;
    font-size: 20px;
    color: #333;
  }
  .admin_title{
    margin-top: 20px;
    text-align: center;
  }

  .demo-ruleForm{

      position: relative;
      margin-left: 30%;
  }

  .input_form{
    margin-top: 20px;
  }
</style>