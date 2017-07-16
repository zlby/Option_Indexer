<template>
	<div class="homepage">
		<div class="Carousel">
			<el-carousel height="730px">
				<el-carousel-item>
					<div class="inner">
						<p class="p1">介绍文字</p>
						<br>
						<p class="p2">英文说明</p>
						<br><br><br><br>
						<el-button class="button1">learn more</el-button>
					</div>
					<img src= "../assets/pexels-photo-374018.jpeg">
				</el-carousel-item>
				<el-carousel-item>
					<div class="inner">
						<p class="p1">介绍文字</p>
						<br>
						<p class="p2">英文说明</p>
						<br><br>						<br><br>
						<el-button class="button1">learn more</el-button>
					</div>
					<img src= "../assets/pexels-photo-374018.jpeg">
				</el-carousel-item>
				<el-carousel-item>
					<div class="inner">
						<p class="p1">介绍文字</p>
						<br>
						<p class="p2">英文说明</p>
						<br><br>						<br><br>
						<el-button class="button1">learn more</el-button>
					</div>
					<img src= "../assets/pexels-photo-374018.jpeg">
				</el-carousel-item>
				<el-carousel-item>
					<div class="inner">
						<p class="p1">介绍文字</p>
						<br>
						<p class="p2">英文说明</p>
						<br><br>						<br><br>
						<el-button class="button1">learn more</el-button>
					</div>
					<img src= "../assets/pexels-photo-374018.jpeg">
				</el-carousel-item>

			</el-carousel>
		</div>




		<div class="news">
			<el-row>
				<p class="p1">新闻资讯</p>
				<br><br>
				<p class="p2">英文说明</p>

				<el-carousel :interval="4000" type="card" height="625px">
					<el-carousel-item>
						<el-card :body-style="{ padding: '0px' }">
							<img src= "../assets/first4.jpg">
							<div style="padding: 14px;">
								<span>好吃的汉堡</span>
								<p>我特意起了个大早，为的就是看看早晨的天空。我一抬头，星空毫无遮拦的出现在我面前了。璀璨耀眼的小星星眨着亮晶晶的大眼睛，像一颗颗闪着荧光的小水滴。中间有一轮皎洁的明月。万点繁星衬托着月亮 ，而月亮像一个披着荧光衣服的小姑娘惬意地望着小星星。</p>
								<el-button type="primary" size="large">read more</el-button>
							</div>
						</el-card>
					</el-carousel-item>
					<el-carousel-item>
						<el-card :body-style="{ padding: '0px' }">
							<img src= "../assets/first4.jpg">
							<div style="padding: 14px;">
								<span>好吃的汉堡</span>
								<p>我特意起了个大早，为的就是看看早晨的天空。我一抬头，星空毫无遮拦的出现在我面前了。璀璨耀眼的小星星眨着亮晶晶的大眼睛，像一颗颗闪着荧光的小水滴。中间有一轮皎洁的明月。万点繁星衬托着月亮 ，而月亮像一个披着荧光衣服的小姑娘惬意地望着小星星。</p>
								<el-button type="primary" size="large">read more</el-button>
							</div>
						</el-card>
					</el-carousel-item>
					<el-carousel-item>
						<el-card :body-style="{ padding: '0px' }">
							<img src= "../assets/first4.jpg">
							<div style="padding: 14px;">
								<span>好吃的汉堡</span>
								<p>我特意起了个大早，为的就是看看早晨的天空。我一抬头，星空毫无遮拦的出现在我面前了。璀璨耀眼的小星星眨着亮晶晶的大眼睛，像一颗颗闪着荧光的小水滴。中间有一轮皎洁的明月。万点繁星衬托着月亮 ，而月亮像一个披着荧光衣服的小姑娘惬意地望着小星星。</p>
								<el-button type="primary" size="large">read more</el-button>
							</div>
						</el-card>
					</el-carousel-item>
					<el-carousel-item>
						<el-card :body-style="{ padding: '0px' }">
							<img src= "../assets/first4.jpg">
							<div style="padding: 14px;">
								<span>好吃的汉堡</span>
								<p>我特意起了个大早，为的就是看看早晨的天空。我一抬头，星空毫无遮拦的出现在我面前了。璀璨耀眼的小星星眨着亮晶晶的大眼睛，像一颗颗闪着荧光的小水滴。中间有一轮皎洁的明月。万点繁星衬托着月亮 ，而月亮像一个披着荧光衣服的小姑娘惬意地望着小星星。</p>
								<el-button type="primary" size="large">read more</el-button>
							</div>
						</el-card>
					</el-carousel-item>
				</el-carousel>

			</el-row>
		</div>
		

		<div class="news1">
			<el-row>
				<el-col :span="24">
					<el-card>
						<img src="../assets/first4.jpg" class="pic1">
						<p><h1>星期五早晨</h1>我特意起了个大早，为的就是看看早晨的天空。我一抬头，星空毫无遮拦的出现在我面前了。璀璨耀眼的小星星眨着亮晶晶的大眼睛，像一颗颗闪着荧光的小水滴。中间有一轮皎洁的明月。万点繁星衬托着月亮 ，而月亮像一个披着荧光衣服的小姑娘惬意地望着小星星。 一颗流星在蓝幽幽的天空中划过一道神奇的弧线，像织女抛出的梭子，转瞬即逝。星空真蓝啊，蓝的发黑，蓝的发黑，蓝的清澈，蓝的纯洁，像磨的一常光滑的蓝宝石。一丝丝凉风刮过，呼呼的直往人怀里钻，让人感觉既凉爽 ，又惬意 。星星，还眨着眼睛。月亮，还是那么皎洁。早晨的天空，依然是那么美。
						</p>
					</el-card>
				</el-col>
			</el-row>
		</div>

		<div class="news2">
			<el-row>
				<el-col :span="24">
					<el-card>
						<img src="../assets/first4.jpg" class="pic2">
						<p><h1>星期五早晨</h1>我特意起了个大早，为的就是看看早晨的天空。我一抬头，星空毫无遮拦的出现在我面前了。璀璨耀眼的小星星眨着亮晶晶的大眼睛，像一颗颗闪着荧光的小水滴。中间有一轮皎洁的明月。万点繁星衬托着月亮 ，而月亮像一个披着荧光衣服的小姑娘惬意地望着小星星。 一颗流星在蓝幽幽的天空中划过一道神奇的弧线，像织女抛出的梭子，转瞬即逝。星空真蓝啊，蓝的发黑，蓝的发黑，蓝的清澈，蓝的纯洁，像磨的一常光滑的蓝宝石。一丝丝凉风刮过，呼呼的直往人怀里钻，让人感觉既凉爽 ，又惬意 。星星，还眨着眼睛。月亮，还是那么皎洁。早晨的天空，依然是那么美。
						</p>
					</el-card>
				</el-col>
			</el-row>
		</div>
		
		<div class="about">
			<p class="p1">关于我们</p>
			<br>
			<p class="p2">英文说明</p>
			<br><br><br><br>
		</div>
		
		<div class="promotion">
			<br>
			<p class="p2">你们的宣传语blabla</p>
			<br><br><br><br><br><br><br><br><br><br><br>
			<p class="p2">宣传语blabla</p>
			<br><br><br><br>
			<p class="p2">@官方微博</p>
			<br><br><br><br><br>
		</div>


	<div class="contact">
		<p class="p1">联系我们</p>
		<br><br><br><br><br><br><br>
		<el-form ref="form" :model="form" label-width="80px">
			<el-row  :gutter="20"> 
			<el-col :span="6" :offset="6">
			<el-form-item>
				<el-input v-model="form.name" placeholder = "Your Name"></el-input>
			</el-form-item>
			</el-col>
			<el-col :span="6" >
			<el-form-item>
				<el-input v-model="form.email" placeholder = "Your Email"></el-input>
			</el-form-item>
			</el-col>
			</el-row>
			<el-row>
			<el-col :span="12" :offset="6">
			<el-form-item>
				<el-input type="textarea" v-model="form.desc" placeholder = "Your Message"></el-input>
			</el-form-item>
			</el-col>
			</el-row>
			<el-row :gutter="20">
			<el-col :span="12" :offset="10">
			<el-form-item>
				<el-button type="primary" size="large" @click="onSubmit">send message</el-button>
			</el-form-item>
			</el-col>
			</el-row>
		</el-form>


	</div>


			<div class="promotion">
			<br>
			<p class="p2">超链接</p>
			<br><br><br><br><br><br><br><br><br><br><br>
			<br><br><br><br>
			<p class="p2">超链接</p>
			<br><br><br><br><br>
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
}

.el-carousel-item{
	background-image: url("../assets/1.jpg");
}


  .el-carousel__item h3 {
    color: #475669;
    font-size: 14px;
    opacity: 0.75;
    line-height: 200px;
    margin: 0;
  }
  
  .el-carousel__item:nth-child(2n) {
    background-color: #99a9bf;
  }
  
  .el-carousel__item:nth-child(2n+1) {
    background-color: #d3dce6;
  }


.fillcontain{
      height: 100%;
    width: 100%;
}

.inner{
	text-align: center;
	position: fixed;
	z-index: 4;
	top: 38%;
	left: 43%;
	color:#fff;
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



</style>