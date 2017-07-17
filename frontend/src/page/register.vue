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

// 	export default{
//     data() {
//       return {
//         form: {
//           username: '',
//           password: '',
//           email: '',
//           phone: ''
//         }
//       }
//     },
//     methods: {
//       onSubmit() {
//         console.log('submit!');
//       }
//   }
// }

import axios from 'axios'

export default {

 data (){
  return {
   form: {
    phone: '',
    password: '',
    email: '',
    phone: ''
  },
  active: 0
};
},

computed: {
},

methods: {


	dj: function() {
			// console.log(this.form)      ////返回的是一个包含很多内容东西的对象 里边还有不想要的东西
			
			// console.log(obj)
			// instance.post('/client/register/',obj)
			// .then(function() {
			// 	console.log(response);
			// })
			// .catch(function(error) {
			// 	console.log(error);
			// });
			var obj = JSON.stringify(this.form);
			axios.post('/client/register/', obj)
			.then(function(res){
				console.log(res);
			})
			.catch(function(err){
				console.log(err);
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