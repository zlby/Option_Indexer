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
		<el-col :span="4" :offset="1">
			<el-menu-item index= "/login" >登陆</el-menu-item>

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


			<el-menu-item index="/register">注册</el-menu-item>	
		</el-col>
<!-- 			<el-menu-item index="9"><img src="../assets/附件切图/云.png" class="touxiang1"></el-menu-item>	
			<el-menu-item index="8"><img src="../assets/附件切图/搜索.png" class="touxiang1"></el-menu-item>	 -->		
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
    password: ''
        },
        formLabelWidth: '120px'
      };
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