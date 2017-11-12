<template>
	<div>
		<head-second></head-second>
		<div style="margin-top:30px">
			<el-row>

				<el-col :span="10" :offset="1" class="assess">
					<el-row>
						<el-col :span="22" :offset="2" style="margin-top:10px">
							<span>Time&nbsp&nbsp&nbsp</span>
							<el-date-picker v-model="daypicker"
							type="date"
							placeholder="Select time"
							align="right"
							:picker-options="pickerOption"
							format="yyyy-MM-dd"
							style="width:50%">
						</el-date-picker>
					</el-col>
				</el-row>
				<el-row>
					<el-col :span="11" :offset="2" style="margin-top:10px">
						<span>Spot goods&nbsp&nbsp&nbsp</span>
						<el-select v-model="choose_agri" style="width:73%">
							<el-option
							v-for="item in filteredAgris"
							:key="item"
							:label="item"
							:value="item"/>
						</el-select>
					</el-col>
					<el-col :span="10" :offset="1" style="margin-top:10px">
						<el-input v-model="query" placeholder="Search in Crops" style="width:50%"></el-input>
					</el-col>
				</el-row>
				<el-row style="margin-top:10px">
					<el-col :span="22" :offset="2">
						<el-button class="el-col el-col-xs-23 el-col-md-23 el-col-sm-23 el-col-lg-23" style="background-color: #FEE090;color: #314057;border: 4px solid #F9D481;" @click="confirmCombo">
							<div style="color: #656565;font-size: 24px">Hedging Combination</div>
						</el-button>
					</el-col>
				</el-row>
				<el-row>
					<el-col :span="22" :offset="2">
						<el-col :span="24" style="margin-top:10px">
							<el-card style="height:335px; width:95%">
								<div name="staggered-fade" tag="ul" v-bind:css="false" class="list">
								<el-row style="margin-top:10px">
									<el-col :span="6" :offset="1" style="vertical-align:center">
										Future Name
									</el-col>
									<el-col :span="6" :offset="1" style="vertical-align:center">
										Buy/Sell Ratio
									</el-col>
									<el-col :span="6" :offset="1" style="vertical-align:center">
										Correlation Coefficient
									</el-col>
									<el-col :span="3">
										Operation
									</el-col>
								</el-row>
									<el-col :span="24" class="div-divider"></el-col>
									<div v-for="(value,key,index) in optionList" class="item" >
										<el-col :span="6" :offset="1" style="vertical-align:center">
											<el-tag color="#ff4949">{{ optionList[key][0] }}</el-tag>
										</el-col>
										<el-col :span="6" :offset="1" style="vertical-align:center">
											<el-tag color="#ff4949">{{ optionList[key][1].toFixed(6) }}</el-tag>
										</el-col>
										<el-col :span="6" :offset="1" style="vertical-align:center">
											<el-tag color="#ff4949">{{ optionList[key][2].toFixed(6) }}</el-tag>
										</el-col>
										<el-col :span="3">
											<el-button size="mini" type="success"  style="vertical-align:center" :comboid="optionList[key][0]" @click="updateGraph($event)">
												Check
											</el-button>
										</el-col>
										<el-col :span="24" class="div-divider"></el-col>
									</div>
								</div>
							</el-card>
						</el-col>
					</el-col>
				</el-row>

			</el-col>

			<el-col :span="12" :offset="1">
				<el-row>
					<div class="graph" id="assesschart" style="width:95%;height:540px;border: 3px solid #F9D481;border-radius: 6px;">
					</div>
				</el-row>
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
				optionList:[],
				currentHold:0,
				query:"",
				choose_agri:"",
				combo_agri:"",
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
			filteredAgris:function(){
			    var vm = this
				var agris=["Pakchoi"," lettuce"," spinach"," cabbage"," Chinese cabbage"," cole"," Artemisia chinensis"," baby food"," green onion"," carrot"," sweet potato","White radish"," lettuce"," onion"," Lotus Root"," Potato"," Sweet Potato"," Cucumber"," Pumpkin"," bitter gourd"," Wax gourd"," broccoli"," tomato","Towel gourd"," Green Pepper"," Round Eggplant"," Summer Squash"," Eggplant","Pepper","Little Cucumber"," Beans"," Celery"," Cilantro"," Ginger"," Garlic"," Mushroom"," Mushroom"," Leek"," Yellow Bean Sprouts"," Green Bean Sprouts"," Corn"," Cauliflower"," Garlic Moss"," Sacha Sugar Orange"," Pomelo "," Miju "," Lemon "," Red Pomelo "," Small Papaya "," Pearl Melon "," Seedless Watermelon "," Black Beauty Watermelon "," Hami Melon "," Watermelon"," Emperor Banana"," Hainan Banana"," Crown Pear"," Honey Pear"," Pear"," Green Apple"," Imported Snake Fruit"," Gong Pear","  Red Fuji"," Pear"," Yali Pear"," Apple"," Qingtian"," Red Seed"," Red Grape"," Grape"," Narcissus"," Avocado"," Sweet pomegranate "," samara fruit "," imported mangosteen "," Thai durian "," imported kiwi "," black sugar cane "," strawberry "," pineapple "," persimmon "," pomegranate  Ginseng "," dragon fruit "," jujube "," hawthorn "," kiwifruit "," mango "," jujube "," chestnut "," white melon "," papaya "," fresh dates  Green grapes"," kiwifruit"," chives"," citrus"," papaya"," Kyoho grapes"," imported dragon fruit"," dried persimmons"," imported grapefruit"," imported lemons"," Red orange"," red orange"," orange"," kumquat"," grapefruit"," tribute orange"," melon"," white berry melon"," banana"," crystal red fuji"," Coconut Green"," Imported Longan"," Imported Hongmang"," Cherry"," Elizabeth"," Yangmei"," Longan"," Lizao"," Imported Red Li"," Black Brin "," tribute orange "," sweet orange "," apricot "," Sichuan peach "," nectarine ","cherry" ]
				return agris.filter(function(item){
					return (item.indexOf(vm.query) !== -1)||(item.indexOf(vm.query)!==-1)
				})


			}
		},
		mounted:function(){
			this.myChart= echarts.init(document.getElementById('assesschart'));
			this.template={
				"optionPrice":{
					name: null,
					type: 'line',
					step:false,
					smooth:false,
					data:null,
					gridIndex:null,
					itemStyle:{
						normal:{
							color:null
						}
					}
				},
				"optionError":{
					name: null,
					type: 'line',
					step:false,
					smooth:false,
					data:null,
					gridIndex:null,
					itemStyle:{
						normal:{
							color:null
						}
					},
					markLine: {
						symbol: ['none', 'arrow'],
						data: [
						{
							name: 'min line',
							type: 'min',
							label:'Min'
						},
						{
							name: 'max line',
							type: 'max',
							label:'Max'
						},
						{
							name: 'Avg line',
							type: 'average',
							label:'Avg'
						},
						]
					},
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
					text: 'Price Curve of Future & Spot',
					subtext:"",
					left:"7%",
					top:"0%"
				},
				{
					text: 'Error Sequence Curve',
					subtext:"",
					left:"7%",
					top:"50%"
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
			        },
			        toolbox: {
			        	feature: {
			        		dataZoom: {
			        			yAxisIndex: false
			        		}
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
			        	type: "inside",
			        	start: 0,
			        	end: 100,
			        	xAxisIndex: [1]
			        },
			        ],
			        grid: [
			            //
			            {
			            	left: '10%',
			            	height: '36%',
			            	top: "10%",
			            	width: "80%"
			            },
			            {
			            	left: '10%',
			            	height: '36%',
			            	top: "60%",
			            	width: "80%"
			            }
			            ],
			            xAxis: [
			            {
			            	type: "category",
			            	name:"Time",
			            	data: [new Date("2000-01-01 00:00:00")],
			            	scale: true,
			            	boundaryGap: true,
			            	axisLine: {onZero: false},
			            	splitLine: {show: false},
			            	splitNumber: 4,
			            	min: 'dataMin',
			            	max: 'dataMax',
			            	gridIndex:0,
			            	axisPointer: {
			            		z: 100
			            	}
			            },
			            {
			            	type: "category",
			            	name:"Time",
			            	data: null,
			            	scale: true,
			            	boundaryGap: true,
			            	axisLine: {onZero: false},
			            	splitLine: {show: false},
			            	splitNumber: 4,
			            	min: 'dataMin',
			            	max: 'dataMax',
			            	gridIndex:1,
			            	axisPointer: {
			            		z: 100
			            	}
			            }
			            ],
			            yAxis: [
			            {
			            	name:"Price",
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
			            },
			            {
			            	name:"错误率",
			            	scale: true,
			            	gridIndex: 1,
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
			    	updateGraph:function(event){
			    		if(event.target.tagName=="SPAN"){
			    			var comboid=event.target.parentNode.getAttribute("comboid")
			    		}else{
			    			var comboid=event.target.getAttribute("comboid")
			    		}
			    		var agri=this.choose_agri;
			    		if(this.choose_agri!=this.combo_agri){
			    			agri=this.combo_agri;
			    		}
			    		var params={
			    			agri_type:this.choose_agri,
			    			code: comboid
			    		}
			    		var saveThis=this;
			    		axios.get('/market/cross_breed_hedge/',{params:params}).then(function(res){
			    			res=res.data;
			    			if(res.status.code===0){
			    				saveThis.popSeries("期货曲线");
			    				saveThis.popSeries("现货曲线");
			    				saveThis.popSeries("error序列曲线");
			    				saveThis.addChartOption(saveThis.createPriceSeries({name:"期货曲线",data:res.crop_list}))
			    				saveThis.addChartOption(saveThis.createPriceSeries({name:"现货曲线",data:res.future_list}))
			    				saveThis.addChartOption(saveThis.createErrorSeries({name:"error序列曲线",data:res.error_list}))
                  saveThis.myChart.setOption(saveThis.option,true)
                  console.log(saveThis.option.xAxis);
			    			}else{
			    				saveThis.$notify({
			    					type:"danger",
			    					title:"错误",
			    					message:"似乎出了一些问题"
			    				})
			    			}
			    		})
			    	},
			    	confirmCombo:function(){
			    		var params={
			    			agri_type:this.choose_agri,
			    			time_future:echarts.format.formatTime("yyyy-MM-dd",this.daypicker)
			    		};
			    		console.log(params)
			    		var saveThis=this
			    		axios.get('/market/choose_future/',{params:params}).then(function(res){
			    			res=res.data;
			    			if(res.status.code===0){
			    				saveThis.optionList=[];
			    				for(var item in res.future_return){
			    					saveThis.optionList.push(res.future_return[item]);
			    				}
			    				saveThis.combo_agri=saveThis.choose_agri
			    			}else{
			    				saveThis.$notify({
			    					type:"danger",
			    					title:"错误",
			    					message:"似乎出了一些问题"
			    				})
			    			}
			    		})
			    	},
			    	createPriceSeries:function(data){
			    		var series = this.deepClone(this.template.optionPrice);
			    		series.name = data.name;
			    		var processed=data.data.map(function(o){
			    			return [o[0].slice(0,10)+" "+o[0].slice(11,19),o[1]];
			    		});
			    		series.data=processed
			    		series.xAxisIndex=0;
			    		series.yAxisIndex=0;
			    		series.itemStyle.normal.color=this.randomGenWebSafeColor();
			    		var newXAxis=[];
			    		var abre=this.option.xAxis[0].data;
			    		var processedX=processed.map(function(o){
			    			return o[0]
			    		})
			    		if(new Date(abre[0]).getTime()>new Date(processedX[0]).getTime()){
			    			var start=processedX[0];
			    		}
			    		else{
			    			var start=abre[0]
			    		}
			    		if(abre.length==1){
			    			start=processedX[0]
			    		}
			    		if(new Date(abre[abre.length-1]).getTime()>new Date(processedX[processedX.length-1]).getTime()){
			    			var end=abre[abre.length-1]
			    		}
			    		else{
			    			var end=processedX[processedX.length-1]
			    		}
			    		var days=(new Date(end).getTime()-new Date(start).getTime())/86400000;
			    		newXAxis.push(start);
			    		var startMiSec=new Date(start).getTime()
			    		for(var i=1;i<days;i++){
			    			var date=new Date(startMiSec+86400000*i);
			    			newXAxis.push(echarts.format.formatTime("yyyy-MM-dd hh:mm:ss",date))
			    		}
			    		newXAxis.push(end)
			    		this.option.xAxis[0].data=newXAxis;
			    		console.log(newXAxis);
			    		return {
			    			name:data.name,
			    			series:series
			    		}
			    	},
			    	createErrorSeries:function(data){
			    		var series = this.deepClone(this.template.optionError);
			    		series.name = data.name;
			    		var processed=data.data.map(function(o){
			    			return [o[0].slice(0,10)+" "+o[0].slice(11,19),o[1].toFixed(4)];
			    		});
			    		series.data=processed
			    		series.xAxisIndex=1;
			    		series.yAxisIndex=1;
			    		series.itemStyle.normal.color=this.randomGenWebSafeColor();
			    		this.option.xAxis[1].data=processed.map(function(o){
			    		    return o[0]
              })
			    		console.log(series)
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
					//this.myChart.setOption(this.option,true);
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
			height:548px;
		}
		span{
			font-size: 14px;
		}
    .div-divider{
      margin:3px 0px;
    }
	</style>
