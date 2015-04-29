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

var currentPi, ip;

var wssb = new ws.Server({ port: 10010 });
var wssp = new ws.Server({ port: 10030 });

// port 10010: websockets for browsers - allow users to subscribe

wssb.on('connection', function (client) {
  ws.on('message', function (message) {
    currentPi.send(message);
    console.log('An instruction ' + str.replace(/\s+/g, ' ') + ' forwarded to ' + ip + '!');
  });
});

// port 10030: websockets for python on pi

wssp.on('connection', function (client) {
  var currentPi = client;
  ip = client.upgradeReq.connection.remoteAddress;
  client.on('message', function (message) {
    var jsonObj = JSON.parse(str);
    jsonObj.ip = ip;
    wssb.clients.forEach(function (client) {
      client.send(JSON.stringify(jsonObj));
    });
    console.log('A message ' + str.replace(/\s+/g, ' ') + ' forwarded to ' + wss.clients.length + ' clients!');
  });
});
