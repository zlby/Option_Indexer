<template>
	<div class = "navigate2">

		<el-menu :default-active="activeIndex2" class="el-menu-demo" mode="horizontal" @select="handleSelect" fixed="true">
			<el-row>
			<el-col :span="8"><el-menu-item index="1">链接网址</el-menu-item></el-col>
			<el-col :span="8"><el-menu-item index="2">各种网站</el-menu-item></el-col>
			<el-col :span="8"><el-menu-item index="3">附属网址</el-menu-item></el-col>

			</el-row>
		</el-menu>
	</div>



</template>

<script>
	export default {
		data() {
			return {
				activeIndex: '1',
				activeIndex2: '1'
			};
		},
		methods: {
			handleSelect(key, keyPath) {
				console.log(key, keyPath);
			}
		}
	}
</script>

<style>
.el-menu-demo{
	width: 100%;
	bottom: 0px;
	position: relative;
    background-color:#404040;
    color:#FFF;

}
*{
	margin:0px;
}


</style>