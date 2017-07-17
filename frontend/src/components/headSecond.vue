<template>
<div class="second">
		<el-row :gutter="20" style="margin-left: 0px; margin-right: 0px;">
		<el-menu class="el-menu-demo3" mode="horizontal" router>
		<el-col :span= "4">
			<el-menu-item index="/"><i class="el-icon-share"></i></el-menu-item>
			<el-menu-item index="/">我的主页</el-menu-item>
		</el-col>

		<el-col :span= "4">
			<el-menu-item><i class="el-icon-menu"></i></el-menu-item>
			<el-menu-item index="/productIntro" >中文</el-menu-item>
			<el-menu-item index="/use"><i class="el-icon-search"></i></el-menu-item>
		</el-col>
		
		<el-col :span="7" :offset="9">
			<el-menu-item  index="/login"><i class="el-icon-message"></i></el-menu-item>
			<el-menu-item><img src="../assets/bigtouxiang.png"></el-menu-item>
			<el-menu-item>
				<el-dropdown>
					<span class="el-dropdown-link">
						周思尧<i class="el-icon-caret-bottom el-icon--right"></i>
					</span>
					<el-dropdown-menu slot="dropdown">
						<el-dropdown-item><i class="el-icon-setting"></i>
							<el-button type="text" @click="dialogFormVisible = true">个人信息设置</el-button>
						</el-dropdown-item>


						<el-dropdown-item><i class="el-icon-edit"></i>
						账号切换
						</el-dropdown-item>

						<el-dropdown-item><i class="el-icon-arrow-left"></i>
						注销
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
		</el-col>
		</el-menu>
		</el-row>
</div>
</template>

<script>
	export default {
	data() {
      return {
        dialogFormVisible: false,
        form: {
    		userName: '',
   		    password: '',
   		    newpassword: '',
   		    email: '',
   		    phone: ''
        },

      };
    },
    methods:{
    	      handleClose(done) {
        this.$confirm('确认关闭？')
          .then(_ => {
            done();
          })
          .catch(_ => {});
      }
    }
 }
</script>

<style lang="less">

	@import '../style/common';

	.el-menu-demo3{
		width:100%;
background-repeat:no-repeat; 
background-size:100% 100%;
-moz-background-size:100% 100%;
		padding-left: 0px;
    	padding-right: 0px;
    	height: 60px;
		z-index: 3;

	}
	.el-menu-demo3 .el-menu-item{
		color:#000000;
	}
	.el-menu-demo3 img{
		width: 60px;
		height: 60px;
	}

	.el-menu--horizontal .el-menu-item:hover, .el-menu--horizontal .el-submenu__title:hover {
    background-color: #eef1f600;
    }
	
	.el-menu-demo3 .el-col:nth-child(1){
		background-color: #FFCC66;
	}

	.second{
				margin-right: 0px;
		margin-left: 0px;
	}

	.el-dialog{
	width: 800px;
	height: 600px;
}

</style>