<template>
	<div>
		<head-second></head-second>
		<div class="beangroup">
			<el-col :span="9" :offset="1">
				<div class="input">
					<div class="partOne" style="margin-top:20px">
						<el-card style="height:60px;padding-top:20px;padding-left:15px">
							<el-row :gutter="20">
								<el-col :span="12">
									<div style="">
										<span style="vertical-align:center; margin-top:8px">
											时间
										</span>
											<el-select v-model="value" placeholder="请选择时间" style="width:75%">
												<el-option>123</el-option>
											</el-select>
									</div>
								</el-col>
								<el-col :span="12">
									<div style="">
										<span style="vertical-align:center; margin-top:8px">
											现货
										</span>
										<el-input placeholder="请输入现货量(吨)" style="width:75%"></el-input>
									</div>
								</el-col>
							</el-row>
						</el-card>
					</div> 
					
					<div class="partTwo">
						<el-row :gutter="20">
							<el-col :span="12">
								<div class="container">
									<div class="wrapper" v-for="comboFuture in comboFutures">
										<div class="kind">
											<span>期货品种</span>
											<el-select v-model="comboFuture.future" class="sel">
												<el-option
												v-for="item in futures"
												:key="item"
												:label="item"
												:value="item"/>
											</el-select>
										</div>

										<span>期货持仓</span>
										<el-input class="inp" v-model="comboFuture.futureHold"/>

									</div>
									<el-button type="danger" @click="addFuture" style="float: right; margin-right: 20px; "><i class="el-icon-plus"></i></el-button>
								</div>
							</el-col>

							<el-col :span="12">
								<div class="container">
									<div class="wrapper" v-for="comboOption in comboOptions">
										<div class="kind">
										<span>期权品种</span>
											<el-select v-model="comboOption.option" class="sel">
												<el-option
												v-for="item in options"
												:key="item"
												:label="item"
												:value="item"/>
											</el-select>
										</div>

										<span>期权持仓</span>
										<el-input class="inp" v-model="comboOption.optionHold"/>

										<div class="kind">
										<span style="margin-left:15px">波动率</span>
											<el-select v-model="comboOption.ratio" class="sel">
												<el-option
												v-for="item in ratios"
												:key="item"
												:label="item"
												:value="item"/>
											</el-select>
										</div>

									</div>
									<el-button type="danger" @click="addOption" style="float: right; margin-right: 20px; "><i class="el-icon-plus"></i></el-button>
								</div>
							</el-col>
						</el-row>
					</div>

					<div class="partThree">
						<el-button class="el-col el-col-xs-24 el-col-md-24 el-col-sm-24 el-col-lg-24" style="background-color: #FEE090;color: #314057;border: 4px solid #F9D481;">
							<div style="color: #656565;font-size: 24px">开&nbsp&nbsp&nbsp始</div></el-button>
						</div>
					</div>
				</el-col>
				<el-col :span="14">
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
				headSecond,
			},

			data(){
				return{
					futures: ['A', 'B', 'C', 'D'],
					comboFutures: [],

					options: ['1','2','3'],
					ratios: ['1','2','3'],
					comboOptions: [],
				}
			},
			methods:{
				addFuture: function() {
					this.comboFutures.push({'future': null, 'futureHold': 0})
				},
				addOption: function() {
					this.comboOptions.push({'option': null, 'ratio': null, 'optionHold': 0})
				}
			}
		}

	</script>

	<style lang="less">
		@import '../style/common';
	

		.el-input{
			border-radius: 6px;
			border: 3px solid #F9D481;
			background:rgba(0, 0, 0, 0)
		}

		.partOne{
			border-radius: 5px;
			border: 2px solid #2C2E3B;
		}


		.partTwo{
			margin-top: 20px;
		}

		.partThree{
			margin-top: 20px;
		}

		.el-button{
		}


		.container {
			padding-top: 10px;
			padding-bottom: 10px;
			padding-left: 12px;
		  width: 100%;
		height: 500px;
		border-radius: 5px;
		border: 2px solid #2C2E3B;
		overflow: auto;
		background-color: #e4e4e4;
	}
	.wrapper {
		 width: 90%;
		padding: 5px;
		border-radius: 5px;
		border: 1px solid #bababd;
		background-color: white;
		margin-bottom: 10px;
	}
	.kind {
		margin-top: 5px;
	}
	.sel {
		margin-left: 18px;
		 width: 50%;
	}
	.inp {
		margin-left: 18px;
		 width: 50%;
		 margin-top: 5px;
	}
</style>