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


					<el-col>
					<el-form-item>
						<el-input v-model="form.username" id= "username" placeholder="Username"></el-input>
					</el-form-item>
					</el-col>

					<el-col >
					<el-form-item>
						<el-input v-model="form.password" id= "password" placeholder="Password"></el-input>
					</el-form-item>
					</el-col>
					
					<el-col >
					<el-form-item>
						<el-input v-model="form.email" id= "email" placeholder="Email"></el-input>
					</el-form-item>
					</el-col>

					<el-col >
					<el-form-item>
						<el-input v-model="form.phone" id= "phone" placeholder="Phone"></el-input>
					</el-form-item>
					</el-col>

					<el-col>
					<el-form-item :span="6">
						<el-button type="primary" size="large" v-on:click="dj" class="denglubtn">注册</el-button>
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
<<<<<<< HEAD
			// var obj = JSON.stringify(this.form)
=======
>>>>>>> 300b56639c74bfe7e922d8b2eb64be4d96fbc59d
			axios.post('/client/register/', this.form)
			.then(function(res){
				res = res.data
				if (res.status.code == '0') { // 注册成功，自动登录
					router.push('/productIntro')
				} else { // 注册失败
					alert('用户名已存在！')
				}
				
			})
			.catch(function(err){
				alert('用户名已存在！')
			}); 
		}



}

}


</script>

<style lang="less">
	@import '../style/common';
.register{
	background-image: url("../assets/1.jpg");
	background-repeat:no-repeat;
	height: 100%;
	width: 100%;
}

.box-card{
	background: transparent;
	// text-align: center;
}

</style>