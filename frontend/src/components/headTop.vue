<template>
	<div class = "navigate">
	<el-row>
		<el-menu class="el-menu-demo1" mode="horizontal" router>
		<el-col :span = "4" :offset ="3">
			<el-menu-item index="/"><img src="../assets/bigtouxiang1.png" class="touxiang"></el-menu-item>	
		</el-col>
		<el-col :span="6" :offset="6">
			<el-menu-item index="/">首页</el-menu-item>		
			<el-menu-item index="/productIntro" >产品介绍</el-menu-item>
			<el-menu-item index="/use">信息资源</el-menu-item>
		</el-col>
<!-- 			<el-dialog :visible.sync="dialogFormVisible" :modal-append-to-body="false" :modal="false">
				<el-form :model="form">

					<el-form-item>
						<el-input v-model="form.username" id= "username" placeholder="Username"></el-input>
					</el-form-item>

					<el-form-item>
						<el-input v-model="form.password" id= "password" placeholder="Password"></el-input>
					</el-form-item>

				</el-form>
				<div slot="footer" class="dialog-footer">
					<el-button type="primary" @click="dialogFormVisible = false">确 定</el-button>
				</div>
			</el-dialog> -->

		<el-col :span="4" offset="1" v-if="loggedin==false">
			<el-menu-item index= "/login" >登录</el-menu-item>
			<el-menu-item index="/register">注册</el-menu-item>	
		</el-col>
		<el-col :span="4" offset="1" v-else>


            <el-menu-item  index="/login"><i class="el-icon-message"></i></el-menu-item>
            <el-menu-item><img style="width: 60px; height: 60px;" src="../assets/bigtouxiang.png"></el-menu-item>
            <el-menu-item>
                <el-dropdown>
                    <span class="el-dropdown-link">
                        {{name}}<i class="el-icon-caret-bottom el-icon--right"></i>
                    </span>
                    <el-dropdown-menu slot="dropdown">
                        <el-dropdown-item><i class="el-icon-setting"></i>
                            <el-button type="text" @click="dialogFormVisible = true">个人信息设置</el-button>
                        </el-dropdown-item>


                        <el-dropdown-item><i class="el-icon-edit"></i>
                        账号切换
                        </el-dropdown-item>

                        <el-dropdown-item><i class="el-icon-arrow-left"></i>
                        <el-button type="text" @click="logout">注销</el-button>
                        </el-dropdown-item>

                    </el-dropdown-menu>

                    <el-dialog title="信息修改" :visible.sync="dialogFormVisible" :modal-append-to-body="false" :before-close="handleClose">
                        <el-form :model="form">
                            <el-form-item>
                                <el-input v-model="form.username" id= "username" placeholder="Username"></el-input>
                            </el-form-item>
                            <el-form-item>
                                <el-input v-model="form.password" id= "password" placeholder="Password"></el-input>
                            </el-form-item>
                            <el-form-item>
                                <el-input v-model="form.newpassword" id= "newpassword" placeholder="newPassword"></el-input>
                            </el-form-item>
                            <el-form-item>
                                <el-input v-model="form.email" id= "email" placeholder="Email"></el-input>
                            </el-form-item>
                            <el-form-item>
                                <el-input v-model="form.phone" id= "phone" placeholder="Phone"></el-input>
                            </el-form-item>
                        </el-form>
                        <div slot="footer" class="dialog-footer">
                            <el-button @click="dialogFormVisible = false">取 消</el-button>
                            <el-button type="primary" @click="dialogFormVisible = false">确 定</el-button>
                        </div>
                    </el-dialog>

                </el-dropdown>
            </el-menu-item>




			<!-- <el-menu-item index= "/login" >{{name}}</el-menu-item>
			<el-menu-item index="/register">信息</el-menu-item>	 -->
		</el-col>


		</el-menu>
	</el-row>
	</div>



</template>

<script>
  import {mapGetters} from 'vuex'
  export default {
  	data() {
      return {
        dialogFormVisible: false,
        form: {
		    username: '',
		    password: ''
        },
        formLabelWidth: '120px'
      };
    },
    computed: {
    	loggedin () {
    		return this.$store.state.login.loggedin;
    	},
    	name () {
    		return this.$store.state.login.username;
    	}
    },
    methods: {
    	logout: function() {
    		this.$store.dispatch('UserLogout');
    	}
    }
}
</script>

<style lang="less">

	@import '../style/common';

	.el-menu-demo1{
		width:100%;
background-repeat:no-repeat; 
background-size:100% 100%;
-moz-background-size:100% 100%;
		padding-left: 0px;
    	padding-right: 0px;
    	height: 60px;
		z-index: 3;
		background-color:#404040;
	}
	.el-menu-item{
		color:#fff;
	}


	.el-menu--horizontal .el-menu-item:hover, .el-menu--horizontal .el-submenu__title:hover {
    background-color: #eef1f600;
}

.touxiang{
	width: 58px;
	height: 58px;
}

.touxiang1{
	color:white;
	-webkit-filter: drop-shadow(#FFFFFF 0px 0);filter: drop-shadow(#FFFFFF 0px 0);   
}


#username{
	opacity:0.90;
}

#password{
	opacity: 0.90;
}

</style>