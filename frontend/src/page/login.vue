<template>
	<div>
		<section>
		  <div><br><br><br><br></div>
			<el-row  :gutter="20">
				<el-form ref="form" :model="form" label-width="80px" method="post" @submit.prevent="reg()">
					<el-col :span="8" :offset="8">
					<el-form-item label="昵称">
						<el-input v-model="form.username" id= "username" placeholder="请输入昵称"></el-input>
					</el-form-item>
					</el-col>
					<el-col :span="8" :offset="8">
					<el-form-item label="密码">
						<el-input v-model="form.password" id= "password" placeholder="请输入密码"></el-input>
					</el-form-item>
					</el-col>

					<el-col :span="8" :offset="8">
					<el-form-item label="邮箱">
						<el-input v-model="form.email" id="email" placeholder="请输入邮箱" ></el-input>
					</el-form-item>
					</el-col>

					<el-col :span="8" :offset="8">
					<el-form-item label="手机号码">
						<el-input v-model="form.phone" id="phone" placeholder="请输入手机号码"></el-input>
					</el-form-item>
					</el-col>


					<el-col :span="8" :offset="8">
					<el-form-item>
                    <p>
                        可通过该手机号码快速找到密码<br>
                        中国大陆地区以外手机号码<a href="#">  点击这里</a>
                    </p>
					</el-form-item>
					</el-col>
					<el-col :span="8" :offset="8">
					<el-form-item>
						<el-button type="primary" size="large" @click="submitForm">立即注册</el-button>
            <router-link to="/" class="btn btn-default">返回</router-link>
					</el-form-item>
					</el-col>
				</el-form>
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

export default {

 data (){
  return {
   form: {
    userName: '',
    password: '',
    email: '',
    phone: ''
  }
}
},
computed: {
},

methods: {
  reg(){
    this.$store.dispatch('UserReg',this.user);
  }
}

}


</script>

<style>
</style>