<template>
	<div class = "footer">

		<div class="footer-wraper">
			<div class="follow">关注我们</div>
			<div class="follow-btn-group">
				<img src="../assets/weixin.png" class="follow-btn">
				<img src="../assets/wechat.png" class="follow-btn">
			</div>
			<div class="copyright">Copyright © 2017-2047 OPTIONINDEXER.COM All Rights Reserved</div>
		</div>
		


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

<style>

.footer{
	background-image: url("../assets/map.png");
	background-color: #5c5766;
	background-position:600px 0%;
	background-repeat: no-repeat;
	background-image-opacity:0;
	height:500px;
}

.footer-wraper{
	position: relative;
	top:30%;
}


.follow{
	min-width:300px;
	width:100%;
	margin:auto;	
	font-size: 40px;
	text-align: center;
	padding-bottom: 40px;
	color: white;
}
.follow-btn{
	width:64px;
	margin:0px 10px;
}
.follow-btn-group{
	width:200px;
	margin:auto;
	text-align: center;
	padding-bottom: 40px;
}
.copyright{
	color:white;
	border-top:5px solid white;
	font-size:25px;
	width:55%;
	margin:auto;
	text-align: center;
	padding-top: 20px;
}


</style>