<template>
	<div class="login">
		<section>
		  <div><br><br><br><br></div>
			<el-row  :gutter="20">
				<el-col :span="8" :offset="11">
				<img src="../assets/bigtouxiang.png">
				</el-col>
				<el-col :span="6" :offset="9">
					<el-card class="box-card" style="margin-top:40px">
						<el-form ref="form" :model="form" action="" role="form">
							<el-col :span="24" >
								<el-form-item>
									<el-input v-model="form.username" id= "username" placeholder="Username"></el-input>
								</el-form-item>
							</el-col>

							<el-col >
								<el-form-item>
									<el-input v-model="form.password" id= "password" placeholder="Password"></el-input>
								</el-form-item>
							</el-col>

<!-- 							<el-col >
								<el-form-item>
									<el-checkbox v-model="checked" style="color: #FFFFFF;">记住我</el-checkbox>
<! 									<router-link to="/register" class="zhucebtn">注册</router-link>

								</el-form-item>
							</el-col> -->


							<el-col>
								<el-form-item :span="12">
									<el-button type="primary" size="large" class="denglubtn" @click="dj">登陆</el-button>
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
    userName: '',
    password: ''
  },
  checked: 'true'
};
},

computed: {
},

methods: {
	dj: function() {
			var obj = JSON.stringify(this.form)
			axios.post('/client/login/', obj)
			.then(function(res){
				res = res.data
				if (res.status.code == '0') { // 注册成功，自动登录
					router.push({path:'/productIntro'})
				} else { // 注册失败
					alert('登录失败！')
				}
				
			})
			.catch(function(err){
				console.log(err)
			}); 
		}
}

}


</script>

<style lang="less">

.login{
	background-image: url("../assets/1.jpg");
	background-repeat:no-repeat;
	height: 100%;
	width: 100%;
}

.box-card{
	
	background: transparent;
	// opacity: 0.7;
	// text-align: center;
}
.denglubtn{
}

.zhucebtn{
	color:#FFFFFF;
}
</style>