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
  client.on('message', function (message) {
    currentPi.send(message);
    console.log('An instruction ' + message.replace(/\s+/g, ' ') + ' forwarded to ' + ip + '!');
  });
});

// port 10030: websockets for python on pi

wssp.on('connection', function (pi) {
  currentPi = pi;
  ip = pi.upgradeReq.connection.remoteAddress;
  pi.on('message', function (message) {
    var jsonObj = JSON.parse(message);
    jsonObj.ip = ip;
    wssb.clients.forEach(function (client) {
      client.send(JSON.stringify(jsonObj));
    });
    console.log('A message ' + message.replace(/\s+/g, ' ') + ' forwarded to ' + wssb.clients.length + ' clients!');
  });
});
