<template>
	<div class="homepage">
		<div class="Carousel">
			<el-carousel height="730px">
				<el-carousel-item>
					<div class="inner">
						<p class="p1">INDEXER</p>
						<br>
						<p class="p2">option</p>
						<br><br><br><br>
						<el-button class="button1">learn more</el-button>
					</div>
					<img src= "../assets/pexels-photo-374018.jpg">
				</el-carousel-item>
				<el-carousel-item>
					<div class="inner">
						<p class="p1">INDEXER</p>
						<br>
						<p class="p2">option</p>
						<br><br>						<br><br>
						<el-button class="button1">learn more</el-button>
					</div>
					<img src= "../assets/pexels-photo-306519.jpeg">
				</el-carousel-item>
				<el-carousel-item>
					<div class="inner">
						<p class="p1">INDEXER</p>
						<br>
						<p class="p2">option</p>
						<br><br>						<br><br>
						<el-button class="button1">learn more</el-button>
					</div>
					<img src= "../assets/pexels-photo-373367.jpeg">
				</el-carousel-item>
				<el-carousel-item>
					<div class="inner">
						<p class="p1">INDEXER</p>
						<br>
						<p class="p2">option</p>
						<br><br>						<br><br>
						<el-button class="button1">learn more</el-button>
					</div>
					<img src= "../assets/pexels-photo-439379.jpeg">
				</el-carousel-item>

			</el-carousel>
		</div>




		<div class="news">
			<el-row>
				<p class="p1" style="margin-top:80px">NEWS</p>
				<br><br>
				<p class="p2">option</p>
				<br><br><br>
				<el-carousel :interval="4000" type="card" height="625px">
					<el-carousel-item>
						<el-card :body-style="{ padding: '0px' }">
							<img src= "../assets/pexels-photo-159888.jpeg">
							<div style="padding: 14px;">
								<span>全国金融工作会议传递中国金融发展三大信号</span>
								<p>今年以来，中国高层在不同场合多次谈及金融议题。决策层提出“金融活，经济活”，将其摆在经济工作突出位置。此次会议进一步强调，金融是国家重要的核心竞争力，金融安全是国家安全的重要组成部分，金融制度是经济社会发展中重要的基础性制度。</p>
								<el-button class="newsbtn" type="primary" size="large" style="margin-top:15px">read more</el-button>
							</div>
						</el-card>
					</el-carousel-item>
					<el-carousel-item>
						<el-card :body-style="{ padding: '0px' }">
							<img src= "../assets/pexels-photo-210574.jpeg">
							<div style="padding: 14px;">
								<span>外汇局就《关于金融机构报送银行卡境外交易信息的通知》发布政策问答</span>
								<p>日前，国家外汇管理局发布《关于金融机构报送银行卡境外交易信息的通知》政策问答，就金融机构银行卡境外交易信息报送的时间、金额、数据、方式等相关问题予以解答。</p>
								<el-button class="newsbtn" type="primary" size="large" style="margin-top:15px">read more</el-button>
							</div>
						</el-card>
					</el-carousel-item>
					<el-carousel-item>
						<el-card :body-style="{ padding: '0px' }">
							<img src= "../assets/taxes-tax-evasion-police-handcuffs.jpg">
							<div style="padding: 14px;">
								<span>上半年全国财政收入较快增长 增收结构呈现积极变化</span>
								<p>“上半年，我国经济运行保持在合理区间，稳中向好态势明显。在此基础上，全国财政收入实现较快增长。”财政部国库司巡视员娄洪在7月14日召开的新闻发布会上表示，上半年，一般公共预算收入同比增长9.8%，财政增收结构呈现积极变化，中高端制造业、新兴服务业税收增长平稳较快。</p>
								<el-button class="newsbtn" type="primary" size="large" style="margin-top:15px">read more</el-button>
							</div>
						</el-card>
					</el-carousel-item>
					<el-carousel-item>
						<el-card :body-style="{ padding: '0px' }">
							<img src= "../assets/pexels-photo-286442.jpeg">
							<div style="padding: 14px;">
								<span>监管趋严下银行理财规范发展</span>
								<p>自2004年第一只银行理财产品在我国出现以来，13年间，银行理财业务获得快速发展。数据显示，截至2016年末，银行理财产品余额达到29.05万亿元，同比增长23.63%。不过，近年来，银行理财业务风险也在不断暴露，监管逐步趋严。规范创新发展，成为新时期理财业务的主旋律。</p>
								<el-button class="newsbtn" type="primary" size="large" style="margin-top:15px">read more</el-button>
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
						<img src="../assets/pexels-photo-210574.jpeg" class="pic1">
						<p><h1>监管趋严下银行理财规范发展</h1>自2004年第一只银行理财产品在我国出现以来，13年间，银行理财业务获得快速发展。数据显示，截至2016年末，银行理财产品余额达到29.05万亿元，同比增长23.63%。不过，近年来，银行理财业务风险也在不断暴露，监管逐步趋严。规范创新发展，成为新时期理财业务的主旋律。
						</p>
					</el-card>
				</el-col>
			</el-row>
		</div>

		<div class="news2">
			<el-row>
				<el-col :span="24">
					<el-card>
						<img src="../assets/pexels-photo-286442.jpeg" class="pic2">
						<p><h1>上半年全国财政收入较快增长 增收结构呈现积极变化</h1>“上半年，我国经济运行保持在合理区间，稳中向好态势明显。在此基础上，全国财政收入实现较快增长。”财政部国库司巡视员娄洪在7月14日召开的新闻发布会上表示，上半年，一般公共预算收入同比增长9.8%，财政增收结构呈现积极变化，中高端制造业、新兴服务业税收增长平稳较快。
						</p>
					</el-card>
				</el-col>
			</el-row>
		</div>
		
		<div class="about">
			<p class="p1">About</p>
			<br>
			<p class="p2">option</p>
			<br><br><br><br>
		</div>
		
		<div class="promotion">
			<br>
			<p class="p2">INDEXER</p>
			<br><br><br><br><br><br><br><br><br><br><br>
			<p class="p2">INDEXER</p>
			<br><br><br><br>
			<p class="p2">@官方微博</p>
			<br><br><br><br><br>
		</div>


	<div class="contact">
		<p class="p1">Contact</p>
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
				<el-button type="primary" size="large">send message</el-button>
			</el-form-item>
			</el-col>
			</el-row>
		</el-form>


	</div>


			<div class="promotion">
			<br>
			<p class="p2">super</p>
			<br><br><br><br><br><br><br><br><br><br><br>
			<br><br><br><br>
			<p class="p2">super</p>
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

.newsbtn{
	margin-right: 200px;
	text-align: center;
}

</style>