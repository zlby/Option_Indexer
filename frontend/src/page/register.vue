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
				<el-form ref="form" :model="form" action="" role="form">


					<el-col :span="24">
					<el-form-item>
						<el-input v-model="form.username" class="input_op" style="margin-top:20px" placeholder="Username"></el-input>
					</el-form-item>
					</el-col>

					<el-col :span="24">
					<el-form-item>
						<el-input v-model="form.password" class="input_op" type="password" placeholder="Password"></el-input>
					</el-form-item>
					</el-col>
					
					<el-col :span="24">
					<el-form-item>
						<el-input v-model="form.email" class="input_op"  placeholder="Email"></el-input>
					</el-form-item>
					</el-col>

					<el-col :span="24">
					<el-form-item>
						<el-input v-model="form.phone" class="input_op" placeholder="Phone"></el-input>
					</el-form-item>
					</el-col>

					<el-col :span="24">
					<el-form-item>
						<el-button type="primary"  v-on:click="dj" class="el-col el-col-xs-24 el-col-md-24 el-col-sm-24 el-col-lg-24">注册</el-button>
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

export default {

 data (){
  return {
	   form: {
	    phone: '',
	    password: '',
	    email: '',
	    username: ''
	  },
	  active: 0
	};
},

computed: {
},
methods: {


	dj: function() {
			this.$store.dispatch('UserRegister', this.form)
			.then(() => {
				this.$store.dispatch('UpdateUserInfo')
			})
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