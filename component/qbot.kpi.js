function create_module_data(data){
  chartmodel = document.createElement('p');
  chartmodel.style.width = "800px";
  chartmodel.style.height = "450px";
  var myChart = echarts.init(chartmodel);
  TimeStamp = [];
  module_name = [];
  latency = {};
  count = {};
  obj = {};

  for(var i=0;i<data.length;i++){
    time_ishere = TimeStamp.indexOf(data[i]['TimeStamp']);
    module_ishere = module_name.indexOf(data[i]['Module']);
    if(time_ishere==-1){
      TimeStamp.push(data[i]['TimeStamp']);
    }
    if(module_ishere==-1){
      module_name.push(data[i]['Module']);
    }
  }
  for(var m=0;m<module_name.length;m++){
    latency[module_name[m]] = []
    count[module_name[m]] = []
    obj[module_name[m]] = []
    for(var n=0;n<TimeStamp.length;n++){
      latency[module_name[m]][TimeStamp[n]] = 0
      count[module_name[m]][TimeStamp[n]] = 0
    }
  }
  for(var i=0;i<data.length;i++){
    for(var k=0;k<module_name.length;k++){
      if(data[i]['Module']==module_name[k]){
        for(var j=0;j<TimeStamp.length;j++){
          if(data[i]['TimeStamp']==TimeStamp[j]){
            latency[module_name[k]][TimeStamp[j]] += data[i]['Latency'];
            count[module_name[k]][TimeStamp[j]] ++;
          }
        }
      }
    }
  }
  for(var i=0;i<module_name.length;i++){
    for(var j=0;j<TimeStamp.length;j++){
      if(count[module_name[i]][TimeStamp[j]]==0){
        svg = 0;
      }
      else{
        svg = latency[module_name[i]][TimeStamp[j]]/count[module_name[i]][TimeStamp[j]];
      }
      obj[module_name[i]].push(svg.toFixed(5));
    }
  }
  series_data = [];
  for(var i=0;i<(Object.keys(module_name)).length;i++){
    if(TimeStamp.length==1){
      series_data.push({name:module_name[i],type:'bar',data:obj[module_name[i]]})
    }
    else{
      series_data.push({name:module_name[i],type:'line',data:obj[module_name[i]]})
    }
  }
  zoom_start = parseInt((TimeStamp.length-20)/5)
  datazoom = [{id: 'dataZoomX',type: 'slider',start: zoom_start,end: 100,xAxisIndex: [0],filterMode: 'filter'}]
  option = {
      tooltip: {
          trigger: 'axis'
      },
      dataZoom: datazoom,
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
          type: 'value'
      },
      series: series_data
  };
  myChart.setOption(option);
  return chartmodel;
}

function drawTable(bubbleContent,data) {
  key_list = [];
  data_list = [];
  for(var key in data[0]){
    key_list.push(key)
  }
  for(i=0;i<data.length;i++){
    list = [];
    for(j=0;j<key_list.length;j++){
      list.push(data[i][key_list[j]]);
    }
    data_list.push(list);
  }
  var chart = new google.visualization.DataTable();
  for(i=0;i<key_list.length;i++){
    chart.addColumn('string',key_list[i])
  }
  for(i=0;i<data_list.length;i++){
    chart.addRows([data_list[i]]);
  }
  var table = new google.visualization.Table(bubbleContent);
  table.draw(chart, {showRowNumber: true, width: '800px'});
}

function create_visitor_stats(data){
  chartmodel = document.createElement('p');
  chartmodel.style.width = "800px";
  chartmodel.style.height = "450px";
  var myChart = echarts.init(chartmodel);
  TimeStamp = [];
  Visitors = [];
  Hits = [];


  for(var i=0;i<data.length;i++){
    TimeStamp.push(data[i]['TimeStamp']);
    Visitors.push(data[i]['Visitor']);
    Hits.push(data[i]['Hits']);
  }


  zoom_start = parseInt((TimeStamp.length-20)/5)
  datazoom = [{id: 'dataZoomX',type: 'slider',start: zoom_start,end: 100,xAxisIndex: [0],filterMode: 'filter'}]
  option = {
      tooltip: {
          trigger: 'axis'
      },
      dataZoom: datazoom,
      legend: {
          data: 'dummy',
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
       yAxis: [{
          name: 'Visitors',
          type: 'value',
      },
      {
          name: 'Hits',
          type: 'value',
      }],
      series:
       [
           {
           name:'Visitor',
           type:'bar',
           data:Visitors,
           color: 'LightSteelBlue',
           yAxisIndex: 0,
           },
           {name:'Hits',
           type:'line',
           color: 'Auqamarin',
           yAxisIndex: 1,
           data:Hits}
       ]
  };
  myChart.setOption(option);
  return chartmodel;
}

function create_qna_stats(data){
  chartmodel = document.createElement('p');
  chartmodel.style.width = "800px";
  chartmodel.style.height = "450px";
  var myChart = echarts.init(chartmodel);
  TimeStamp = [];
  Total = [];
  Accuracy = [];


  for(var i=0;i<data.length;i++){
    TimeStamp.push(data[i]['TimeStamp']);
    Total.push(data[i]['Total']);
    Accuracy.push(data[i]['Accuracy']);
  }

  series_data = []
  series_data.push({name:'Total',type:'bar',data:Total})
  series_data.push({name:'Accuracy',type:'line',data:Accuracy})

  zoom_start = parseInt((TimeStamp.length-20)/5)
  datazoom = [{id: 'dataZoomX',type: 'slider',start: zoom_start,end: 100,xAxisIndex: [0],filterMode: 'filter'}]
  option = {
      tooltip: {
          trigger: 'axis'
      },
      dataZoom: datazoom,
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
      yAxis: [{
          name: 'Responses',
          type: 'value',
      },
      {
          name: 'Accuracy',
          type: 'value',
          axisLabel:{
            show: true,
            interval: 'auto',
            formatter: '{value} %'
          },
          show: true
      }],
      series: [
           {
               name:'Total',
               type:'bar',
               data:Total,
               color: 'LightSteelBlue',
               yAxisIndex: 0,
           },
           {
               name:'Accuracy',
               type:'line',
               color: 'Auqamarin',
               yAxisIndex: 1,
               data:Accuracy,
           }
       ]
  };
  myChart.setOption(option);
  return chartmodel;
}