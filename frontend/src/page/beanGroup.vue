<template>
	<div class="homepage fillcontain">
		<head-second></head-second>
		<div class="beangroup">
			<el-col :span="8" :offset="1">
				<div class="input">
					<div class="partOne">
						<el-card style="height:100px;margin-top:20px">
							<el-row :gutter="20">
								<el-col :span="10">
									<div style="margin-top:8px">
										<el-col :span="4" style="vertical-align:center">
										时间
										</el-col>
										<el-col :span="20">
											<el-select v-model="value" placeholder="请选择时间">
												<el-option>123</el-option>
											</el-select>
										</el-col>
									</div>
								</el-col>
								<el-col :span="14">
									<div style="margin-top:8px">
										<el-col :span="4" style="vertical-align:center">
											现货量(吨)
										</el-col>
										<el-col :span="20">
											<el-input placeholder="请输入现货量(吨)"></el-input>
										</el-col>
									</div>
								</el-col>
							</el-row>
						</el-card>
					</div> 
					
					<div class="partTwo">
						<el-row :gutter="20">
							<el-col :span="12">
								<el-card>
									1
								</el-card>
							</el-col>

							<el-col :span="12">
								<el-card>
									2
								</el-card>
							</el-col>
						</el-row>
					</div>

					<div class="partThree">
						<el-button class="el-col el-col-xs-24 el-col-md-24 el-col-sm-24 el-col-lg-24" style="background-color: #FEE090;color: #FEE090;">
						<div style="color: #656565;font-size: 24px">开&nbsp&nbsp&nbsp始</div></el-button>
					</div>
				</div>
			</el-col>
			<el-col :span="15">
				<div class="graph">
				</div>
			</el-col>
		</div>
	</div>
</template>

<script>
	import headSecond from '../components/headSecond'
	import footerBottom from '../components/footerBottom'
	export default{

		components:{
			headSecond
		},

		data(){
			return{
			}
		}
	}

</script>

<style lang="less">
	@import '../style/common';

	.partOne{

	}

	.partTwo{
		margin-top: 20px;
	}

	.partThree{
		margin-top: 20px;
	}

	.el-button{
	}
</style>