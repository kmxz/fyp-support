var nodeStatic = require('node-static');
var http = require('http');
var ws = require('ws');

// port 10000: static file - serving static files in this directory

var fileServer = new nodeStatic.Server(__dirname, { cache: 0 });

http.createServer(function (request, response) {
  request.addListener('end', function () {
    fileServer.serve(request, response);
  }).resume();
}).listen(10000); 

var currentPi, ip;

var wsjsb = new ws.Server({ port: 10010 });
var wsjsp = new ws.Server({ port: 10030 });
var wsbsb = new ws.Server({ port: 10060 });
var wsbsp = new ws.Server({ port: 10070 });

// port 10010: websockets for browsers, json

wsjsb.on('connection', function (client) {
  client.on('message', function (message) {
    try {
      currentPi.send(message);
      console.log('An instruction ' + message.replace(/\s+/g, ' ') + ' forwarded to ' + ip + '!');
    } catch (e) {
      console.error(e);
    }
  });
});

// port 10030: websockets for python on pi, json

wsjsp.on('connection', function (pi) {
  currentPi = pi;
  ip = pi.upgradeReq.connection.remoteAddress;
  pi.on('message', function (message) {
    var jsonObj = JSON.parse(message);
    jsonObj.ip = ip;
    try {
      wsjsb.clients.forEach(function (client) {
        client.send(JSON.stringify(jsonObj));
      });
      console.log('A message ' + message.replace(/\s+/g, ' ') + ' forwarded to ' + wsjsb.clients.length + ' clients!');
    } catch (e) {
      console.error(e);
    }
  });
});

// port 10070: websockets for python on pi, binary

wsbsp.on('connection', function (pi) {
  pi.on('message', function (message) {
    try {
      wsbsb.clients.forEach(function (client) {
        client.send(message);
      });
      console.log('A binary forwarded to ' + wsbsb.clients.length + ' clients!');
    } catch (e) {
      console.error(e);
    }
  });
});

console.log('10000, 10010, 10030, 10060 and 10070 port started.');