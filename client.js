// Let us open a web socket
var ws = new WebSocket('ws://' + window.location.hostname + ':10010/');
ws.onmessage = function (evt)  {
  var msg = evt.data;
  console.log(msg);
};
ws.onclose = function() {
  alert('WebSockets connection is closed.');
};