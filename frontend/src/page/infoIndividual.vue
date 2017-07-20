<template>
  <div>
    <header class="admin_title"><i class="el-icon-edit"></i>      个人信息</header>
    <div class="admin_set">
    <el-col :span="18">
      <el-form :model="form"  :rules="rules2" ref="form" label-width="100px" class="demo-ruleForm">
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
          <el-input v-model="form.email" ></el-input>
<!--           <el-input type="name" :value="name" ></el-input> -->
        </el-form-item>

        <el-form-item label="手机号码" class="input_form">
          <el-input v-model="form.phone" :value="phone"></el-input>
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
  export default{

    data:function(){

      return{
        form: {
          old_password: '',
          new_password: '',
          email: '',
          phone: ''
        }
      }
    },
    computed: {
      name () {
        return this.$store.state.login.username;
      },
      email () {
        return this.$store.state.login.new_email;
      },
      phone (){
        return this.$store.state.login.new_phone;
      }
    },


    components:{
    },

    methods:{
      dj: function(){
        this.$store.dispatch('UserNewpassword', {old_password:this.form.old_password,
          new_password:this.form.new_password});
        this.$store.dispatch('UserNewemailphone',{email:this.form.email,
          phone:this.form.phone});
      },
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