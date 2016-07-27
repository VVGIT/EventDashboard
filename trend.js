var express = require('express');
var app = express();

//require('highcharts/modules/exporting')(Highcharts);
var port = process.env.PORT || 5000;
app.use(express.static('public'));
app.use(express.static('src/views'));
app.use(express.static('src/css'));
app.use(express.static('public/Python'));
app.use(express.static('public/json'));

app.listen(port, function (err) {
    console.log('Listening on port: ' + port);
});
