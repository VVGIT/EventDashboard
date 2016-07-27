function buildTrend2() {

    $('#row1').append('<div id=chart-trend2 class=w3-half class=w3-container><div id=inner2></div></div>');
    $('#banner').append('</div>');

    var options = {

        chart: {
            type: 'column',
            events: {
                load: function () {
                    var self = this;
                    setInterval(function () {
                        $.ajax({
                           type: 'POST',
                           url: 'http://localhost:5000/getData.py',
                           data: 'ITR',
                           dataType: 'text',
                           contentType: 'text/plain',
                           xhrFields: {withCredentials: false},
                           headers: {
                               'Access-Control-Allow-Origin': 'http://localhost:3000',
                               'Access-Control-Allow-Credentials': false
                           }
                        }).done(function(o) {
                            
                        });
                                                
                        $.getJSON('trends2.json', function (data) {
                            var series = self.series[0];
                            series.setData(data);
                        });
                    }, 5000);
                }
            },
            animation: {
                duration: 200
            }
        },
        title: {
            text: '2017 ITR Events'
        },
        xAxis: {
            type: 'number',
            title: {
                text: 'Region Number'
            }
        },
        yAxis: {
            type: 'currency',
            title: {
                text: 'Dollar Value of events (in Billions)',
                margin: 10
            },
            labels: {
                formatter: function() {
                    return '$ ' + this.value;
                }
            }
        },
        series: [{
            showInLegend: false,
            // pointInterval: 3600*1000 //minute
            data: [],
            dataLabels: {
                enabled: true,
                rotation: 0,
                color: '#872657',
                align: 'center',
                format: '$' + '{point.y:.1f}',
                y: 0, // 10 pixels down from the top
                style: {
                    fontSize: '11px',
                    fontFamily: 'Verdana, sans-serif'
                }
            }
        }]
    };

    $('#chart-trend2').highcharts(options);

}