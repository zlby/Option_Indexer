<template>
<div class = "homepagesecond">
<el-row>
  <el-col :span="6" v-for="(o, index) in 3" :key="o" :offset="index > 0 ? 3 : 0">
    <el-card>
      <i class="el-icon-delete"></i>
      
    </el-card>
  </el-col>

  <br><br><br><br>

  <div> 
  <el-col :span="12" :offset="2" style="padding-top: 50px">
  	<el-card class="box-card">
  		<div slot="header" class="clearfix">
  			<span style="line-height: 36px;">数据名称</span>
  			<el-button style="float: right;" type="primary" icon="close"></el-button>
  		</div>
  		<div v-for="o in 4" :key="o" class="text item">
  			{{'列表内容 ' + o }}
  		</div>
  	</el-card>
	</el-col>
	<el-col :span="6" :offset="3" style="padding-top: 50px">
  	<el-card class="box-card">
  		<div slot="header" class="clearfix">
  			<span style="line-height: 36px;">对话框</span>
  			<el-button style="float: right;" type="primary" icon="close"></el-button>
  		</div>
  		<div v-for="o in 4" :key="o" class="text item">
  			{{'列表内容 ' + o }}
  		</div>
  	</el-card>
	</el-col>
  </div>

<br><br><br>

 <div> 
  <el-col :span="12" :offset="2" style="padding-top: 50px">
  	<el-card class="box-card">
  		<div slot="header" class="clearfix">
  			<span style="line-height: 36px;">数据名称</span>
  			<el-button style="float: right;" type="primary" icon="close"></el-button>
  		</div>
  		<div v-for="o in 4" :key="o" class="text item">
  			{{'列表内容 ' + o }}
  		</div>
  	</el-card>
	</el-col>
	<el-col :span="6" :offset="3" style="padding-top: 50px">
  	<el-card class="box-card">
  		<div slot="header" class="clearfix">
  			<span style="line-height: 36px;">对话框</span>
  			<el-button style="float: right;" type="primary" icon="close"></el-button>
  		</div>
  		<div v-for="o in 4" :key="o" class="text item">
  			{{'列表内容 ' + o }}
  		</div>
  	</el-card>
	</el-col>
  </div>



</el-row>


</div>



</template>

<script>


	export default {
	}
</script>

<style lang="less">

.homepagesecond{
	background-color: ;
}

</style>