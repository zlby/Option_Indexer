<template>
<div class="second">
		<el-row :gutter="20" style="margin-left: 0px; margin-right: 0px;">
		<el-menu :default-active="activeIndex" class="el-menu-demo3" mode="horizontal" @select="handleSelect" router>
		<el-col :span= "4">
			<el-menu-item index="/"><i class="el-icon-share"></i></el-menu-item>
			<el-menu-item index="/">我的主页</el-menu-item>
		</el-col>

		<el-col :span= "4">
			<el-menu-item index="11"><i class="el-icon-menu"></i></el-menu-item>
			<el-menu-item index="/productIntro" >中文</el-menu-item>
			<el-menu-item index="/use"><i class="el-icon-search"></i></el-menu-item>
		</el-col>
		
		<el-col :span="7" :offset="9">
			<el-menu-item  index="11"><i class="el-icon-menu"></i></el-menu-item>
			<el-menu-item  index="/login"><i class="el-icon-information"></i></el-menu-item>
			<el-menu-item  index="/login"><i class="el-icon-message"></i></el-menu-item>
			<el-menu-item  index="8"><img src="../assets/bigtouxiang.png"></el-menu-item>
			<el-menu-item  index="9">周思尧</el-menu-item>
		</el-col>
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
</style>