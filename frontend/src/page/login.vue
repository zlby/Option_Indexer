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
						<el-form ref="form" :model="form" action="" role="form" 
						:rules="rules2" class="demo-ruleForm">
							<el-col :span="24" >
								<el-form-item>
									<el-input v-model="form.username" id= "username" placeholder="Username"></el-input>
								</el-form-item>
							</el-col>

							<el-col >
								<el-form-item>
									<el-input  type="password" v-model="form.password" id= "password" placeholder="Password" auto-complete="off"></el-input>
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
			this.$store.dispatch('UserLogin', this.form);
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