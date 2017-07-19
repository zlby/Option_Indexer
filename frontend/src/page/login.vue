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
						<el-form ref="form" :model="form" action="" role="form" :rules="rules2" class="demo-ruleForm">
							<el-col :span="20" :offset="2">
								<el-form-item>
									<el-input v-model="form.username"  style="margin-top:20px" id= "username" placeholder="Username"></el-input>
								</el-form-item>
							</el-col>

							<el-col :span="20" :offset="2">
								<el-form-item>
									<el-input  type="password" v-model="form.password" id= "password" placeholder="Password" auto-complete="off"></el-input>
								</el-form-item>
							</el-col>

							<el-col :span="20" :offset="2">
								<el-form-item>
									<el-button class="el-col el-col-xs-24 el-col-md-24 el-col-sm-24 el-col-lg-24" type="primary"   @click="dj">登陆</el-button>
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
	background-image: url("../assets/背景.jpg");
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