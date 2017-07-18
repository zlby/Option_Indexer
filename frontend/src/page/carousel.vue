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
								<el-row :gutter="20">
									<el-col :span="6" :xs="6" :sm="6" :md="6" :lg="6">
										<el-card class="news-card">
											<img src= "../assets/pexels-photo-159888.jpeg">
											<div style="padding: 14px;">
												<p class="H1">全国金融工作会议</p>
												<div class="news-text" style="padding: 14px;">今年以来，中国高层在不同场合多次谈及金融议题。决策层提出“金融活，经济活”，将其摆在经济工作突出位置。此次会议进一步强调，金融是国家重要的核心竞争力，金融安全是国家安全的重要组成部分，金融制度是经济社会发展中重要的基础性制度。</div>
											</div>
											<el-button class="news-btn" type="primary" size="large" style="margin-top:15px">read more</el-button>
										</el-card>
									</el-col>
									<el-col :span="6" :xs="6" :sm="6" :md="6" :lg="6">
										<el-card class="news-card">
											<img src= "../assets/pexels-photo-159888.jpeg">
											<div style="padding: 14px;">
												<p class="H1">全国金融工作会议</p>
												<div class="news-text" style="padding: 14px;">今年以来，中国高层在不同场合多次谈及金融议题。决策层提出“金融活，经济活”，将其摆在经济工作突出位置。此次会议进一步强调，金融是国家重要的核心竞争力，金融安全是国家安全的重要组成部分，金融制度是经济社会发展中重要的基础性制度。金融是国家重要的核心竞争力，金融安全是国家安全的重要组成部分，金融制度是经济社会发展中重要的基础性制度。</div>
											</div>
											<el-button class="news-btn" type="primary" size="large" style="margin-top:15px">read more</el-button>
										</el-card>
									</el-col>
									<el-col :span="6" :xs="6" :sm="6" :md="6" :lg="6">
										<el-card class="news-card">
											<img src= "../assets/pexels-photo-159888.jpeg">
											<div style="padding: 14px;">
											<p class="H1">全国金融工作会议</p>
												<div class="news-text" style="padding: 14px;">今年以来，中国高层在不同场合多次谈及金融议题。决策层提出“金融活，经济活”，将其摆在经济工作突出位置。此次会议进一步强调，金融是国家重要的核心竞争力，金融安全是国家安全的重要组成部分，金融制度是经济社会发展中重要的基础性制度。</div>
											</div>
											<el-button class="news-btn" type="primary" size="large" style="margin-top:15px">read more</el-button>
										</el-card>
									</el-col>
									<el-col :span="6" :xs="6" :sm="6" :md="6" :lg="6">
										<el-card class="news-card">
											<img src= "../assets/pexels-photo-159888.jpeg">
											<div style="padding: 14px;">
												<p class="H1">全国金融工作会议</p>
												<div class="news-text" style="padding: 14px;">今年以来，中国高层在不同场合多次谈及金融议题。决策层提出“金融活，经济活”，将其摆在经济工作突出位置。此次会议进一步强调，金融是国家重要的核心竞争力，金融安全是国家安全的重要组成部分，金融制度是经济社会发展中重要的基础性制度。</div>
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


		</div>
	</template>

	<script>
		export default{

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
			background-image: url("../assets/background1.png");
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