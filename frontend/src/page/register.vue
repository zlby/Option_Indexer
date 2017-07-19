<template>
	<div class="register">
		<section>
		  <div><br><br><br><br></div>
			<el-row  :gutter="20">
				<el-col :span="8" :offset="11">
				<img src="../assets/bigtouxiang.png">
				</el-col>
				<el-col :span="6" :offset="9">
				<el-card class="box-card" style="margin-top:40px">
				<el-form ref="form" :model="form" action="" role="form">


					<el-col :span="20" :offset="2">
					<el-form-item>
						<el-input v-model="form.username" style="margin-top:20px" id= "username" placeholder="Username"></el-input>
					</el-form-item>
					</el-col>

					<el-col :span="20" :offset="2">
					<el-form-item>
						<el-input v-model="form.password" type="password" id= "password" placeholder="Password"></el-input>
					</el-form-item>
					</el-col>
					
					<el-col :span="20" :offset="2">
					<el-form-item>
						<el-input v-model="form.email" id= "email" placeholder="Email"></el-input>
					</el-form-item>
					</el-col>

					<el-col :span="20" :offset="2">
					<el-form-item>
						<el-input v-model="form.phone" id= "phone" placeholder="Phone"></el-input>
					</el-form-item>
					</el-col>

					<el-col :span="20" :offset="2">
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
			this.$store.dispatch('UserRegister', this.form);
		}



}

}


</script>

<style lang="less">
	@import '../style/common';
.register{
	background-image: url("../assets/背景.jpg");
	background-repeat:no-repeat;
	height: 100%;
	width: 100%;
}

.box-card{
	background: transparent;
	// text-align: center;
}

</style>