<template>
	<div class="homepage">
		<div class="Carousel1">
			<el-carousel>
				<el-carousel-item class="background1">
					<div class="inner">
						<p class="p1">INDEXER</p>
						<br>
						<p class="p2">最前沿的商品期货期权资讯</p>
						<br><br><br><br>
						<el-button class="button1" v-on:click="buttongroup" v-if="loggedin==false">开始使用</el-button>
            <el-button class="button1" v-on:click="home" v-else>个人中心</el-button>
					</div>
					<!-- 					<img src= "../assets/background1.png"> -->
				</el-carousel-item>
				<el-carousel-item class="background2">
					<div class="inner">
						<p class="p1">INDEXER</p>
						<br>
						<p class="p2">最精确的商品期货期权预测</p>
						<br><br>						<br><br>
						<el-button class="button1" v-on:click="buttongroup" v-if="loggedin==false">开始使用</el-button>
            <el-button class="button1" v-on:click="home" v-else>个人中心</el-button>
					</div>
					<!-- 					<img src= "../assets/background1.png"> -->
				</el-carousel-item>
				<el-carousel-item class="background3">
					<div class="inner">
						<p class="p1">INDEXER</p>
						<br>
						<p class="p2">最权威的商品期权交易策略</p>
						<br><br>						<br><br>
						<el-button class="button1" v-on:click="buttongroup" v-if="loggedin==false">开始使用</el-button>
            <el-button class="button1" v-on:click="home" v-else>个人中心</el-button>
					</div>
					<!-- 					<img src= "../assets/background1.png"> -->
				</el-carousel-item>
				<el-carousel-item class="background4">
					<div class="inner">
						<p class="p1">INDEXER</p>
						<br>
						<p class="p2">最准时的商品期权交易提醒</p>
						<br><br>						<br><br>
						<el-button class="button1" v-on:click="buttongroup" v-if="loggedin==false">开始使用</el-button>
            <el-button class="button1" v-on:click="home" v-else>个人中心</el-button>
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
					<el-carousel-item v-for="page in 4" :index1="page">
						<div class="news_container">
							<el-row :gutter="40">
								<el-col :span="6" :xs="6" :sm="6" :md="6" :lg="6" v-for="news in 4" :index2="news">
									<el-card class="news-card">
										<img :src="imgArr[page-1][news-1]">
										<div style="padding: 14px; height:150px" >
											<p class="H1">{{title[page-1][news-1]}}</p>
											<p class="H1">{{time[page-1][news-1]}}</p>
											<div class="news-text" style="padding: 14px;">{{content[page-1][news-1]}}</div>
										</div>
										<el-button  @click="bj(page, news)" class="news-btn" type="primary" size="large" style="margin-top:10px" >read more</el-button>
									</el-card>
								</el-col>
							</el-row>
						</div>
					</el-carousel-item>
				</el-carousel>

				<el-dialog class="tanchu" title="新闻" size="large" :visible.sync="dialogFormVisible" :modal-append-to-body="true" style="z-index:999;">
						<p class="H1">{{title[index1-1][index2-1]}}</p>
						<p class="H1">{{time[index1-1][index2-1]}}</p>
						<div>{{content[index1-1][index2-1]}}</div>
					<div slot="footer" class="dialog-footer">
						<el-button @click="dialogFormVisible=false">退 出</el-button>
					</div>
				</el-dialog>


			</div>
		</div>
		<footerBottom></footerBottom>
	</div>
</template>

<script>
	import footerBottom from '../componentsCH/footerBottom'
	import api from '../api'
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
				},
				index:1,
				dialogVisible: false,
				dialogFormVisible: false,
				index1: 1,
				index2: 1,
				imgArr:[[require('../assets/pexels-photo-1.jpeg'), require('../assets/pexels-photo-2.jpeg'), require('../assets/pexels-photo-3.jpeg'),require('../assets/pexels-photo-4.jpeg')],
						[require('../assets/pexels-photo-5.jpeg'), require('../assets/pexels-photo-6.jpeg'), require('../assets/pexels-photo-7.jpeg'),require('../assets/pexels-photo-8.jpeg')],
						[require('../assets/pexels-photo-9.jpeg'), require('../assets/pexels-photo-10.jpeg'), require('../assets/pexels-photo-11.jpeg'),require('../assets/pexels-photo-12.jpeg')],
						[require('../assets/pexels-photo-13.jpeg'), require('../assets/pexels-photo-14.jpeg'), require('../assets/pexels-photo-15.jpeg'),require('../assets/pexels-photo-16.jpeg')] ]
			}
		},

		computed: {
			title (){
				return this.$store.state.login.title;
			},
			content (){
				return this.$store.state.login.content;
			},
			time (){
				return this.$store.state.login.time;
			},
			pictures (){
				return ['../assets/pexels-photo-159888.jpeg', '']
			},
      loggedin(){
			    return this.$store.state.login.loggedin;
      }
		},

		mounted:function() {
			for (var i = 1; i < 5; i++) {
				this.$store.dispatch('News',{page_number: i})
			}


		},
		methods:{
			carouselChange:function(index){
				console.log(index)
				index++;
				console.log(index)
			},
			bj:function(page, news){
				this.dialogFormVisible = true;
				this.index1 = page
				this.index2 = news
			},
			buttongroup:function(){
				this.$router.push({ path: '/zh-cn/login' })
			},
      home:function () {
        this.$router.push({ path: '/zh-cn/homepageIndividual/list' })
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

	.background1{
		background-image: url("../assets/background1.jpeg");

	}

		.background2{
		background-image: url("../assets/background2.jpeg");

	}

		.background3{
		background-image: url("../assets/background3.jpeg");

	}

		.background4{
		background-image: url("../assets/background4.jpeg");

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
		font-size: 20px;
	}

	.el-card__body{
		padding: 0px;
	}

	.news_container{
		width: 80%;
		margin: auto;
		height: 400px;
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
