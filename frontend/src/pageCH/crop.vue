<template>
	<div>
		<div class="beangroup">
			<el-col :span="9" :offset="1" style="height: 100%;">
				<div class="input">
					<div class="partOne" style="margin-top:20px">
						<el-card style="height:60px;padding-top:15px">
							<el-row :gutter="20">
								<el-col :span="14">
									<div style="">
										<span style="vertical-align:center; margin-top:8px;">
											时间
										</span>
										<el-date-picker v-model="daypicker"
										type="date"
										placeholder="选择日期时间"
										align="right"
										:picker-options="pickerOption"
										format="yyyy-MM-dd"
										style="width:80%">
									</el-date-picker>
								</div>
							</el-col>
							<el-col :span="10">
								<div style="">
									<span style="vertical-align:center; margin-top:8px">
										现货
									</span>
									<el-input placeholder="请输入现货量(吨)" style="width:70%" v-model="currentHold"></el-input>
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
										<div>期货品种</div>
										<el-select v-model="comboFuture.code" class="sel">
											<el-option
											v-for="item in filteredFutures"
											:key="item"
											:label="item"
											:value="item"/>
										</el-select>
									</div>
									<div class="kind">
										<div>期货持仓</div>
										<el-input-number controls="false" class="inp" v-model="comboFuture.amount" size="small"></el-input-number>
									</div>
								</div>
								<el-button type="danger" @click="addFuture" style="float: right; margin-right: 20px; "><i class="el-icon-plus"></i></el-button>
							</div>
						</el-col>

						<el-col :span="12">
							<div class="container">
								<div class="wrapper" v-for="comboOption in comboOptions">
									<div class="kind">
										<div>期权品种</div>
										<el-select v-model="comboOption.code" class="sel">
											<el-option
											v-for="item in filteredOptions"
											:key="item"
											:label="item"
											:value="item"/>
										</el-select>
									</div>
									<div>
										<div>期权持仓</div>
										<el-input-number class="inp" v-model="comboOption.amount" controls="false" size="small"></el-input-number>
									</div>
									<div class="kind">
										<div>波动率</div>
										<el-input-number v-model="comboOption.volatility" controls="false" class="sel" size="small" :step="0.05">
										</el-input-number>
									</div>
								</div>
								<el-button type="danger" @click="addOption" style="float: right; margin-right: 20px; "><i class="el-icon-plus"></i></el-button>
							</div>
						</el-col>
					</el-row>
				</div>

				<!--<div class="partThree">-->
					<!--<el-button class="el-col el-col-xs-24 el-col-md-24 el-col-sm-24 el-col-lg-24" style="background-color: #FEE090;color: #314057;border: 4px solid #F9D481;" @click="confirmCombo">-->
						<!--<div style="color: #656565;font-size: 24px">开&nbsp&nbsp&nbsp始</div></el-button>-->
					<!--</div>-->
				</div>
			</el-col>

			<el-col :span="14">

				<el-col :span="12">
					<div class="graph" id="cropchart" style="width:100%;height:200px;margin-top:20px；margin-left:20px;">
					</div>
				</el-col>


				<el-col :span="12">

					<el-row style="margin-top:10px">
						<el-col :span="6" style="margin-top:8px;">
							<p>正态分布</p>
						</el-col>
						<el-col :span="6">
							<span>μ&nbsp&nbsp</span>
							<el-input v-model="norm_dist[0]" size="small" style="width:50%"></el-input>
						</el-col>

						<el-col :span="12">
							<span>σ&nbsp&nbsp</span>
							<el-input v-model="norm_dist[1]" size="small" style="width:25%"></el-input>
						</el-col>

					</el-row>

					<el-row style="margin-top:10px">
						<el-col :span="6" style="margin-top:8px">
							<p>三角分布</p>
						</el-col>

						<el-col :span="6">
							<span>a&nbsp&nbsp</span>
							<el-input v-model="tri_dist[0]" size="small" style="width:50%"></el-input>
						</el-col>

						<el-col :span="6">
							<span>b&nbsp&nbsp</span>
							<el-input v-model="tri_dist[2]" size="small" style="width:50%"></el-input>
						</el-col>

						<el-col :span="6">
							<span>c</span>
							<el-input v-model="tri_dist[1]" size="small" style="width:50%"></el-input>
						</el-col>
					</el-row>

					<el-row style="margin-top:10px">
						<el-col :span="6" style="margin-top:8px">
							<p>均匀分布</p>
						</el-col>
						<el-col :span="6">
							<span>u1</span>
							<el-input v-model="uni_dist[0]" size="small" style="width:50%"></el-input>
						</el-col>
						<el-col :span="12">
							<span>u2</span>
							<el-input v-model="uni_dist[1]" size="small" style="width:25%"></el-input>
						</el-col>
					</el-row>
					<el-row>
						<el-col :span="10">
							<div class="partThree">
							<el-button style="background-color: #FEE090;color: #314057;border: 4px solid #F9D481; margin-top：10px" @click="updateGraph">
								<div style="color: #656565;font-size: 18px">使用所选分布预测</div>
							</el-button>
							</div>
						</el-col>
						<el-col :span="10" :offset="4">
							<div class="partThree">
							<el-button style="background-color: #FEE090;color: #314057;border: 4px solid #F9D481; margin-top：10px" @click="updateGraphDL">
								<div style="color: #656565;font-size: 18px">使用深度学习预测</div>
							</el-button>
							</div>
						</el-col>
					</el-row>
				</el-col>

				<el-col :span="22" :offset="2">
						<div class="partThree">
						<el-button style="background-color: #FEE090;color: #314057;border: 4px solid #F9D481;" disabled="true">
						<div style="color: #656565;font-size: 18px">套期保值方式偏好</div>
						</el-button>
					</div>
				</el-col>

				<el-col :span="22" :offset="2">
					<div>
						<el-row style="margin-top:10px">
							<el-col :span="6">
								<span>套期保持成本尽量小</span>
							</el-col>
							<el-col :span="18">
								<el-radio-group v-model="radio2">
								<el-col :span="4" :offset="0">
									<el-radio :label="1">很不重要</el-radio>
								</el-col>
									<el-col :span="1" :offset="4">
									<el-radio :label="2">不重要</el-radio>
									</el-col>
								<el-col :span="1" :offset="4">
									<el-radio :label="3">一般</el-radio>
								</el-col>
								<el-col :span="1" :offset="4">
									<el-radio :label="4">重要</el-radio>
								</el-col>
								<el-col :span="1" :offset="4">
									<el-radio :label="5">非常重要</el-radio>
								</el-col>
								</el-radio-group>
							</el-col>
						</el-row>

						<el-row style="margin-top:10px">
							<el-col :span="6">
								<span>亏损风险尽量小</span>
							</el-col>
							<el-col :span="18">
								<el-radio-group v-model="radio1">
								<el-col :span="4" :offset="0">
									<el-radio :label="1">很不重要</el-radio>
								</el-col>
									<el-col :span="1" :offset="4">
									<el-radio :label="2">不重要</el-radio>
									</el-col>
								<el-col :span="1" :offset="4">
									<el-radio :label="3">一般</el-radio>
								</el-col>
								<el-col :span="1" :offset="4">
									<el-radio :label="4">重要</el-radio>
								</el-col>
								<el-col :span="1" :offset="4">
									<el-radio :label="5">非常重要</el-radio>
								</el-col>
								</el-radio-group>
							</el-col>
						</el-row>

						<el-row style="margin-top:10px">
							<el-col :span="6" style="margin-top:8px">
								<span>套期保值成本上限</span>
							</el-col>
							<el-col :span="18">
								<el-input-number controls="false" v-model="max_cost" style="width:30%;"></el-input-number>
							</el-col>
						</el-row>

						<el-row style="margin-top:10px">
							<el-col :span="6" style="margin-top:8px">
								<span>豆粕期货单边持仓上限</span>
							</el-col>
							<el-col :span="18">
								<el-input-number controls="false" v-model="fmax" style="width:30%"></el-input-number>
							</el-col>
						</el-row>

						<el-row style="margin-top:10px">
							<el-col :span="6" style="margin-top:8px">
								<span>豆粕期权单边持仓上限</span>
							</el-col>
							<el-col :span="18">
								<el-input-number controls="false" v-model="omax" style="width:30%"></el-input-number>
							</el-col>
						</el-row>

					</div>
				</el-col>

				<el-col :span="24">
					<div class="partThree">
						<el-button class="el-col el-col-xs-12 el-col-md-12 el-col-sm-12 el-col-lg-12" @click="confirmCombo" style="background-color: #FEE090;color: #314057;border: 4px solid #F9D481; margin-left:250px">
							<div style="color: #656565;font-size: 20px">生成套期保值最优决策</div></el-button>
					</div>
				</el-col>
			</el-col>
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
				comboFutures:[],
				comboOptions:[],
				currentHold:0,
				radio2: 5,
				radio1: 5,
				usePredict:false,
				max_cost:0,
				fmax:0,
				omax:0,
				tri_dist:['','',''],
				norm_dist:['',''],
				uni_dist:['',''	],
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
			this.myChart= echarts.init(document.getElementById('cropchart'));
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
					text: '概率密度函数',
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
			            	name:"",
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
			            	name:"",
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
			    	sendDispReq:function(params){
			    		var saveThis=this
			    		var dis_name=" "
			    		if(params.type=="triangle"){
			    			dis_name="三角分布"
			    		}
			    		if(params.type=="normal"){
			    			dis_name="正态分布"
			    		}
			    		if(params.type=="uniform"){
			    			dis_name="均匀分布"
			    		}
			    		axios.get('market/distributions',{params:params}).then(function(res){
			    			res=res.data;
			    			if(res.status.code===0){
			    				this.usePredict=false;
			    				saveThis.addChartOption(saveThis.createSeries({name:dis_name,data:res.distribution}))
			    				saveThis.$notify({
			    					type:"success",
			    					title:"成功",
			    					message:"将使用"+dis_name+"为您预测"
			    				})
			    			}
			    			else{
			    				saveThis.$notify({
			    					type:"danger",
			    					title:"错误",
			    					message:"似乎出了一些问题"
			    				})
			    			}
			    		})
			    	},
			    	updateGraph:function(){
			    		var full=[this.checkFull(this.tri_dist),this.checkFull(this.norm_dist),this.checkFull(this.uni_dist)];
			    		console.log(full,this.checkFull(this.norm_dist),this.checkFull(this.norm_dist))
			    		if(full[0]){
			    			this.sendDispReq({
			    				type:"triangle",
			    				argv:JSON.stringify(this.tri_dist)
			    			})
			    		}
			    		if(full[1]){
			    			this.sendDispReq({
			    				type:"normal",
			    				argv:JSON.stringify(this.norm_dist)
			    			})
			    		}
			    		if(full[2]){
			    			this.sendDispReq({
			    				type:"uniform",
			    				argv:JSON.stringify(this.uni_dist)
			    			})
			    		}
			    		this.popSeries("三角分布")
			    		this.popSeries("正态分布")
			    		this.popSeries("均匀分布")
			    		this.popSeries("深度学习分布")
			    	},
			    	updateGraphDL:function(){
			    		var params={
			    			type:"predict",
			    			time_future:echarts.format.formatTime("yyyy-MM-dd",this.daypicker),
                argv:JSON.stringify([echarts.format.formatTime("yyyy-MM-dd",this.daypicker)])
			    		}
			    		var dis_name="深度学习分布"
              var saveThis=this
			    		axios.get('market/distributions',{params:params}).then(function(res){
			    			res=res.data;
			    			if(res.status.code===0){
			    				this.usePredict=true;
			    				saveThis.popSeries("三角分布")
			    				saveThis.popSeries("正态分布")
			    				saveThis.popSeries("均匀分布")
			    				saveThis.popSeries("深度学习分布")
			    				saveThis.addChartOption(saveThis.createSeries({name:"深度学习分布",data:res.distribution}))
			    				saveThis.$notify({
			    					type:"success",
			    					title:"成功",
			    					message:"将使用深度学习为您预测"
			    				})
			    			}
			    			else{
			    				saveThis.$notify({
			    					type:"danger",
			    					title:"错误",
			    					message:"似乎出了一些问题"
			    				})
			    			}
			    		})

			    	},
			    	checkNull:function(array){
			    		var isNull=true;
			    		for(var i=0;i<array.length;i++){
			    			if(array[i]!=""){
			    			    isNull=false;
			    			}else{

			    			}
			    		}
			    		return isNull;
			    	},
			    	checkFull:function(array){
			    		var isFull=true;
			    		for(var i=0;i<array.length;i++){
			    			if(array[i]==""){
			    			    isFull=false;
			    			}else{

			    			}
			    		}
			    		return isFull;
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
			    			future_list:JSON.stringify(this.comboFutures),
			    			option_list:JSON.stringify(this.comboOptions),
			    			time_future:echarts.format.formatTime("yyyy-MM-dd",this.daypicker),
			    			w1:this.radio1,
			    			w2:this.radio2,
			    			max_cost:this.max_cost,
			    			fmax:this.fmax,
			    			omax:this.omax,
			    			dist:{
			    				type:"",
			    				argv:[]
			    			}
			    		};
			    		var onedistMessage={
			    			type:"danger",
			    			title:"注意",
			    			message:"一次显示只能选择一种分布，请删除别的分布的参数"
			    		}
			    		if(this.usePredict==true){
			    			params.dist.type="predict"
			    			params.argv=JSON.stringify([echarts.format.formatTime("yyyy-MM-dd",this.daypicker)])
			    		}
			    		else if(!this.checkNull(this.tri_dist)&&this.checkFull(this.tri_dist)){
			    			if(this.checkNull(this.norm_dist)||this.checkNull(this.uni_dist)){
			    				params.dist.type="triangle";
			    				params.dist.argv=this.tri_dist;
			    			}
			    			else{
			    				this.$notify(onedistMessage)
			    			}
			    		}
			    		else if(!this.checkNull(this.norm_dist)&&this.checkFull(this.norm_dist)){
			    			if(this.checkNull(this.tri_dist)||this.checkNull(this.uni_dist)){
			    				params.dist.type="normal";
			    				params.dist.argv=this.norm_dist;
			    			}
			    			else{
			    				this.$notify(onedistMessage)
			    			}

			    		}
			    		else if(!this.checkNull(this.uni_dist)&&this.checkFull(this.uni_dist)){
			    			if(this.checkNull(this.tri_dist)||this.checkNull(this.norm_dist)){
			    				params.dist.type="uniform";
			    				params.dist.argv=this.uni_dist;
			    			}
			    			else{
			    				this.$notify(onedistMessage)
			    			}
			    		}else{
			    			this.$notify({
			    				type:"danger",
			    				title:"注意",
			    				message:"需要完整填写任意一种分布的全部参数"
			    			})
			    			return ;
			    		}
			    		if(typeof(params.max_cost)!="number"){
			    			params.max_cost=null;
			    		}
			    		if(typeof(params.fmax)!="number"){
			    			params.fmax=null;
			    		}
			    		if(typeof(params.omax)!="number"){
			    			params.omax=null;
			    		}

			    		var saveThis=this
              saveThis.$notify({
			    					type:"success",
			    					title:"成功",
			    					message:"我们的服务器正在为您计算套保策略，这可能会需要几分钟，我们会将结果发送至您的邮箱中"
			    				})
			    		axios.get('/market/hedging/',{params:params}).then(function(res){
			    			res=res.data;
			    			if(res.status.code===0){

			    			}
			    			else if(res.status.code===-6){
			    				saveThis.$notify({
			    					type:"danger",
			    					title:"错误",
			    					message:"您的参数似乎输入的不够"
			    				})
			    			}
			    			else{
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
		span{
			font-size:14px;
		}
		p{
			font-size:14px;
		}

		.container {
			padding-top: 10px;
			padding-bottom: 10px;
			padding-left: 12px;
			padding-right:10px;
			width: 95%;
			height: 415px;
			border-radius: 5px;
			border: 2px solid #2C2E3B;
			overflow: auto;

		}
		.wrapper {
			width: 90%;
			padding: 5px;
			border-radius: 5px;
			border: 1px solid #bababd;
			background-color: white;
			margin-bottom: 10px;
			background-color: #e4e4e4;
		}
		.kind {
			margin-top: 7px;
		}
		.inp ,.sel{
			width: 90%;
			margin-top: 5px;
			max-width:250px;
			min-width:130px;
		}
	</style>
