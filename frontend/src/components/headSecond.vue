<template>
<div class="second">
		<el-row >
		<el-menu class="el-menu-demo3" mode="horizontal" router>
		<el-col :span= "5" :xs="5" :md="5" :lg="5" :sm="5"style="background-color: #FFCC66; min-width:200px">
			<el-menu-item index="/" class="el-col el-col-8 el-col-xs-8 el-col-md-8 el-col-sm-8 el-col-lg-8"><i class="el-icon-share"></i></el-menu-item>
			<el-menu-item index="/homepageIndividual/list" class="el-col el-col-16 el-col-xs-16 el-col-md-16 el-col-sm-16 el-col-lg-16">个人主页</el-menu-item>
		</el-col>
		</el-menu>
		</el-row>
</div>
</template>

<script>
	export default {
	data() {
      return {
      };
    }
 }
</script>

<style lang="less">

	@import '../style/common';

// 	.el-menu-demo3{
// 		width:100%;
// background-repeat:no-repeat;
// background-size:100% 100%;
// -moz-background-size:100% 100%;
// 		padding-left: 0px;
//     	padding-right: 0px;
//     	height: 60px;
// 		z-index: 3;

// 	}
// 	.el-menu-demo3 .el-menu-item{
// 		color:#000000;
// 	}
// 	.el-menu-demo3 img{
// 		width: 60px;
// 		height: 60px;
// 	}

// 	.el-menu--horizontal .el-menu-item:hover, .el-menu--horizontal .el-submenu__title:hover {
//     background-color: #eef1f600;
//     }

// 	.yellow{
// 		background-color: #FFCC66;
// 	}

// 	.second{
// 		margin-right: 0px;
// 		margin-left: 0px;
// 	}


</style>
