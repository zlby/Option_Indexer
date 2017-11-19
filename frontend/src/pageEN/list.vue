<template style="min-width:800px">
    <div>
        <el-col :span="20">
            <div id="list" style="width:100%;height:300px; margin-bottom:20px; margin-top:20px"></div>
        </el-col>
        <el-col :span="20" style="margin-top:30px">
            <div class="el-col el-col-9 el-col-xs-9 el-col-sm-9 el-col-md-9 el-col-lg-9 ">
                <el-date-picker
                  v-model="daypicker"
                  type="daterange"
                  align="right"
                  placeholder="Select date range"
                  :picker-options="pickerOption"
                  style="margin-left:50px; width:60%;">
                </el-date-picker>
            </div>

            <el-col :span="7">
            <el-radio-group v-model="interval">
                <el-radio-button label="day">day</el-radio-button><el-radio-button label="hour">hour</el-radio-button>
            </el-radio-group>
            </el-col>
            <el-col :span="8">
            <el-button type="success" size="large" style="position:relative;bottom:0px;" @click="changeDataFormat">Confirm data display format</el-button>
            </el-col>
        </el-col>
        <el-col :span="20" style="margin-top:30px; margin-left:50px">
            <el-card class="box-card">
              <el-input v-model="query" placeholder="Search combination"></el-input>

              <div name="staggered-fade" tag="ul" v-bind:css="false" class="list">
                    <el-col :span="9" style="vertical-align:center">
                     positive option
                     </el-col>
                  <el-col :span="9">
                     negative option
                  </el-col>
                  <el-col :span="6">
                        operation
                  </el-col>
                  <el-col :span="24" class="div-divider"></el-col>
                  <div v-for="(value,key,index) in computedList" class="item" >

                  <el-col :span="9" style="vertical-align:center">
                     <el-tag color="#ff4949">{{ computedList[key].positive_option }}</el-tag>
                  </el-col>
                  <el-col :span="9">
                     <el-tag color="#13ce66">{{computedList[key].negative_option}}</el-tag>
                  </el-col>
                  <el-col :span="6">
                        <el-button size="mini" type="success"  style="vertical-align:center" @click="updateCombo($event)" :comboid="computedList[key].id">
                            display
                        </el-button>
                        <el-button size="mini" type="danger" style="vertical-align:center" @click="deleteCombo($event)" :comboid="computedList[key].id">
                            delete
                        </el-button>
                  </el-col>
                  <el-col :span="24" class="div-divider"></el-col>
                </div>
              </div>
            </el-card>
        </el-col>
</div>
</template>

<script>
  import echarts from 'echarts'
  import Bus from '../bus'
  import axios from 'axios'
  import radarCharts from '../componentsEN/radarCharts'
  import {notifi} from '../notif'

  export default{
      data(){
        console.log(this.$store.state.login.OptionComboList)
        console.log(this.$store.state.login.comboId)
        return{
            query: '',
            // list:this.$store.state.login.OptionComboList,
            // comboid:this.$store.state.login.comboId,
            interval: 'hour',
            pickerOption: {
              shortcuts: [{
                text: 'Last week',
                onClick(picker) {
                  const end = new Date();
                  const start = new Date();
                  start.setTime(start.getTime() - 3600 * 1000 * 24 * 7);
                  picker.$emit('pick', [start, end]);
                }
              }, {
                text: 'Last month',
                onClick(picker) {
                  const end = new Date();
                  const start = new Date();
                  start.setTime(start.getTime() - 3600 * 1000 * 24 * 30);
                  picker.$emit('pick', [start, end]);
                }
              }, {
                text: 'Last three month',
                onClick(picker) {
                  const end = new Date();
                  const start = new Date();
                  start.setTime(start.getTime() - 3600 * 1000 * 24 * 90);
                  picker.$emit('pick', [start, end]);
                }
              }]
            },
            daypicker: ''
        }
    },
    components:{
        radarCharts
    },

    computed: {
        comboid: function() {
            return this.$store.state.login.comboId
        },
        list: function() {
            return this.$store.state.login.OptionComboList
        },
        computedList: function () {
            var vm = this
            return this.list.filter(function (item) {
                return (item.positive_option.toLowerCase().indexOf(vm.query.toLowerCase()) !== -1)||(item.negative_option.toLowerCase().indexOf(vm.query.toLowerCase())!==-1)
        })
    },

  },

  created:function(){
    Bus.$on('addNewOption', optionObj=>{
        this.removeFuture();
        this.addFuture(optionObj.future)
        this.addOption(optionObj.future, optionObj.option)
    })
    Bus.$on('removeOption', optionObj=>{
        this.popOption(optionObj.option)
    })
},
mounted:function(){
    this.$store.dispatch('getOptionCombo')
    this.future={
    }
    this.combinations=[];
    this.mapData=[];
    this.dataFormat={
            start_time:"2017-06-01 09:00",
            end_time:"2017-07-01 09:00",
            data_type:"hour"
        };
    this.option= {
        title:[
        {
            text: 'Option Data',
            subtext:"No combination displayed",
            left:"5%",
            top:"0%"
        },
        {
            text: 'Option Implied Volatility',
            subtext:"No combination displayed",
            left:"55%",
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
                },
                saveAsImage:{
                    type:"png"
                }
            }
        },
        axisPointer: {
            link: {xAxisIndex: 'all'}
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
            start: 50,
            end: 100,
            xAxisIndex: [0, 1]
        },
        {
            type: "slider",
            show: true,
            start: 50,
            end: 100,
            xAxisIndex: [0, 1],
            bottom:"0px",
            left:"center"
        }
        ],
        grid: [
            //
            {
                left: '5%',
                height: '70%',
                top: "10%",
                width: "40%"
            },
            {
                left: '55%',
                top: '10%',
                height: '70%',
                width: "40%"
            }
            ],
            xAxis: [
            {
                type: "category",
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
            },
            {
                type: 'category',
                gridIndex: 1,
                data: null,
                scale: true,
                boundaryGap: true,
                axisLine: {onZero: false},
                axisTick: {show: true},
                splitLine: {show: false},
                axisLabel: {show: true},
                splitNumber: 4,
                min: 'dataMin',
                max: 'dataMax',
                axisPointer: {
                    label: {

                    }
                }
            }
            ],
            yAxis: [
            {
                scale: true,
                gridIndex:0,
                splitArea: {
                    show: true
                }
            },
            {
                scale: true,
                gridIndex: 1,
                splitNumber: 10,
                axisLabel: {
                    show: true,
                    formatter: function (value) {
                        return (value * 100).toFixed(2) + "%";
                    }
                },
                axisLine: {show: true},
                axisTick: {show: true},
                splitLine: {show: true},
                axisPointer: {
                    label: {
                        formatter: function (params) {
                            return "IV\n" + (params.value * 100).toFixed(2) + "%";
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
    this.template={
        "optionK":{
            name: null,
            type: 'candlestick',
            step:false,
            smooth:false,
            data:null,
            markPoints:{
                label:{
                    formatter:function(param){
                        return param!=null?Math.floor(param.value):"";
                    }
                },
                data:[
                {
                    name: 'highest value',
                    type: 'max',
                    valueDim: 'highest'
                },
                {
                    name: 'lowest value',
                    type: 'min',
                    valueDim: 'lowest'
                },
                {
                    name: 'average value on close',
                    type: 'average',
                    valueDim: 'close'
                }
                ]
            },
            markLine: {
                symbol: ['none', 'arrow'],
                data: [
                {
                    name: 'min line on close',
                    type: 'min',
                    valueDim: 'close'
                },
                {
                    name: 'max line on close',
                    type: 'max',
                    valueDim: 'close'
                }
                ]
            },
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
        "IVD":{
            name:"Implied volatility difference",
            type:"line",
            data:null,
            xAxisIndex:3,
            yAxisIndex:3,
            tooltip:{
                trigger:"axis",
            },
            itemStyle:{
                normal:{
                    color:"#000000",
                    borderWidth:1
                }
            }
        }
    }
    this.optionbackup=this.deepClone(this.option);
    this.myChart=echarts.init(document.getElementById('list'));
    // var dataK=[];
    // for(var i=0;i<20;i++){
    //     dataK.push(splitData());
    // }
        this.myChart.setOption(this.option);
        window.store=this
    /*var saveThis=this;
    // 自定义事件
    this.myChart.on("legendselectchanged",function(params){

        saveThis.option.legend[0].selected=saveThis.myChart.getOption().legend[0].selected;
        if(saveThis.checkSelection(params)==2){
            saveThis.showIVDifference(params.selected);
        }else{
            saveThis.popSeries("隐含波动率之差");
            saveThis.option.title[3].subtext="隐含波动率之差只在\n选中两个期权数据时显示"
        }
        var selectName=saveThis.getSelectedName(params.selected);
        if(selectName.length!=0){
            saveThis.option.title[1].subtext=selectName.join(",");
            saveThis.option.title[2].subtext=selectName.join(",");
        }
        saveThis.myChart.setOption(saveThis.option,true);
    })*/
},

methods: {

//启动函数
//启动函数
// document.getElementById("send").onclick=function() {
//     var data = splitData();
//     data.name = document.getElementById("selection").value;
//     var series = this.deepClone(this.
// template.optionK);
//     series.name = data.name;
//     series.data = data.values;
// //     var IVSeries = this.deepClone(this.
// template.optionIV);
//     IVSeries.data = data.IVData;
//     IVSeries.name = data.name;
//     IVSeries.itemStyle.normal.color = randomGenWebSafeColor();
//     this.option.legend[0].data.push(series.name);
//     var temp = this.option.series.pop();
//     this.option.series.push(IVSeries);
//     this.option.series.push(temp);
//     this.option.series.push(series);
//     this.myChart.setOption(this.option);
//   }

resetChart:function(){
    this.myChart.clear();
    this.combinations=[];
    this.mapData=[];
    this.option=this.deepClone(this.optionbackup);
    this.myChart.setOption(this.option,true);
},

changeDataFormat:function(){
    this.resetChart();
    var startTime=echarts.format.formatTime("yyyy-MM-dd hh:mm",this.daypicker[0]);
    var endTime=echarts.format.formatTime("yyyy-MM-dd hh:mm",this.daypicker[1]);
    if(this.interval=="hour"){
        var dataType="hour";
    }else{
        var dataType="day"
    }
    if(startTime.toUpperCase()=="NAN-NAN-NAN NAN:NAN"||endTime.toUpperCase()=="NAN-NAN-NAN NAN:NAN"){
        this.$notify({
            title: 'Attention',
            message: 'No specific date range was selected , please select one',
            type: 'warning'
        })
        return ;
    }
    var dataType=this.interval;
    this.dataFormat={
        start_time:startTime,
        end_time:endTime,
        data_type:this.interval
    }
    this.$notify({
        title: 'Current data format',
        message: 'Start Time:'+startTime+"End Time:"+endTime+"Time interval:"+dataType,
        type: 'success'
    })
},
addCombination:function(optionName1,optionName2){
    console.log(this.dataFormat)
    var reqparams=this.deepClone(this.dataFormat)
    console.log(reqparams,this.dataFormat)
    reqparams.option_list="[\""+optionName1+"\",\""+optionName2+"\"]";
    var saveThis=this
    if(this.getCombinationIndex(optionName1,optionName2)==-1){
        axios.get('/market/options/treading_data/',{params:reqparams}).then(function(res){
        res=res.data;
        if(res.status.code===0){
            saveThis.combinations.push(saveThis.splitAppendCombination(res,[optionName1,optionName2]));
            saveThis.mapData.push([optionName1,optionName2]);
            saveThis.changeDisplayCombination(optionName1,optionName2);
        }else{
            alert('出错')
        }
    })
    }else{
        this.changeDisplayCombination(optionName1,optionName2)
    }
},
changeDisplayCombination:function(optionName1,optionName2){
    var index=this.getCombinationIndex(optionName1,optionName2);
    if(index!==-1){
        this.option.series.push(this.combinations[index][0].series);
        this.option.series.push(this.combinations[index][0].IVSeries);
        this.option.series.push(this.combinations[index][1].series);
        this.option.series.push(this.combinations[index][1].IVSeries);
        this.option.xAxis[0].data=this.combinations[index][0].xAxis;
        this.option.xAxis[1].data=this.combinations[index][0].xAxis;
        this.option.title[0].subtext=optionName1+" and "+optionName2
        this.option.title[1].subtext=optionName1+" and "+optionName2
        this.myChart.setOption(this.option);
    }
},
removeCombination:function(){
    var optionNames=this.option.title[0].subtext.split(" and ")
    this.popSeries(optionNames[0]);
    this.popSeries(optionNames[1]);
    this.myChart.setOption(this.option,true);
},
splitAppendCombination:function(res,optionNames){
    var combine=[];
    var xAxis=[];
    for(var i=0;i<res.data.length;i++){
        var option=res.data[i];
        var optionValues=option.data.map(function(o){
            return [o.open_price,o.close_price,o.max_price,o.min_price]
        });
        var optionXAxis=option.data.map(function(o){
            return o.time
        });
        var optionIVData=option.data.map(function(o){
            return o.volatility.toFixed(4);
        });
        var optionProc=this.createSeries({
            name:option.code,
            values:optionValues,
            IVData:optionIVData,
            categoryData:optionXAxis
        })
        //optionProc.series.data=this.alignTimeAxis(dataK.xAxis,optionProc.xAxis,optionProc.series.data);
        combine.push(optionProc);
    }
    return combine;
},
alignTimeAxis:function(futureXAxis,optionXAxis,optionData){
    var index=futureXAxis.indexOf(optionXAxis[0]);
    if(index==-1){
        return [];
    }
    var fill=["-","-","-","-"];
    var rtn=[]
    var no_datas=[];
    for(var i=0;i<index;i++){
        no_datas.push(fill);
    }
    rtn=no_datas.concat(optionData);
    for(var i=index,j=0;i<futureXAxis.length;i++,j++){
        if(futureXAxis[i]!=optionXAxis[j]){
            rtn.splice(i,0,fill);
        }
    }
    return rtn
},
getCombinationIndex:function(optionName1,optionName2){
    for(var i=0;i<this.mapData.length;i++){
        if((optionName1===this.mapData[i][0]||optionName1===this.mapData[i][1])&&(optionName2===this.mapData[i][1]||optionName2===this.mapData[i][1])){
            return i;
        }
    }
    return -1;
},
createRandomCombination:function(){
    var combinations=[]
    for(var i=0;i<10;i++){
        var optionSet=[]
        var option1=this.createRandomSeries();
        var option2=this.createRandomSeries();
        optionSet.push(option1);
        optionSet.push(option2);
        combinations.push(optionSet);
    }
    return combinations;
},
createSeries:function(data){
    var series = this.deepClone(this.template.optionK);
    series.name = data.name;
    series.data = data.values;
    series.xAxisIndex=0;
    series.yAxisIndex=0;
    if(data.IVData.length!=0){
        var IVSeries = this.deepClone(this.template.optionIV);
        IVSeries.data = data.IVData;
        IVSeries.name = data.name;
        IVSeries.itemStyle.normal.color = this.randomGenWebSafeColor();
        IVSeries.xAxisIndex=1;
        IVSeries.yAxisIndex=1;
    }
    return {
        series:series,
        IVSeries:IVSeries,
        xAxis:data.categoryData
    }
},
createCombinationMap:function(){
    return this.combinations.map(function(o){
        return [o[0].series.name,o[1].series.name];
    })
},
randomGenWebSafeColor:function(){
  var base=["00","33","66","99","cc","ff"];
  var color="#"
  for(var i=0;i<3;i++){
    color+=base[Math.floor(Math.random()*6)];
}
return color;
},
createRandomSeries:function(){
    var data = this.splitData();
    data.name = "M"+(Math.random()*1000+1000).toFixed(0);
    var series = this.deepClone(this.template.optionK);
    series.name = data.name;
    series.data = data.values;
    series.xAxisIndex=0;
    series.yAxisIndex=0;
    var IVSeries = this.deepClone(this.template.optionIV);
    IVSeries.data = data.IVData;
    IVSeries.name = data.name;
    IVSeries.itemStyle.normal.color = this.randomGenWebSafeColor();
    IVSeries.xAxisIndex=1;
    IVSeries.yAxisIndex=1;
    return {
      series:series,
      IVSeries:IVSeries,
      xAxis:data.categoryData
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

checkSelection:function(params){
  var totalSelected=0;
  for(var x in params.selected){
    if(params.selected[x]==true){
      totalSelected++;
  }
}
return totalSelected;
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
//计算期权隐含波动率之差
showIVDifference:function(selected){
  var calcDataSet=[];
  var IVDSeries=this.deepClone(this.
    template.IVD);
  this.option.title[3].subtext=selectName[0]+" and "+selectName[1];
  for(var i=0;i<this.option.series.length;i++){
    var series=this.option.series[i];
    for(var name in selectName){
      if((series.name==selectName[name])&&(series.type=="line")){
        calcDataSet.push(series.data);
    }
}
}
if(calcDataSet.length==2){
    IVDSeries.data=this.calcIVDifference(calcDataSet[0],calcDataSet[1]);
    this.option.series.push(IVDSeries);
}
},
calcIVDifference:function(data1,data2){
  return data1.map(function(value,index) {
    if(data2[index]!=undefined){
      return (value - data2[index]).toFixed(2);
  }else{
      return value;
  }
})
},


//数据处理
splitData:function() {
  var rawData=this.randomDataGenK();
  var categoryData = [];
  var IVData=[];
  var values = [];
  var length=rawData.length;
  for (var i = 1; i < rawData.length; i++) {
    categoryData.push(rawData[i].splice(0, 1)[0]);
    IVData.push(rawData[i].splice(rawData[i].length-1,rawData[i].length)[0]);
    values.push(rawData[i])
}
return {
    name:rawData[0],
    categoryData: categoryData,
    IVData:IVData,
    values: values
};
},
//
//随机数据生成
randomDataGenK:function(){
  var date=echarts.number.parseDate("2017-06-11 09:00:00");
  var data=[];
  data.push("M"+(Math.random()*1000+1000).toFixed(0));
  var beforeClose=parseFloat((Math.random()*1000+1000).toFixed(4));
  var beforeRate=0.2;
  for(var j=1;j<31;j++){
    var total=0
    for(var i=0;i<6;i++){
      var singleData=[];
      singleData.push(echarts.format.formatTime("yyyy-MM-dd hh:mm:ss",date))
      singleData.push(beforeClose.toFixed(1));
      var maximum,minimum
      if(Math.random()<0.5){
        minimum=beforeClose-parseFloat((Math.random()*50))
        beforeClose+=parseFloat((Math.random()*50));
        maximum=beforeClose+parseFloat((Math.random()*50))
    }
    else{
        maximum=beforeClose+parseFloat((Math.random()*50))
        beforeClose-=parseFloat((Math.random()*50));
        minimum=beforeClose-parseFloat((Math.random()*50));
    }
    if(beforeClose<0){
        beforeClose=0.0;
        minimum=0.0;
    }
    singleData.push(beforeClose.toFixed(1));
    singleData.push(maximum.toFixed(1));
    singleData.push(minimum.toFixed(1));
    if(Math.random()<0.5){
        beforeRate-=parseFloat((Math.random()/5));
    }else{
        beforeRate+=parseFloat((Math.random()/5));
    }
    if(beforeRate<0){
        beforeRate=0.0;
    }
    singleData.push(beforeRate.toFixed(2));
    date.setTime(date.getTime()+3600000);
    data.push(singleData)
}
date.setTime(date.getTime()+64800000);
}
return data
},
updateCombo:function(event){
    if(event.target.tagName=="SPAN"){
        var comboid=event.target.parentNode.getAttribute("comboid")
    }else{
        var comboid=event.target.getAttribute("comboid")
    }
    console.log(this.comboid,comboid);
    var index=this.comboid.indexOf(parseInt(comboid));
    console.log(this.list[index],index)
    var pOption=this.list[index].positive_option;
    var nOption=this.list[index].negative_option;
    if(this.option.title[0].subtext!=""){
        this.removeCombination();
    }
    this.addCombination(pOption,nOption);
},
deleteCombo:function(event){
        if(event.target.tagName=="SPAN"){
          var e=event.target.parentNode;
        }else{
          var e=event.target;
        }
        var id=e.getAttribute("comboid");
        var saveThis=this
        axios.put('/client/delete_combo/',{id:id})
        .then(function(res){
            console.log(res);
            if(res.data.status.code=="0"){
                var index=saveThis.comboid.indexOf(parseInt(id));
                console.log(index,saveThis.list,saveThis.comboid)
                // console.log(saveThis.list[index].id,saveThis.comboid[index])
                // saveThis.list.splice(index,1);
                saveThis.$store.commit("deleteCombo", {index: index})
            }else{
               notifi("Delete failed", "Network connection problem", "error", saveThis)
            }
        })
        .catch(function(error){
            console.log(error)
            notifi("Delete failed", "Please check network connection", "error", saveThis)
        })
      }
//期货切换的函数
//清除上一个期货

}
}
</script>



<style lang="less" scoped>
  @import '../style/common';

.list{
    // margin-top: 20px;
    margin-left: 40px;
}
.div-divider{
    margin:5px 0px;
    height:0px;
    background-color: #666
}
  .msg{
  //     height:25px;
  // line-height:25px;
  // overflow:hidden;
  // margin-top: 20px;
  }
  span{

  }

  .item{
    margin-top:10px;
  }
</style>
