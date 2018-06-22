
function create_cockpit_data(data){     // create chart by using echarts library
  chartmodel = document.createElement('p');
  chartmodel.style.width = "800px";
  chartmodel.style.height = "450px";
  var myChart = echarts.init(chartmodel);
  TimeStamp = [];
  module_name = [];
  cockpit_data = {};
  var min_y = 0;

  for(var tmp in data[0]){
    if(tmp!='time' && tmp!='category')
      module_name.push(tmp);
  }
  for(var i=0;i<data.length;i++){
    time_ishere = TimeStamp.indexOf(data[i]['time']);
    if(time_ishere==-1){
      TimeStamp.push(data[i]['time']);
    }
  }
  for(var m=0;m<module_name.length;m++){
    cockpit_data[module_name[m]] = []
  }
  min_y = data[0][module_name[0]];
  for(var i=0;i<data.length;i++){
    for(var k=0;k<module_name.length;k++){
        if(data[i][module_name[k]]<min_y){
          min_y = data[i][module_name[k]];
        }
        cockpit_data[module_name[k]].push(data[i][module_name[k]]);
    }
  }

  series_data = [];
  for(var i=0;i<(Object.keys(module_name)).length;i++){
    if(TimeStamp.length==1){
      min_y = 0;
      series_data.push({name:module_name[i],type:'bar',data:cockpit_data[module_name[i]]})
    }
    else{
      series_data.push({name:module_name[i],type:'line',data:cockpit_data[module_name[i]]})
    }
  }
  if(data[0]['category']=='cpvi'){
    axisLabel = {formatter: function (value, index){return value.toFixed(1)+'%';}}
  }
  else{
    axisLabel = {formatter: function (value, index){return value}}
  }
  option = {
      tooltip: {
          trigger: 'axis',
      },
      //dataZoom: datazoom,
      legend: {
          data: module_name,
          type: 'scroll',
          orient: 'vertical',
          right: 5,
          top:10,
          bottom: 10
      },
      grid: {
          left: '3%',
          right: '25%',
          bottom: '12%',
          containLabel: true
      },
      xAxis: {
          type: 'category',
          boundaryGap: false,
          data: TimeStamp,
          axisLabel : {
            interval:0,
            rotate:"67.5"
        }
      },
      yAxis: {
          type: 'value',
          splitNumber:3,
          min:min_y,
          axisLabel:axisLabel
      },
      series: series_data
  };
  myChart.setOption(option);
  return chartmodel;
}

function create_highcharts(data){     // create chart by using highcharts library
  chartmodel = document.createElement('div');
  chartmodel.style.width = "600px";
  chartmodel.style.height = "350px";
  x_filter = data[0]['x_filter'];     
  category = data[0]['category'];     // this value is the cockpit name.
  y_unit = '';                        // this value is the unit . if the chart data has unit , need add it . such as the CPVi chart's unit is '%' .so i add unit after
  subtitle_font = 'Filter : ALL'      // this value is filter title . i add this value in chart subtitle.
  if(data[0]['filter_data'].length!=0){
    subtitle_font = 'Filter : '
    for(i=0;i<data[0]['filter_data'].length;i++){
      subtitle_font+=data[0]['filter_data'][i]+'  '
    }
  }

  key_all = Object.keys(data[0]);     // get the data filters and save into the key_all
  var obj = {}
  for(var i=0;i<key_all.length;i++){
    obj[key_all[i]] = [];
  }
  for(var i=0;i<data.length;i++){
    for(var j=0;j<key_all.length;j++){
      if(!isNaN(data[i][key_all[j]])){
        obj[key_all[j]].push(parseFloat(data[i][key_all[j]]));
      }else{
        obj[key_all[j]].push(data[i][key_all[j]]);
      }
    }
  }
  series_data = [];
  for(var i=0;i<(Object.keys(obj)).length;i++){
    if(!isNaN(obj[key_all[i]][0])){
      series_data.push({name:key_all[i],type: 'spline',data:obj[key_all[i]]})
    }
  }
  if(category=='CPVi'){
    y_unit = "%"
  }
  json = {
    title : {     // this is the toptitle.show the cockpit name.
      text: category+' Chart'   
    },
    subtitle : {      // this is the subtitle.show the filter.
      text: subtitle_font
    },
    xAxis : {     // this is the xAxis.
      categories: obj[x_filter]
    },
    yAxis : {     // this is the yAxis.
      title:{
        text:""
      },
      labels: {formatter: function() { return this.value + y_unit;}},
      plotLines: [{
          width: 1,
          color: '#808080'
      }]
    },
    tooltip:{
      shadow: true,                
      animation: true,
      borderRadius: 10,
      valueSuffix: y_unit
    },
    legend : {
        layout: 'vertical',
        align: 'right',
        verticalAlign: 'middle',
        borderWidth: 0
    },
    credits: {  
      enabled: false     //do not show the logo
    },
    series :  series_data     
  }
  var chart = Highcharts.chart(chartmodel, json);
  return chartmodel;
}