<template style="min-width:800px">
    <el-row>
        <el-col :span="20" style="margin-top:20px">

            <div class="el-col el-col-9 el-col-xs-9 el-col-sm-9 el-col-md-9 el-col-lg-9 ">
                <el-date-picker
                  v-model="daypicker"
                  type="daterange"
                  align="right"
                  placeholder="Select date range"
                  :picker-options="pickerOption"
                  style="margin-left:50px; width:60%">
                </el-date-picker>
            </div>

            <el-col :span="4">
            <el-radio-group v-model="interval">
                <el-radio-button label="day">day</el-radio-button><el-radio-button label="hour">hour</el-radio-button>
            </el-radio-group>
            </el-col>

            <el-col :span="4">
            <el-button type="success" size="large" style="position:relative;bottom:0px;" @click="changeDataFormat">Confirm data display format</el-button>
            </el-col>
            <el-col :span="4">
            <el-button type="success" size="large" style="position:relative;bottom:0px;margin-left:50px;" @click="putCombination">Add option combination</el-button>
            </el-col>

        </el-col>

                <el-col :span="20" :offset="4">
            <div id="option" style="width:100%;height:600px; margin-top:30px;">
            </div>
        </el-col>
    </el-row>
</template>

<script>
  import echarts from 'echarts'
  import Bus from '../bus'
  import axios from 'axios'

  export default{
    data() {
      return {
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
      };
    },
    created:function(){
        var saveThis=this;
        Bus.$on('addNewOption', optionObj=>{
            saveThis.readyCombinedOption.push(optionObj.option);
            if(this.futureDataGet.indexOf(optionObj.future)===-1){
                axios.get('/market/future/'+optionObj.future+'/treading/',{
            params:saveThis.dataFormat}).then(function(res){
                    res=res.data;
                    if(res.status.code===0){
                        if(saveThis.fewDataOptionSet.indexOf(optionObj.option)!==-1){
                            saveThis.$notify({
                                type:"warning",
                                title:"Attention",
                                message:"Due to the lack of this option's data, it may have poor display effect"
                            })
                        }
                        saveThis.future[optionObj.future]=saveThis.splitAppendData(res);
                        saveThis.removeFuture();
                        saveThis.addFuture(optionObj.future);
                        saveThis.addOption(optionObj.future, optionObj.option);
                        saveThis.futureDataGet.push(optionObj.future);
                        console.log(saveThis.readyCombinedOption.length)
                        if(saveThis.readyCombinedOption.length==2){
                            saveThis.showIVDifference(saveThis.readyCombinedOption);
                            saveThis.myChart.setOption(saveThis.option,true)
                        }else{
                            saveThis.popSeries("Implied volatility difference");
                            saveThis.option.title[3].subtext="Implied volatility difference will be displayed\nwhen you choose only two options"
                            saveThis.myChart.setOption(saveThis.option,true)
                        }
                    }else{
                        alert('出错')
                    }
                })
            }else{
                saveThis.removeFuture();
                saveThis.addFuture(optionObj.future);
                saveThis.addOption(optionObj.future, optionObj.option);
                if(saveThis.readyCombinedOption.length==2){
                    var selected={};
                    saveThis.showIVDifference(saveThis.readyCombinedOption);
                    saveThis.myChart.setOption(saveThis.option,true)
                }else{
                    saveThis.popSeries("Implied volatility difference");
                    saveThis.option.title[3].subtext="Implied volatility difference will be displayed\nwhen you choose only two options"
                    saveThis.myChart.setOption(saveThis.option,true)
                }
            }
        })
        Bus.$on('removeOption', optionObj=>{
            this.popOption(optionObj.option)
            var index=this.readyCombinedOption.indexOf(optionObj.option)
            if(index!=-1){
                this.readyCombinedOption.splice(index,1);
            }
            if(this.readyCombinedOption.length==2){
                var selected={};
                this.showIVDifference(this.readyCombinedOption);
                this.myChart.setOption(this.option,true)
            }
        })
    },
    mounted:function(){
        this.myChart=echarts.init(document.getElementById('option'));
        this.mapData={};
        this.future={
            name:[]
        };
        this.readyCombinedOption=[];
        this.dataFormat={
            start_time:"2017-06-01 09:00",
            end_time:"2017-07-01 09:00",
            data_type:"hour"
        };
        this.futureDataGet=[];
        this.fewDataOptionSet=[];
        var saveThis=this;
        var futureList=[];
/*        axios.get('/market/futures/',{
            params:{start_time:"2017-06-01 09:00"}
        }).then(function(res){
            saveThis.createMapData(res.data);
            //saveThis.future[res.data.status.data.future.code]=saveThis.splitAppendData(res.data);

        })*/
        axios.get('/market/futures/').then(function(res){
            res=res.data;
            if(res.status.code===0){
                saveThis.createMapData(res);
                Bus.$emit("getData", saveThis.mapData);
            }else{
                alert('出错')
            }
        })
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


    // var dataK=[];
    // for(var i=0;i<20;i++){
    //     dataK.push(splitData());
    // }
    this.optionbackup= {
        title:[
        {
            text: 'Future Data',
            subtext:"Please choose future",
            left:"10%",
            top:"0%"
        },
        {
            text: 'Option Data',
            subtext:"Please choose option",
            left:"10%",
            top:"45%"
        },
        {
            text: 'Option Implied volatility',
            subtext:"Please choose option",
            left:"60%",
            top:"0%"
        },
        {
            text: 'Implied volatility difference',
            subtext:"Need two options to display",
            left:"60%",
            top:"45%"
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
                dataZoom:{
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
            left: "10%",
            icon: "roundRect",
            gridIndex:1,
        }
        ],
        dataZoom: [
        {
            type: "inside",
            start: 50,
            end: 100,
            xAxisIndex: [0, 1,2,3]
        },
        {
            type: "slider",
            show: true,
            start: 50,
            end: 100,
            xAxisIndex: [0, 1,2,3],
            bottom: "0",
            left:"center"
        }
        ],
        visualMap:[
        ],
        grid: [
            //
            {
                left: '10%',
                height: '30%',
                top: "10%",
                width: "40%"
            },
            {
                left: '10%',
                bottom: '15%',
                height: '30%',
                width: "40%"
            },
            {
                left: '60%',
                top: '10%',
                height: '30%',
                width: "40%"
            },
            {
                left: '60%',
                bottom: '15%',
                height: '30%',
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
            },
            {
                type: 'category',
                gridIndex: 2,
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
            },
            {
                type: 'category',
                gridIndex: 3,
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
                splitArea: {
                    show: true
                }
            },
            {
                scale: true,
                gridIndex:1,
                splitArea: {
                    show: true
                }
            },
            {
                scale: true,
                gridIndex: 2,
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
                    tooltip: {
                        show:true,
                        formatter: "IV:{value}"
                    }
                }
            },
            {
                scale: true,
                gridIndex: 3,
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
                    tooltip: {
                        show:true,
                        formatter: function (params) {
                            return "IV difference\n" + (params.value * 100).toFixed(2) + "%";
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
        //this.createRandomFuture();
        //Bus.$emit("getData", this.mapData);
    this.option=this.deepClone(this.optionbackup);
    //initFuture();
    // this.loadFuture(this.future["name"][0]);
    this.myChart.setOption(this.option);
    // 自定义事件
    this.myChart.on("legendselectchanged",function(params){
        saveThis.option.legend[0].selected=saveThis.myChart.getOption().legend[0].selected;
        if(saveThis.checkSelection(params)==2){
            var selectName=saveThis.getSelectedName(params.selected);
            saveThis.showIVDifference(selectName);
        }else{
            saveThis.popSeries("Implied volatility difference");
            saveThis.option.title[3].subtext="Implied volatility difference will be displayed\nwhen you choose only two options"
        }
        var selectName=saveThis.getSelectedName(params.selected);
        if(selectName.length!=0){
            saveThis.option.title[1].subtext=selectName.join(",");
            saveThis.option.title[2].subtext=selectName.join(",");
        }
        saveThis.myChart.setOption(saveThis.option,true);
    })
    window.store=this;
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
    console.log(this.option,this.optionbackup)
    this.option=this.deepClone(this.optionbackup);
    console.log(this.option,this.optionbackup)
    this.readyCombinedOption=[];
    this.futureDataGet=[];
    this.future={
        name:[]
    };
    this.fewDataOptionSet=[];
    this.myChart.setOption(this.option,true);
},




changeDataFormat:function(){
    Bus.$emit("resetAllBtn");
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
            message: 'No specific date range was selected , please selected one',
            type: 'warning'
        })
        return ;
    }
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


randomGenWebSafeColor:function(){
  var base=["00","33","66","99","cc","ff"];
  var color="#"
  for(var i=0;i<3;i++){
    color+=base[Math.floor(Math.random()*6)];
}
return color;
},
createRandomFuture:function(){
    var futureNames=[]
    for(var i=0;i<5;i++){
      var name="期货"+Math.floor(Math.random()*1000+1000);
      futureNames.push(name);
      var names=[];
      var datas=[];
      var futureK=this.createRandomSeries();
      for(var j=0;j<5;j++){
        var data=this.createRandomSeries();
        names.push(data.series.name);
        datas.push(data);

        this.future[name]={
            names:names,
            datas:datas,
            dataK:futureK,
        };
        futureK.series.xAxisIndex=0;
        futureK.series.yAxisIndex=0;
        futureK.series.name=name;
    }
    this.future["name"]=futureNames;
}
},

createVisualMap:function(){
    this.option.visualMap[0].pieces=this.createRandomArea();
    this.option.visualMap[0].seriesIndex=this.option.series.length-1;
    this.option.visualMap[0].outOfRange={
      color: '#999'
  }
  this.option.visualMap[0].precision=4;
},

createRandomSeries:function(){
    var data = this.splitData();
    data.name = "M"+(Math.random()*1000+1000).toFixed(0);
    var series = this.deepClone(this.
      template.optionK);
    series.name = data.name;
    series.data = data.values;
    series.xAxisIndex=1;
    series.yAxisIndex=1
    var IVSeries = this.deepClone(this.
      template.optionIV);
    IVSeries.data = data.IVData;
    IVSeries.name = data.name;
    IVSeries.itemStyle.normal.color = this.randomGenWebSafeColor();
    IVSeries.xAxisIndex=2;
    IVSeries.yAxisIndex=2;
    return {
      series:series,
      IVSeries:IVSeries,
      xAxis:data.categoryData
  }

},

createRandomArea:function(){
    var pieces=[];
    var base=Math.random()*0.2;
    for(var i=0;i<3;i++){
      pieces.push({
        gt:base,
        lte:(base+=Math.random()*0.2),
        color:"green"
    })
  }
  return pieces;
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
    if(series.name===seriesName){
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
        newarr.push(this.deepClone(obj[i]));
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
//
//期货切换的函数
//清除上一个期货
clearLastFuture:function(){
  var futureName=this.option.title[0].subtext;
  var currentFuture=this.future[futureName];
  this.popSeries(futureName);
  var selectedName=this.getSelectedName();
  for(var i=0;i<currentFuture.names.length;i++){
    for(var name in selectedName){
      if(name==currentFuture.names[i]){
        continue;
    }
    this.popSeries(currentFuture.names[i])
}
}
this.popSeries("Implied volatility difference");
},
//载入下一个期货
loadFuture:function(futureName){
  var currentFuture=this.future[futureName]
  console.log(futureName);
  this.option.xAxis[0].data=currentFuture["dataK"].xAxis;
  this.option.xAxis[1].data=currentFuture["dataK"].xAxis;
  this.option.xAxis[2].data=currentFuture["dataK"].xAxis;
  this.option.xAxis[3].data=currentFuture["dataK"].xAxis;
  this.option.series.push(currentFuture["dataK"].series);
  for(var i=0;i<currentFuture["names"].length;i++){
    this.option.series.push(currentFuture["datas"][i].IVSeries);
    this.option.series.push(currentFuture["datas"][i].series);
}
this.option.legend[0].data=currentFuture["names"];
var selected={};
for(var i=0;i<this.future[futureName]["names"].length;i++){
    if(i<2){
      selected[this.future[futureName]["names"][i]]=true;
  }else{
      selected[this.future[futureName]["names"][i]]=false;
  }
}
this.option.legend[0].selected=selected;
this.showIVDifference(selected);
this.option.title[0].subtext=futureName;
var selectName=this.getSelectedName(selected);
if(selectName.length!=0){
    this.option.title[1].subtext=selectName.join(",");
    this.option.title[2].subtext=selectName.join(",");
}
this.myChart.setOption(this.option);
},
//计算期权隐含波动率之差
showIVDifference:function(selectName){
  var calcDataSet=[];
  var IVDSeries=this.deepClone(this.
    template.IVD);
  this.popSeries("Implied volatility difference");
  this.option.title[3].subtext=selectName[0]+"与"+selectName[1];
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
      return (value - data2[index]).toFixed(4);
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
createSeries:function(data){
    var series = this.deepClone(this.template.optionK);
    series.name = data.name;
    series.data = data.values;
    series.xAxisIndex=1;
    series.yAxisIndex=1;
    if(data.IVData.length!=0){
        var IVSeries = this.deepClone(this.template.optionIV);
        IVSeries.data = data.IVData;
        IVSeries.name = data.name;
        IVSeries.itemStyle.normal.color = this.randomGenWebSafeColor();
        IVSeries.xAxisIndex=2;
        IVSeries.yAxisIndex=2;
    }
    return {
        series:series,
        IVSeries:IVSeries,
        xAxis:data.categoryData
    }
},
//期货切换的函数
//清除上一个期货
addFuture: function(futureName){
    this.option.xAxis[0].data=this.future[futureName].dataK.xAxis;
    this.option.xAxis[1].data=this.future[futureName].dataK.xAxis;
    this.option.xAxis[2].data=this.future[futureName].dataK.xAxis;
    this.option.xAxis[3].data=this.future[futureName].dataK.xAxis;
    this.option.series.push(this.deepClone(this.future[futureName].dataK.series));
    this.option.title[0].subtext=futureName;
    this.myChart.setOption(this.option,true);
},
removeFuture: function(){
    var futureName=this.option.title[0].subtext
    this.popSeries(futureName);
    this.myChart.setOption(this.option,true);
},
addOption: function(futureName,optionName){
    var currentFuture=this.deepClone(this.future[futureName]);
    var index=currentFuture.names.indexOf(optionName);
    if(index!=-1){
        var series=currentFuture.datas[index].series;
        var IVSeries=currentFuture.datas[index].IVSeries;
        this.option.legend[0].data.push(optionName);
        this.option.series.push(IVSeries);
        this.option.series.push(series);
        this.myChart.setOption(this.option,true);
    }else{
        var zeroSeries=this.createZeroDataSeries(currentFuture.dataK.xAxis,{name:optionName})
        var series=zeroSeries.series;
        var IVSeries=zeroSeries.IVSeries;
        this.option.legend[0].data.push(optionName);
        this.option.series.push(IVSeries);
        this.option.series.push(series);
        this.myChart.setOption(this.option,true);
    }
},
popOption: function(optionName){
    this.popSeries(optionName);
    this.popLegend(optionName);
    this.myChart.setOption(this.option,true);
},
createRandomMapData: function() {
    this.createRandomFuture();
    var mapData={};
    for(var i=0;i<this.future.name.length;i++){
        var name=this.future.name[i];
        mapData[name]=this.future[name].names;
    }
    return mapData;
    //"qihuo1":["qiquan1,qiquan2,qiquan3"]
},
popLegend: function(optionName){
    for(var i=0 ;i<this.option.legend[0].data.length;i++){
        var name=this.option.legend[0].data[i]
        if(name==optionName){
            this.option.legend[0].data.splice(i,1);
            i--;
        }
    }
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
splitAppendData:function(res){
    var tag=res.status.data;
    var threshold=0
    var data={};
    var futureValues=tag.future.data.map(function(o){
        return [o.open_price,o.close_price,o.max_price,o.min_price]
    });
    var futureXAxis=tag.future.data.map(function(o){
        return o.time
    });
    var dataK=this.createSeries({
        name:tag.future.code,
        values:futureValues,
        categoryData:futureXAxis,
        IVData:["-"]
    });
    dataK.series.xAxisIndex=0;
    dataK.series.yAxisIndex=0;
    var optionNames=tag.options.map(function(o){
        if(o.data.length>=threshold){
            return o.code;
        }else{
            return "-"
        }
    });
    for(var i=0;i<optionNames.length;i++){
        if(optionNames[i]=="-"){
            optionNames.splice(i,1);
            this.mapData[tag.future.code].splice(i,1);
            i--;
        }
    }
    var optionSeries=[];
    for(var i=0;i<tag.options.length;i++){
        var option=tag.options[i];
        if((option.data.length<40&&this.dataFormat.data_type=="hour")||
            (option.data.length<3&&this.dataFormat.data_type=="day")){
            this.fewDataOptionSet.push(option.code);
            var optionProc=this.createZeroDataSeries(futureXAxis,{name:option.code});
        }else{
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
        }
        optionProc.series.data=this.alignTimeAxis(dataK.xAxis,optionProc.xAxis,optionProc.series.data);
        if(optionProc.series.name!=tag.future.code){
            optionProc.IVSeries.data=this.alignTimeAxis(dataK.xAxis,optionProc.xAxis,optionProc.IVSeries.data);
        }
        optionSeries.push(optionProc)
    }
    return {
        names:optionNames,
        dataK:dataK,
        datas:optionSeries
    }
},
createZeroDataSeries:function(futureXAxis,obj){
    var series = this.deepClone(this.template.optionK);
    series.name = obj.name;
    series.data = [["-","-","-","-"]];
    series.xAxisIndex=1;
    series.yAxisIndex=1;
    var IVSeries = this.deepClone(this.template.optionIV);
    IVSeries.data = ["-"];
    IVSeries.name = obj.name;
    IVSeries.itemStyle.normal.color = this.randomGenWebSafeColor();
    IVSeries.xAxisIndex=2;
    IVSeries.yAxisIndex=2;
    return {
        series:series,
        IVSeries:IVSeries,
        xAxis:futureXAxis
    }
},
createMapData:function(res){
    for(var i=0;i<res.future_list.length;i++){
        var future=res.future_list[i];
        this.mapData[future.code]=future.options;
    }
},
putCombination:function(){
    if(this.readyCombinedOption.length==2){
        var saveThis=this;
        axios.put('/client/add_combo/',
            {positive_option:this.readyCombinedOption[0],negative_option:this.readyCombinedOption[1]},
            {validateStatus:null}
            ).then(function(res){
              if(res.data.status.code=='0'){
                  saveThis.$notify({
                      title: 'Success',
                      message: 'You have successfully chosen option '+saveThis.readyCombinedOption[0]+"and option "+saveThis.readyCombinedOption[1],
                      type: 'success'
                  });
              }else if(res.data.status.code=="-6"){
                saveThis.$notify.error({
                    title: 'Error',
                    message: 'You have chosen an nonexistent option or the combination you choose is unpredictable',
                    type: 'danger'
                });
              }
              else{
                  saveThis.$notify.error({
                      title: 'Error',
                      message: 'Some internal error occurred...',
                      type: 'danger'
                  });
              }
          }).catch(function(e){
            saveThis.$notify.error({
              title: 'Error',
              message: 'Network connection got some problems',
              type: 'danger'
            })
    })
      }
          else{
        this.$notify({
          title: 'Attention',
          message: 'You need to select two options before you specify a combination',
          type: 'warning'
      });
    }
}


}

}
</script>



<style lang="less" scoped>
  @import '../style/common';
.el-input__icon .el-icon-date{
    padding-left: 200px;
}

</style>
