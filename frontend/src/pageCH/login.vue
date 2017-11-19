<template>
	<div class="login">
		  <div><br><br><br><br></div>
			<el-row  :gutter="20">
				<div class="login_pic">
				<img src="../assets/login_icon.png">
				</div>
				<el-col :span="6" :offset="9"   :xs="6" :md="6" :lg="6" :sm="6">
					<el-card class="box-card" style="margin-top:40px">
						<el-form ref="form" :model="form" action="" role="form" :rules="rules2" class="demo-ruleForm" @keyup.enter.native="dj('form')">
							<el-col :span="24" :xs="24" :md="24" :lg="24" :sm="24">
								<el-form-item prop="username">
									<el-input v-model="form.username" class="input_op" style="margin-top:20px" placeholder="Username"></el-input>
								</el-form-item>
							</el-col>

							<el-col :span="24" :xs="24" :md="24" :lg="24" :sm="24">
								<el-form-item prop="password">
									<el-input  type="password" class="input_op" v-model="form.password" placeholder="Password" auto-complete="off"></el-input>
								</el-form-item>
							</el-col>

							<el-col :span="24"  :xs="24" :md="24" :lg="24" :sm="24">
								<el-form-item>
									<el-button class="el-col el-col-xs-24 el-col-md-24 el-col-sm-24 el-col-lg-24" type="primary"  @click="dj('form')">登陆</el-button>
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
  import { notifi } from '../notif'
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
  				// password: [
  				// { validator: validatePass, trigger: 'blur' }
  				// ],
  				username: [
  				{ required: true, message: '请输入账号名', trigger: 'blur' },
  				{ min: 0, max: 10, message: '长度在 0 到 10 个字符', trigger: 'blur' }
  				],
  			},
  			checked: 'true'

  		}
  	},

  	methods: {
  		dj: function(formname) {
  			var context = this

  			this.$refs[formname].validate((valid) => {
  				if (valid) {
  					this.$store.dispatch('UserLogin_ch', this.form)
  					.then(function success(){
			        	notifi('登录成功', '欢迎您，'+context.$store.state.login.username, 'success', context)
			        	context.$store.dispatch('UpdateUserInfo')
			        	context.$store.dispatch('getNotification')
			        }, function fail(){
			        	notifi('登录失败', '用户名或密码错误', 'error', context)
			        })
  				} else {
  					notifi('登录失败', '用户名或密码不合法！', 'error', context)
  					return false;
  				}
  			});
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
