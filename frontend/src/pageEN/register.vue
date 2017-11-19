<template>
	<div class="register">
		<section>
		  <div><br><br><br><br></div>
			<el-row  :gutter="20">
			<div class="regis_pic">
				<img src="../assets/regis_icon.png">
			</div>
				<el-col :span="6" :offset="9">
				<el-card class="box-card" style="margin-top:40px">
				<el-form ref="form" :model="form" role="form" :rules="rule">
					<el-col :span="24">
					<el-form-item prop="username">
						<el-input v-model="form.username" class="input_op" style="margin-top:20px" placeholder="Username"></el-input>
					</el-form-item>
					</el-col>

					<el-col :span="24">
					<el-form-item prop="password">
						<el-input v-model="form.password" class="input_op" type="password" placeholder="Password"></el-input>
					</el-form-item>
					</el-col>

					<el-col :span="24">
					<el-form-item prop="checkpassword">
						<el-input v-model="form.checkpassword" class="input_op" type="password" placeholder="Confirm Password"></el-input>
					</el-form-item>
					</el-col>



					<el-col :span="24">
					<el-form-item prop="email">
						<el-input v-model="form.email" class="input_op"  placeholder="Email"></el-input>
					</el-form-item>
					</el-col>

					<el-col :span="24">
					<el-form-item prop="phone">
						<el-input v-model="form.phone" class="input_op" placeholder="Phone"></el-input>
					</el-form-item>
					</el-col>

					<el-col :span="24">
					<el-form-item>
						<el-button type="primary"  v-on:click="dj('form')" class="el-col el-col-xs-24 el-col-md-24 el-col-sm-24 el-col-lg-24">Register</el-button>
					</el-form-item>
					</el-col>
				</el-form>

				</el-card>
				</el-col>
			</el-row>
		</section>

	</div>
</template>

<script>

import axios from 'axios'
import router from '../router'
import {notifi} from '../notif'

export default {

 data (){

	var validatePass = (rule, value, callback) => {
        if (value === '') {
          callback(new Error('Please enter your password again'));
        } else if (value !== this.form.password) {
          callback(new Error('Two passwords are not consistent!'));
        } else {
          callback();
        }
      };


  return {
	   form: {
	    phone: '',
	    password: '',
	    email: '',
	    username: '',
	  },
	  rule:{
	  	username: [
	  	{ required: true, message: 'Please enter your username', trigger: 'blur' },
	  	{ min: 0, max: 10, message: 'The length is between 0 to 10 characters', trigger: 'blur' }
	  	],
	    password: [
	  	{ required: true, message: 'Please enter password', trigger: 'blur' }
	  	],
	  	email: [
	  	{ required: true, message: 'Please enter your Email', trigger: 'blur' }
	  	],
	  	phone: [
	  	{ required: true, message: 'Please enter your mobilephone number', trigger: 'blur' }
	  	],
	  	checkpassword: [
	  	{ validator: validatePass, trigger: 'blur' }
	  	]
	  },
	  active: 0
	};
},

computed: {
},
methods: {


	dj: function(formname) {
		var context = this
        this.$refs[formname].validate((valid) => {
          if (valid) {
   //          this.$store.dispatch('UserRegister', this.form)
			// .then(() => {
			// 	this.$store.dispatch('UpdateUserInfo')
			// })

			this.$store.dispatch('UserRegister_en', this.form)
			.then(function success(){
	        	notifi('Successfully registered', 'Welcome,' + context.form.username, 'success', context)
	        	context.$store.dispatch('UpdateUserInfo')
	        }, function fail(){
	        	notifi('Registeration failed', 'The username you entered has been registered', 'error', context)
	        })

          } else {
            notifi('Registeration failed', 'Username or password is invalid', 'error', context)
            return false;
          }
        });
		},

	    next() {
	    	if (this.active++ > 1)
	        	this.active = 0;
	    }
	}



}



</script>

<style lang="less">
	@import '../style/common';

.regis_pic{
	margin: auto;
	position: relative;
	width: 100px;
}

.register{
	background-image: url("../assets/背景.jpg");
	background-repeat:no-repeat;
	height: 100%;
	width: 100%;
}

.box-card{
	background-color: rgba(255,255,255,0.1);
	// text-align: center;
}

.input_op{
	// background-color: white;
	 opacity: 0.82;
	// position:relative;
background-color: rgb(256,256,256);
	position: relative;
	color:white;
	border-radius:10px;
}

.input_op::-webkit-input-placeholder{
    color: red;
    font-size: 30px;
}

</style>
