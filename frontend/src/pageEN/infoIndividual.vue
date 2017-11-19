<template>
  <div>
    <header class="admin_title"><i class="el-icon-edit"></i>      Personal Info</header>
    <div class="admin_set">
    <el-col :span="18">
      <el-form :model="form" ref="form" label-width="100px" class="demo-ruleForm">
        <el-form-item label="nickname" class="input_form">
          <el-input type="name" :value="name" :disabled="true" ></el-input>
        </el-form-item>

        <el-form-item label="old password" prop="pass" class="input_form">
          <el-input type="password" v-model="form.old_password" ></el-input>
        </el-form-item>

        <el-form-item label="new password" prop="checkPass" class="input_form">
          <el-input type="password" v-model="form.new_password"></el-input>
        </el-form-item>

        <el-form-item label="Email" class="input_form">
          <el-input v-model="cemail" ></el-input>
<!--           <el-input type="name" :value="name" ></el-input> -->
        </el-form-item>

        <el-form-item label="Cellphone Number" class="input_form">
          <el-input v-model="cphone"></el-input>
        </el-form-item>

        <el-form-item class="input_form">
          <el-button type="primary" @click="dj">Submit</el-button>
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
            notifi('Successfully modified', 'password modified successfully ，please login again！', 'success', context)
          }, function fail(){
            context.notif('Modification failed', 'password modification failed，please login again！', 'error')
          })
        }
        if (this.emailOrPhoneChanged) {
          this.$store.dispatch('UserNewemailphone',{email:this.form.email, phone:this.form.phone})
          .then(function success(){
            context.notif('Successfully modified', 'E-mail or mobile phone modified successfully, please log in again!', 'success')
          }, function fail(){
            context.notif('Modification failed', 'E-mail or mobile phone modification failed, please log in again!', 'error')
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
