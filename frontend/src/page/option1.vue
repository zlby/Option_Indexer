<template>
  <div id="charts">


    <el-row :gutter="20" style=" margin-top:10px">
    <el-col :span="16" offset="1">
  <div id="main" style="width:120%;height:600px;"></div>
  </el-col>
</el-row>



</div>



</template>

<script>
  import echarts from 'echarts'
  import Bus from '../bus'

    export default{
    created:function(){
        Bus.$on('addNewOption', optionObj=>{
            this.removeFuture();
            this.addFuture(optionObj.future)
            this.addOption(optionObj.future, optionObj.option)
        })
    },
    mounted:function(){
        

    this.myChart=echarts.init(document.getElementById('main'));

    this.future={
    }
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
            name:"隐含波动率之差",
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
    this.option= {
        title:[
            {
                text: '期货数据',
                subtext:"",
                left:"5%",
                top:"0%"
            },
            {
                text: '期权数据',
                subtext:"",
                left:"5%",
                top:"45%"
            },
            {
                text: '期权隐含波动率',
                subtext:"",
                left:"55%",
                top:"0%"
            },
            {
                text: '隐含波动率之差',
                subtext:"",
                left:"55%",
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
                dataZoom: {
                    yAxisIndex: false
                }
            }
        },
        axisPointer: {
            link: {xAxisIndex: 'all'}
        },
        legend: [
            {
                data:null,
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
                left: '5%',
                height: '30%',
                top: "10%",
                width: "40%"
            },
            {
                left: '5%',
                bottom: '15%',
                height: '30%',
                width: "40%"
            },
            {
                left: '55%',
                top: '10%',
                height: '30%',
                width: "40%"
            },
            {
                left: '55%',
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
                    label: {
                        formatter: function (params) {
                            return "隐含波动率\n" + (params.value * 100).toFixed(2) + "%";
                        }
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
                    label: {
                        formatter: function (params) {
                            return "隐含波动率之差\n" + (params.value * 100).toFixed(2) + "%";
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
    this.createRandomFuture();
    //initFuture();
    this.loadFuture(this.future["name"][0]);
    this.myChart.setOption(this.option);
    var saveThis=this;
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
})


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
    console.log(pieces);
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
    if(series.name.indexOf(seriesName)!=-1){
      this.option.series.splice(i,1)
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
  this.popSeries("隐含波动率之差");
  console.log(this.option.series);
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
showIVDifference:function(selected){
  var selectName=this.getSelectedName(selected);
  var calcDataSet=[];
  var IVDSeries=this.deepClone(this.
    template.IVD);
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

//期货切换的函数
//清除上一个期货
addFuture: function(futureName){
    this.option.xAxis[0].data=this.future[futureName].dataK.xAxis;
    this.option.xAxis[1].data=this.future[futureName].dataK.xAxis;
    this.option.xAxis[2].data=this.future[futureName].dataK.xAxis;
    this.option.xAxis[3].data=this.future[futureName].dataK.xAxis;
    this.option.series.push(this.future[futureName].dataK.series);
    this.option.title[0].subtext=futureName;
    this.myChart.setOption(this.option,true);
},
removeFuture: function(){
    var futureName=this.option.title[0].subtext
    this.popSeries(futureName);
    this.myChart.setOption(this.option,true);
},
addOption: function(futureName,optionName){
    var currentFuture=this.future[futureName];
    var index=currentFuture.names.indexOf(optionName);
    var series=currentFuture.datas[index].series;
    var IVSeries=currentFuture.datas[index].IVSeries;
    this.option.series.push(IVSeries);
    this.option.series.push(series);
    this.option.legend[0].data.push(optionName);
    this.myChart.setOption(this.option,true);
},
popOption: function(optionName){
    this.popSeries(optionName);
    this.popLegend(optionName);
    this.myChart.setOption(this.option,true);
},
createMapData: function() {
    this.createRandomFuture();
    var mapData={};
    for(var i=0;i<future.name.length;i++){
        var name=future.name[i];
        mapData[name]=future[name].names;
    }
    return mapData;
    //"qihuo1":["qiquan1,qiquan2,qiquan3"]
},


}

}
</script>




