<template>
	<div class="homepage">
		<div class="Carousel1">
			<el-carousel>
				<el-carousel-item>
					<div class="inner">
						<p class="p1">INDEXER</p>
						<br>
						<p class="p2">提供最前沿的豆粕期货期权资讯</p>
						<br><br><br><br>
						<el-button class="button1">learn more</el-button>
					</div>
					<!-- 					<img src= "../assets/background1.png"> -->
				</el-carousel-item>
				<el-carousel-item>
					<div class="inner">
						<p class="p1">INDEXER</p>
						<br>
						<p class="p2">提供最前沿的豆粕期货期权资讯</p>
						<br><br>						<br><br>
						<el-button class="button1">learn more</el-button>
					</div>
					<!-- 					<img src= "../assets/background1.png"> -->
				</el-carousel-item>
				<el-carousel-item>
					<div class="inner">
						<p class="p1">INDEXER</p>
						<br>
						<p class="p2">提供最前沿的豆粕期货期权资讯</p>
						<br><br>						<br><br>
						<el-button class="button1">learn more</el-button>
					</div>
					<!-- 					<img src= "../assets/background1.png"> -->
				</el-carousel-item>
				<el-carousel-item>
					<div class="inner">
						<p class="p1">INDEXER</p>
						<br>
						<p class="p2">提供最前沿的豆粕期货期权资讯</p>
						<br><br>						<br><br>
						<el-button class="button1">learn more</el-button>
					</div>
					<!-- <img src= "../assets/background1.png"> -->
				</el-carousel-item>

			</el-carousel>

		<footerBottom></footerBottom>
		</div>
</div>

	</template>

	<script>
		import footerBottom from '../components/footerBottom'
		export default{

			components:{
			 footerBottom,
			},

			data(){
				return{
					form: {
						name: '',
						email: '',
						desc: ''
					}

				}
			}
		}

	</script>

	<style lang="less">
		@import '../style/common';
		.el-carousel img{
			width:100%;
			clear:both;
		}


		.Carousel1 .el-carousel__container{
			height: 730px;
		}

		.Carousel2 .el-carousel__container{
			height: 550px;
		}

		.el-carousel{
			position:relative;
		}

		.news-card{
			min-width: 200px;
		}

		.news-text{
			white-space: nowrap;
			text-overflow:ellipsis;
			overflow:hidden;

		}

		.news-btn{
			width:100%;
			border-top-left-radius: 0px;
			border-top-right-radius: 0px;
		}

		.Carousel1 .el-carousel__item{
			background-image: url("../assets/background1_副本.png");
		}

		.Carousel2 .el-carousel__item{
			background-color: #FFFFFF;
		}

		.el-card{
			background-color: #F3F3F3;
		}

		.news{
			background-color: #FFFFFF;
		}

		.fillcontain{
			height: 100%;
			width: 100%;
		}

		.inner{
			text-align: center;
			z-index: 4;
			margin:-150px auto;
			top:50%;
			color:#fff;
			height:300px;
			position:relative;

		}
		.H1{
			text-align: center;
			font-size: 30px;	
		}

		.el-card__body{
			padding: 0px;
		}

		.news_container{
			width: 80%;
			margin: auto;
		}

		.p1{
			font-size: 60px;
			text-align:center;
		}
		.p2{

			font-size: 30px;
			text-align:center;
		}

		.button1{
			background-color: transparent;
			color:#fff;
		}


		.promotion{
			background-image: url("../assets/1.jpg");
		}

		.homepage{
			background-color: #E8E8E8;
		}
		.pic1{
			width: 600px;
			height: 400px;
			padding-top: 50px;
		}
		.pic2{
			width: 600px;
			height: 400px;
			padding-bottom: 50px;
			float: right;
		}

		.news-btn{
			margin-right: 200px;
			text-align: center;
		}

	</style>