<template>
	<div>
		<head-second></head-second>
		<div style="margin-top:30px">
			<el-row>	

				<el-col :span="10" :offset="1" class="assess">
					<el-row>
					<el-col :span="22" :offset="2" style="margin-top:10px">
						<span>时间&nbsp&nbsp&nbsp</span>
						<el-date-picker v-model="daypicker" 
						type="date" 
						placeholder="选择日期时间" 
						align="right" 
						:picker-options="pickerOption" 
						format="yyyy-MM-dd"
						style="width:50%">
					</el-date-picker>
					</el-col>
					</el-row>
				<el-row>
					<el-col :span="11" :offset="2" style="margin-top:10px">
						<span>现货&nbsp&nbsp&nbsp</span>
						<el-select v-model="value" style="width:73%">
							<el-option
							v-for="item in filteredFutures"
							:key="item.value"
							:label="item.label"
							:value="item.value"/>
						</el-select>
					</el-col>
					<el-col :span="10" :offset="1" style="margin-top:10px">
						<span>持有数量</span>
						<el-input style="width:50%"></el-input>
					</el-col>
				</el-row>

				<el-row style="margin-top:10px">
					<el-col :span="21" :offset="3">
					<el-button class="el-col el-col-xs-22 el-col-md-22 el-col-sm-22 el-col-lg-22" style="background-color: #FEE090;color: #314057;border: 4px solid #F9D481;margin-left:20px">
						<div style="color: #656565;font-size: 24px">套保组合</div>
					</el-button>
					</el-col>
				</el-row>


				<el-row>
					<el-col :span="22" :offset="2">
					<el-col :span="3" style="margin-top:10px">
						<span>期货</span>
					</el-col>
					<el-col :span="21" style="margin-top:10px">
						<el-card style="height:200px; width:95%">
						</el-card>
					</el-col>
					</el-col>
				</el-row>
			


				</el-col>

				<el-col :span="11">
					2
				</el-col>
			</el-row>
		</div>
	</div>
</template>

<script>
	import headSecond from '../components/headSecond'
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
				daypicker: new Date(),
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
		computed:{
			futures: function(){
				return this.$store.state.login.futureBalance;
			},
			options:function(){
				return this.$store.state.login.optionBalance;
			},
			futureTimetable:function(){
				return this.$store.state.login.futureTimetable
			},
			filteredFutures:function () {
				var vm = this
				return this.futures.filter(function (item) {
					var chosenTime=new Date(vm.daypicker).getTime();
					return (vm.futureTimetable[item]>=chosenTime);
				})
			},
			filteredOptions:function () {
				var vm = this
				return this.options.filter(function (item) {
					var chosenTime=new Date(vm.daypicker).getTime();
					var futureCode=item.slice(0,5);
					return (vm.futureTimetable[futureCode]>=chosenTime);
				})
			},
		},
		mounted:function(){
			this.$store.dispatch('getFutureListBalance'),
			this.$store.dispatch('getOptionListBalance')
			this.myChart= echarts.init(document.getElementById('chart'));
			this.template={
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
			this.option={
				title:[
				{
					text: '损益图',
					subtext:"",
					left:"10%",
					top:"4%"
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
							right:100
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
			        	bottom: "10%",
			        	left:"15%"
			        }
			        ],
			        grid: [
			            //
			            {
			            	left: '15%',
			            	height: '60%',
			            	top: "20%",
			            	width: "60%"
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
			        this.myChart.setOption(this.option)
			    },
			    methods:{
			    	addFuture: function() {
			    		this.comboFutures.push({'code': null, 'amount': 0})
			    	},
			    	addOption: function() {
			    		this.comboOptions.push({'code': null, 'volatility':0, 'amount': 0})
			    	},
			    	confirmCombo:function(){
			    		var params={
			    			physicals:this.currentHold,
			    			future_list:JSON.stringify(this.comboFutures),
			    			option_list:JSON.stringify(this.comboOptions),
			    			t1:echarts.format.formatTime("yyyy-MM-dd",this.daypicker),
			    			time_now:"2017-07-12 15:00:00"
			    		};
			    		console.log(params)
			    		var saveThis=this
			    		axios.get('/market/asset_evaluation/',{params:params}).then(function(res){
			    			res=res.data;
			    			if(res.status.code===0){
			    				saveThis.popOption("资产组合")
			    				saveThis.addChartOption(saveThis.createSeries({name:"资产组合",data:res.asset_evaluation_list}))
			    				saveThis.comboFutures=comboFutures;
			    				saveThis.comboOptions=comboFutures;
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
					console.log(this.option.series)
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
				},
			}
		}

	</script>

	<style lang="less">
		@import '../style/common';
		.assess{
			border-radius: 6px;
			border: 3px solid #F9D481;
			background:rgba(0, 0, 0, 0);
			height:600px;
		}
		span{
			font-size: 14px;
		}
	</style>