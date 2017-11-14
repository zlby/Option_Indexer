<template>
	<div class="homepage fillcontain">
		<head-top_en></head-top_en>
		<transition name="slide">
		<router-view></router-view>
		</transition>

<!-- 		<footerBottom></footerBottom> -->
	</div>
</template>

<script>
	import headTop_en from '../componentsEN/headTop_en'
	import footerBottom_en from '../componentsEN/footerBottom_en'
	export default{

		components:{
			headTop_en,
			 footerBottom_en,
		},

		data(){
			return{
				items:[
				{
					img: '../assets/附件切图/样图.png',
				}
			]
		}
	}
}

</script>

<style lang="less">
@import '../style/common';

	.el-carousel{
		width:100%;
	}
  .el-carousel__item h3 {
    color: #475669;
    font-size: 18px;
    opacity: 0.75;
    line-height: 800px;

    margin: 0;
  }

  .el-carousel__item:nth-child(2n) {
    background-color: #99a9bf;
  }

  .el-carousel__item:nth-child(2n+1) {
    background-color: #d3dce6;
  }

</style>
