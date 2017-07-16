<template>
	<div class = "navigate">
	<el-row :gutter="20">
		<el-menu :default-active="activeIndex" class="el-menu-demo1" mode="horizontal" @select="handleSelect" router>
		<el-col :span = "4" :offset ="3">
			<el-menu-item index="/"><img src="../assets/bigtouxiang1.png" class="touxiang"></el-menu-item>	
		</el-col>
		<el-col :span = "5" :offset = "7">
			<el-menu-item index="/">首页</el-menu-item>		
			<el-menu-item index="/productIntro" >产品介绍</el-menu-item>
			<el-menu-item index="/use">信息资源</el-menu-item>
		</el-col>	
		<el-col :span = "5">
			<el-menu-item >登陆</el-menu-item>



			<el-menu-item index="/login">注册</el-menu-item>	
		</el-col>
<!-- 			<el-menu-item index="9"><img src="../assets/附件切图/云.png" class="touxiang1"></el-menu-item>	
			<el-menu-item index="8"><img src="../assets/附件切图/搜索.png" class="touxiang1"></el-menu-item>	 -->		
		</el-menu>
	</el-row>
	</div>



</template>

<script>
  export default {

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

</style>