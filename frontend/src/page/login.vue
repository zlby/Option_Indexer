<template>
	<div class="login">
		  <div><br><br><br><br></div>
			<el-row  :gutter="20">
				<div class="login_pic">
				<img src="../assets/login_icon.png">
				</div>
				<el-col :span="6" :offset="9"   :xs="6" :md="6" :lg="6" :sm="6">
					<el-card class="box-card" style="margin-top:40px">
						<el-form ref="form" :model="form" action="" role="form" :rules="rules2" class="demo-ruleForm">
							<el-col :span="24" :xs="24" :md="24" :lg="24" :sm="24">
								<el-form-item>
									<el-input v-model="form.username" class="input_op" style="margin-top:20px" placeholder="Username"></el-input>
								</el-form-item>
							</el-col>

							<el-col :span="24" :xs="24" :md="24" :lg="24" :sm="24">
								<el-form-item>
									<el-input  type="password" class="input_op" v-model="form.password" placeholder="Password" auto-complete="off"></el-input>
								</el-form-item>
							</el-col>

							<el-col :span="24"  :xs="24" :md="24" :lg="24" :sm="24">
								<el-form-item>
									<el-button class="el-col el-col-xs-24 el-col-md-24 el-col-sm-24 el-col-lg-24" type="primary"   @click="dj">登陆</el-button>
								</el-form-item>
							</el-col>
						</el-form>
					</el-card>
				</el-col>
			</el-row>
	</div>
</template>

<script>
import axios from 'axios'
import router from '../router'
  import { mapActions } from 'vuex'
export default {
 data (){
      var validatePass = (rule, value, callback) => {
        if (value === '') {
          callback(new Error('请输入密码'));
        } 
      };
  return {
   form: {
    username: '',
    password: ''
  },
  rules2: {
          password: [
            { validator: validatePass, trigger: 'blur' }
          ],
      },
  checked: 'true'

};
},

methods: {
	dj: function() {
			this.$store.dispatch('UserLogin', this.form)
			.then(() => {
				this.$store.dispatch('UpdateUserInfo')
			})
		}
}

}


</script>

<style lang="less">

.login_pic{
	margin: auto;
	position: relative;
	width: 100px;
}

.login{
	background-image: url("../assets/背景.jpg");
	background-repeat:no-repeat;
	height: 100%;
	width: 100%;
	// margin: auto;
	// position: relative;
}

.box-card{
	background-color: rgba(255,255,255,0.1);
}



.input_op{
	// background-color: white;
	 opacity: 0.82;
	// position:relative;
background-color: rgb(256,256,256);
	position: relative;
	color:white;
	border-radius: 10px;

	border:0px;
}
.el-input__inner{

}

.zhucebtn{
	color:#FFFFFF;
}
</style>