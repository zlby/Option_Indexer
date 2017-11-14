<template>
    <div id="radar" style="width:500px;height:300px">
    </div>
</template>

<script>
    import echarts from 'echarts'
    import Bus from '../bus'
    export default{
        created:function(){
            Bus.$on('getMapData', optionObj=>{

            })
        },
        mounted:function(){
            this.myChart= echarts.init(document.getElementById('radar'));
            var saveThis=this; 
            this.option = {
                backgroundColor: '#e8e8e8',
                title: {
                    text: '期权组合预期收益',
                    left: 0,
                    top:0,
                    textStyle: {
                        color: '#000'
                    }
                },
                tooltip:{
                    trigger:"item",
                    backgroundColor : 'rgba(0,0,250,0.2)',
                    formatter:function(params){
                        var rtnStr="现起直到"+params.seriesName;
                        var indicator=saveThis.option.radar.indicator;
                        for(var i=0;i<indicator.length;i++){
                            rtnStr+="<br/>"+indicator[i].name+"预期收益:"+params.data[i]+"元"
                        };
                        rtnStr+="<br/>置信率:95%"
                        return rtnStr;
                    },
                    position: function (pos, params, el, elRect, size) {
                        var obj = {
                            top: 0,
                            right:0
                        };
                    //obj[['left', 'right'][+(pos[0] < size.viewSize[0] / 2)]] = 30;
                    return obj;
                },
            },
            legend:[{
                top: 30,
                left:0,
                data: ['7-20', '7-21', '7-22'],
                itemGap: 3,
                textStyle: {
                    color: '#fff',
                    fontSize: 10
                },
                orient:"vertical",
                align:"left",
                selectedMode: 'multiple'
            }],
            // visualMap: {
            //     show: true,
            //     min: 0,
            //     max: 20,
            //     dimension: 6,
            //     inRange: {
            //         colorLightness: [0.5, 0.8]
            //     }
            // },
            visualMap: {
                color: ['#ff1919', '#da1584','#891bc0','#4d27c4','#2650c2'],
                type: 'continuous',
                min: 5000,
                max: 10000,
            },
            radar: {
                indicator: [
                ],
                shape: 'polygon',
                splitNumber: 5,
                name: {
                    textStyle: {
                        color: 'rgb(0, 0, 0)'
                    }
                },
                radius:"75%",
                splitLine: {
                    lineStyle: {
                        color: [
                        'rgba(0, 0, 0, 1)', 'rgba(0, 0, 0, 1)',
                        'rgba(0, 0, 0, 1)', 'rgba(0, 0, 0, 1)',
                        'rgba(0, 0, 0, 1)', 'rgba(0, 0, 0, 1)'
                        ].reverse()
                    }
                },
                name:{
                    formatter:function(value,indicator){
                        return value.split("与").join("\n")
                    }
                },
                splitArea: {
                    show: false
                },
                axisLine: {
                    lineStyle: {
                        color: 'rgba(0, 0, 0,1)'
                    }
                }
            },
            series:null,
            animationDelay: function (idx) {
                return idx * 1000;
            },
            animation:true,
        };
        var lineStyle = {
            normal: {
                width: 2,
                opacity: 1
            }
        };
        this.template={
            series:{
                name:null ,
                type: 'radar',
                lineStyle: lineStyle,
                data: null,
                symbol: 'none',
                itemStyle: {
                    normal: {
                        color: '#F9713C'
                    }
                },
                areaStyle: {
                    normal: {
                        opacity: 0.1
                    },
                    emphasis : {
                        areaStyle: {color:'rgba(0,250,0,0.3)'}
                    }
                }
            }
        }
        this.originData=this.createRandomData()
        this.loadData(this.deepClone(this.originData));
        this.myChart.setOption(this.option);
        this.setDefaultSelection();
        var current=0;
        window.legend_t=setInterval(function(){
            saveThis.myChart.dispatchAction({
                    type:"legendSelect",
                    name:saveThis.option.legend[0].data[current],
            });
            current++;
            if(current==7){
                window.clearInterval(window.legend_t)
            }
        },300)
    },
    methods:{
        createOneCombinationData:function(){
            var data=[]
            for(var i=0;i<this.option.series.length;i++){
                data.push((Math.random()*5000+5000).toFixed(0));
            }
            return data;
        },
        setDefaultSelection:function(){
            var selected={};
            for(var i=0;i<this.option.legend[0].data.length;i++){
                selected[this.option.legend[0].data[i]]=false;
            }
            this.option.legend[0].selected=selected;
            this.myChart.setOption(this.option,true);
        },
        popCombination:function(combinationName){
            var index=this.getCombinationIndex(combinationName);
            console.log(index,combinationName);
            console.log(this.option.series);
            for(var i=0;i<this.option.series.length;i++){
                this.option.series[i].data[0].splice(index,1)
            }
            console.log(this.option.series);
            this.option.radar.indicator.splice(index,1);

            this.myChart.setOption(this.option,true);
        },
        getCombinationIndex:function(combinationName){
            for(var i=0;i<this.option.radar.indicator.length;i++){
                var name=this.option.radar.indicator[i].name;
                if(name===combinationName){
                    return i;
                }
            }
        },
        addCombination:function(){
            var data=this.createOneCombinationData();
            var option1="M"+(Math.random()*1000+1000).toFixed(0)+"-"+(Math.random()*1000+1000).toFixed(0);
            var option2="M"+(Math.random()*1000+1000).toFixed(0)+"-"+(Math.random()*1000+1000).toFixed(0);
            var name=option1+"与"+option2;
            this.option.radar.indicator.push({
                name:name,
                max:10000
            });
            for(var i=0;i<this.option.series.length;i++){
                this.option.series[i].data[0].push(data[i]);
            }
            this.myChart.setOption(this.option,true);
        },
        createRandomData:function(){
            var indicator=[];
            var legendData=[];
            var datas=[];
            var date=echarts.number.parseDate("2017-07-19");
            var max=0
            for(var i=1;i<=7;i++){
                date.setTime(date.getTime()+86400000);
                var dateStr=echarts.format.formatTime("MM-dd",date)
                legendData.push(dateStr);
                var data=[];
                for(var j=0;j<5;j++){
                    var option1="M"+(Math.random()*1000+1000).toFixed(0);
                    var option2="M"+(Math.random()*1000+1000).toFixed(0);
                    var name=option1+"与"+option2;
                    var random=(Math.random()*1000*i+5000).toFixed(0);
                    data.push(random);
            //if(random>max) max=random;
            if(i==1){
                indicator.push({
                    name:name,
                    max:12000
                });
            }
        }
        var series=this.loadSeries({
            name:dateStr,
            data:[data]
        });
        datas.push(series);
    }
    datas=datas;
    return {
        datas:datas,
        legend:legendData,
        indicator:indicator
    }
},
loadData:function(datas){
    console.log(datas);
    this.option.legend[0].data=datas.legend;
    this.option.radar.indicator=datas.indicator;
    this.option.series=datas.datas
    console.log(this.option);
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
loadSeries:function(datas){
    var series=this.deepClone(this.template.series);
    series.name=datas.name;
    series.data=datas.data;
    var color=this.randomGenWebSafeColor();
    /*series.itemStyle={
        normal:{
            color:color,
        }
    }
    series.areaStyle={
        emphasis:{
            color:color
        }
    }*/
    return series;
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

