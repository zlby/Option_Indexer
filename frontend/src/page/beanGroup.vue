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
										<el-date-picker v-model="daypicker" 
											type="date" 
											placeholder="选择日期时间" 
											align="right" 
											:picker-options="pickerOption" 
											format="yyyy-MM-dd">
										</el-date-picker>
									</div>
								</el-col>
								<el-col :span="12">
									<div style="">
										<span style="vertical-align:center; margin-top:8px">
											现货
										</span>
										<el-input placeholder="请输入现货量(吨)" style="width:75%" v-model="currentHold"></el-input>
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
											<el-select v-model="comboFuture.code" class="sel">
												<el-option
												v-for="item in filteredFutures"
												:key="item"
												:label="item"
												:value="item"/>
											</el-select>
										</div>
										<span>期货持仓</span>
										<el-input-number class="inp" v-model="comboFuture.amount" size="small"></el-input-number>
									</div>
									<el-button type="danger" @click="addFuture" style="float: right; margin-right: 20px; "><i class="el-icon-plus"></i></el-button>
								</div>
							</el-col>

							<el-col :span="12">
								<div class="container">
									<div class="wrapper" v-for="comboOption in comboOptions">
										<div class="kind">
										<span>期权品种</span>
											<el-select v-model="comboOption.code" class="sel"> 
												<el-option
												v-for="item in filteredOptions"
												:key="item"
												:label="item"
												:value="item"/>
											</el-select>
										</div>
										<span>期权持仓</span>
										<el-input-number class="inp" v-model="comboOption.amount" size="small"></el-input-number>
										<div class="kind">
										<span style="margin-left:15px">波动率</span>
											<el-input-number v-model="comboOption.volatility" class="sel" size="small" :step="0.05"> 
											</el-input-number>
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
					<div class="graph" id="chart">
					</div>
				</el-col>
			</div>
		</div>
	</template>

	<script>
		import headSecond from '../components/headSecond'
		import footerBottom from '../components/footerBottom'
		import echarts from 'echarts'
		import axios from 'axios'
		import {notifi} from '../notif'
		export default{

			components:{
				headSecond,
			},

			data(){
				return{
					comboFutures:[],
					comboOptions:[],
					currentHold:0,
					daypicker:new Date(),
					pickerOption: {
			          shortcuts: [{
			            text: '今天',
			            onClick(picker) {
			              picker.$emit('pick', new Date());
			            }
			          }]
			        },
				}
			},
			mounted:function(){
				myChart= echarts.init(document.getElementById('main'));
			    template={
			        "optionK":{
			            name: null,
			            type: 'line',
			            step:false,
			            smooth:false,
			            data:null,
			            gridIndex:null,
			        },
			        "optionIV":{
			            name:null,
			            type:"line",
			            data:null,
			            xAxisIndex:1,
			            yAxisIndex:1,
			            tooltip:{
			                trigger:"axis",
			            },
			            itemStyle:{
			                normal:{
			                    color:null,
			                    borderWidth:1
			                }
			            },
			            gridIndex:null,
			        },
			    }
			    option={
			        title:[
			            {
			                text: '损益图',
			                subtext:"",
			                left:"5%",
			                top:"0%"
			            }
			        ],
			        tooltip: {
			            trigger: "axis",
			            axisPointer: {
			                type: "cross"
			            },
			            backgroundColor: 'rgba(245, 245, 245, 0.8)',
			            borderWidth: 1,
			            borderColor: '#ccc',
			            padding: 10,
			            textStyle: {
			                color: '#000'
			            },
			            position: function (pos, params, el, elRect, size) {
			                var obj = {
			                    top: 10,
			                    right:-170
			                };
			                //obj[['left', 'right'][+(pos[0] < size.viewSize[0] / 2)]] = 30;
			                return obj;
			            },
			            extraCssText: 'width: 170px'
			        },
			        toolbox: {
			            feature: {
			                dataZoom: {
			                    yAxisIndex: false
			                }
			            }
			        },
			        axisPointer: {
			            link: {
			                xAxisIndex: 'all',
			            }
			        },
			        legend: [
			            {
			                data:[],
			                bottom: "6%",
			                left: "5%",
			                icon: "roundRect",
			                gridIndex:1,
			            }
			        ],
			        dataZoom: [
			            {
			                type: "inside",
			                start: 0,
			                end: 100,
			                xAxisIndex: [0]
			            },
			            {
			                type: "slider",
			                show: true,
			                start: 0,
			                end: 100,
			                xAxisIndex: [0],
			                bottom: "50%",
			                left:"center"
			            }
			        ],
			        grid: [
			            //
			            {
			                left: '5%',
			                height: '40%',
			                top: "10%",
			                width: "100%"
			            }
			        ],
			        xAxis: [
			            {
			                type: "value",
			                name:"当前豆粕现货价格",			               
			                data: null,
			                scale: true,
			                boundaryGap: true,
			                axisLine: {onZero: false},
			                splitLine: {show: false},
			                splitNumber: 4,
			                min: 'dataMin',
			                max: 'dataMax',
			                axisPointer: {
			                    z: 100
			                }
			            }
			        ],
			        yAxis: [
			            {
			            	name:"资产组合价值",
			                scale: true,
			                gridIndex: 0,
			                splitNumber: 10,
			                axisLabel: {
			                    show: true,
			                },
			                axisLine: {show: true},
			                axisTick: {show: true},
			                splitLine: {show: true},
			                axisPointer: {
			                    label: {
			                        formatter: function (params) {
			                            return params.value
			                        }
			                    }
			                }
			            }
			        ],
			        animationThreshold: 1000,
			        animationDelay: function (idx) {
			            return idx * 10;
			        },
			        animation:true,
			        series: []
			    };
			},
			methods:{
								futures: function(){
					return this.$store.state.login.futureBalance;
				},
				options:function(){
					return this.$store.state.login.optionBalance;
				},
				futureTimetable:function(){
					return this.$store.state.login.futureBalanceTime
				},
				filteredFutures:function () {
					var vm = this
					return vm.futures.filter(function (item) {
						var chosenTime=new Date(vm.daypicker).getTime();
						return (futureTimetabel[item]>=chosenTime);
					})
				},
				filteredOptions:function () {
					var vm = this
					return vm.options.filter(function (item) {
						var chosenTime=new Date(vm.daypicker).getTime();
						var futureCode=item.slice(0,5);
						return (futureTimetable[futureCode]>=chosenTime);
					})
				},

				addFuture: function() {
					this.comboFutures.push({'code': null, 'amount': 0})
				},
				addOption: function() {
					this.comboOptions.push({'code': null, 'volatility':0, 'amount': 0})
				},
				confirmCombo:function(){
					var params={
						physicals:this.currentHold,
						future_list:this.comboFutures,
						option_list:this.comboOptions,
						t1:this.daypicker
					}
					var saveThis=this
					axios.get('/market/asset-evaluation/',params).then(function(res){
						res=res.data;
						if(res.status.code===0){
							saveThis.popOption("资产组合")
							saveThis.addChartOption({name:"资产组合",data:res.data})
							saveThis.comboFutures=[];
							saveThis.comboOptions=[];
						}else{
							saveThis.$notify({
								type:"danger",
								title:"错误",
								message:"似乎出了一些问题"
							})
						}
					})
				},
				createSeries:function(data){
				    var series = this.deepClone(this.template.optionK);
				    series.name = data.name;
				    series.data = data.data;
				    series.xAxisIndex=0;
				    series.yAxisIndex=0;
				    return {
				    	name:data.name,
				        series:series
				    }
				},
				createRandomSeries:function (data){
				    var data=this.randomDataGenK();
				    data.name = "M"+(Math.random()*1000+1000).toFixed(0);
				    var series = this.deepClone(this.template.optionK);
				    series.name = data.name;
				    series.data = data.data;
				    series.xAxisIndex=0;
				    series.yAxisIndex=0;
				    return {
				        name:data.name,
				        series:series
				    }
				},
				//自定义的操作
				getSeriesIndex:function(seriesName) {
					for(var i=0;i<this.option.series.length;i++){
						var series=this.option.series[i];
						var index=series.name.indexOf(seriesName)
						if(index!=-1){
							return index
						}
					}
				},
				popSeries:function(seriesName){
					for(var i=0;i<this.option.series.length;i++){
						var series=this.option.series[i];
						if(series.name.indexOf(seriesName)!=-1){
							this.option.series.splice(i,1);
							i--;
						}
					}
				},
				getSelectedName:function(selected){
				    if(!selected){
				        selected=this.option.legend[0].selected;
				    }
				    var selectName=[]
				    for(var name in selected){
				        if(selected[name]){
				            selectName.push(name);
				        }
				    }
				    return selectName
				},
				deepClone:function(obj){
					if(typeof obj==="object") {
						if (Array.isArray(obj)) {
							var newarr = [];
							for (var i = 0; i < obj.length; i++) {
								newarr.push(obj[i]);
							}
							return newarr;
						} else {
							var newobj = {};
							for (var key in obj) {
								newobj[key] = this.deepClone(obj[key]);
							}
							return newobj
						}
					}else{
						return obj
					}
				},
				popOption: function(optionName){
				    this.popSeries(optionName);
				    this.myChart.setOption(this.option,true);
				},
				addChartOption:function(data){
				    var series=data.series;
				    this.option.series.push(series);
				    this.myChart.setOption(this.option,true);
				},
				randomDataGenK:function(){
				    var curX=Math.floor(Math.random()*1000);
				    var curY=Math.floor(Math.random()*1000);
				    var data=[]
				    for(var i=0;i<1000;i++){
				        var nowX=curX+i*10;
				        var nowY=this.easingfunction(i/1000)*1000
				        curY=nowY;
				        data.push([nowX,nowY]);
				    }
				    return {
				        name:"M"+(Math.random()*1000+1000).toFixed(0),
				        data:data
				    }
				},
				easingfunction:function (k){
				    if ((k *= 2) < 1) { return 0.5 * k * k * k; }
				    return 0.5 * ((k -= 2) * k * k + 2);
				},
				randomGenWebSafeColor:function(){
				    var base=["00","33","66","99","cc","ff"];
				    var color="#"
				    for(var i=0;i<3;i++){
				        color+=base[Math.floor(Math.random()*6)];
				    }
				    return color;
				}
			}
		}

	</script>

	<style lang="less">
		@import '../style/common';
	
		.hidden{
			display:none;
		}

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