var nodeStatic = require('node-static');
var http = require('http');
var ws = require('ws');

// port 10000: static file - serving static files in this directory

var fileServer = new nodeStatic.Server(__dirname);

http.createServer(function (request, response) {
  request.addListener('end', function () {
    fileServer.serve(request, response);
  }).resume();
}).listen(10000); 

// port 10010: websockets - allow users to subscribe

var wss = new ws.Server({ port: 10010 });

// port 10020: receives python uploads, and directly forward to websockets clients

http.createServer(function(request, response) {
  var str = '';
  request.on('data', function (data) {
    str += data;
  });
  request.on('end', function () {
    var jsonObj = JSON.parse(str);
    jsonObj.ip = request.connection.remoteAddress;
    wss.clients.forEach(function (client) {
      client.send(JSON.stringify(jsonObj));
    });
    console.log('A message ' + str.replace(/\s+/g, ' ') + ' forwarded to ' + wss.clients.length + ' clients!');
    response.end();
  });
}).listen(10020);

// that's all!

console.log('All three servers started!');