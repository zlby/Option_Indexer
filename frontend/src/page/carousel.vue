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
		</div>




		<div class="news">
			<div class="Carousel2">
				<div class="outer" style="padding-top:50px">
					<p class="p1">新闻资讯</p>
					<br>
					<p class="p2">提供最前沿的豆粕期货期权资讯</p>
					<br><br><br>
				</div>

				<el-carousel>
					<el-carousel-item>
						<div class="news_container">
							<el-row :gutter="40">
								<el-col :span="6" :xs="6" :sm="6" :md="6" :lg="6">
									<el-card class="news-card">
										<img src= "../assets/pexels-photo-159888.jpeg">
										<div style="padding: 14px;">
											<p class="H1">{{title[0]}}</p>
											<div class="news-text" style="padding: 14px;">{{context[0]}}</div>
										</div>
										<el-button class="news-btn" type="primary" size="large" style="margin-top:15px">read more</el-button>
									</el-card>
								</el-col>
								<el-col :span="6" :xs="6" :sm="6" :md="6" :lg="6">
									<el-card class="news-card">
										<img src= "../assets/pexels-photo-210574.jpeg">
										<div style="padding: 14px;">
											<p class="H1">{{title[1]}}</p>
											<div class="news-text" style="padding: 14px;">{{context[1]}}</div>
										</div>
										<el-button class="news-btn" type="primary" size="large" style="margin-top:15px">read more</el-button>
									</el-card>
								</el-col>
								<el-col :span="6" :xs="6" :sm="6" :md="6" :lg="6">
									<el-card class="news-card">
										<img src= "../assets/pexels-photo-286442.jpeg">
										<div style="padding: 14px;">
											<p class="H1">{{title[2]}}</p>
											<div class="news-text" style="padding: 14px;">{{context[2]}}</div>
										</div>
										<el-button class="news-btn" type="primary" size="large" style="margin-top:15px">read more</el-button>
									</el-card>
								</el-col>
								<el-col :span="6" :xs="6" :sm="6" :md="6" :lg="6">
									<el-card class="news-card">
										<img src= "../assets/taxes-tax-evasion-police-handcuffs.jpg">
										<div style="padding: 14px;">
											<p class="H1">{{title[3]}}</p>
											<div class="news-text" style="padding: 14px;">{{context[3]}}</div>
										</div>
										<el-button class="news-btn" type="primary" size="large" style="margin-top:15px">read more</el-button>
									</el-card>

								</el-col>
							</el-row>
						</div>
					</el-carousel-item>
				</el-carousel>

			</div>
		</div>
		<footerBottom></footerBottom>
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
		},

		computed: {
			title (){
				return this.$store.state.login.title;
			},
			context (){
				return this.$store.state.login.context;
			},
		},
		mounted:function() {
			this.$store.dispatch('News',0);
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