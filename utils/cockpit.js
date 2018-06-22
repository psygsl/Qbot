
function create_cockpit_data(data){
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
