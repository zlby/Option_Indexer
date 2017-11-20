<template>
	<div>
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
						<el-select v-model="choose_agri" style="width:73%">
							<el-option
							v-for="item in filteredAgris"
							:key="item"
							:label="item"
							:value="item"/>
						</el-select>
					</el-col>
					<el-col :span="10" :offset="1" style="margin-top:10px">
						<el-input v-model="query" placeholder="在农产品中搜索" style="width:50%"></el-input>
					</el-col>
				</el-row>
				<el-row style="margin-top:10px">
					<el-col :span="22" :offset="2">
						<el-button class="el-col el-col-xs-23 el-col-md-23 el-col-sm-23 el-col-lg-23" style="background-color: #FEE090;color: #314057;border: 4px solid #F9D481;" @click="confirmCombo">
							<div style="color: #656565;font-size: 24px">套保组合</div>
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
										期货名称
									</el-col>
									<el-col :span="6" :offset="1" style="vertical-align:center">
										买入卖出比
									</el-col>
									<el-col :span="6" :offset="1" style="vertical-align:center">
										相关系数
									</el-col>
									<el-col :span="3">
										操作
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
												查看
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
	import echarts from 'echarts'
	import axios from 'axios'
	import {notifi} from '../notif'
	export default{

		components:{
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
				var agris=["小白菜", "生菜", "菠菜", "大包菜", "大白菜", "油菜", "茼蒿", "娃娃菜", "生葱", "胡萝卜", "番薯", "白萝卜", "莴笋", "洋葱", "藕", "土豆", "红薯", "黄瓜", "南瓜", "苦瓜", "冬瓜", "西兰花", "西红柿", "丝瓜", "青椒", "圆茄", "西葫芦", "茄子", "尖椒", "小黄瓜", "豆角", "芹菜", "香菜", "姜", "蒜苗", "大蒜", "香菇", "蘑菇", "韭菜", "黄豆芽", "绿豆芽", "玉米", "菜花", "蒜苔", "沙糖桔", "脐橙", "蜜柚", "蜜桔", "柠檬", "红柚", "小木瓜", "珍珠瓜", "无籽西瓜", "黑美人西瓜", "哈密瓜", "黄河蜜瓜", "西瓜", "皇帝香蕉", "海南香蕉", "皇冠梨", "蜜梨", "香梨", "青苹果", "进口蛇果", "贡梨", "花牛", "红富士", "梨", "鸭梨", "苹果", "国产青提", "无籽红提", "红提", "葡萄", "水仙芒果", "牛油果", "甜石榴", "圣女果", "进口山竹", "泰国榴莲", "进口奇异果", "黑甘蔗", "草莓", "菠萝", "柿子", "石榴", "人参果", "火龙果", "青枣", "山楂", "猕猴桃", "芒果", "枣", "板栗", "白香瓜", "木瓜", "鲜枣", "进口青提子", "金奇异果", "韭黄", "芦柑", "进口木瓜", "巨峰葡萄", "进口火龙果", "柿饼", "进口西柚", "进口柠檬", "红桔", "红江橙", "澳橙", "金桔", "胡柚", "贡桔", "甜瓜", "白兰瓜", "香蕉", "水晶红富士", "椰青", "进口龙眼", "进口红芒", "樱桃", "伊丽莎白", "杨梅", "桂圆", "梨枣", "杨桃", "进口红李", "黑布林", "贡柑", "甜橙", "杏", "四川水蜜桃","油桃","红樱桃"];
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
					text: '期货与现货价格曲线',
					subtext:"",
					left:"7%",
					top:"0%"
				},
				{
					text: 'Error序列图',
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
			            	name:"时间",
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
			            	name:"时间",
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
			            	name:"期货价格",
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
			            	name:"现货价格",
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
			    		if(data.name=="期货曲线"){
			    			series.yAxisIndex=0;
			    		}else{
			    			series.yAxisIndex=1;
			    		}
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
			    		if(data.data===null){
			    			this.$notify({
			    				type:"danger",
			    				title:"错误",
			    				message:"该跨品种套期保值无错误序列"
			    			})
			    			data.data=[];
			    		}
			    		var processed=data.data.map(function(o){
			    			return [o[0].slice(0,10)+" "+o[0].slice(11,19),o[1].toFixed(4)];
			    		});
			    		series.data=processed
			    		series.xAxisIndex=1;
			    		series.yAxisIndex=2;
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
