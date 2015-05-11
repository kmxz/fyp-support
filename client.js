window.onload = function () {

  var REMOTE_HOST = window.location.hostname;

  var toFriendlyTime = function (timestampInSeconds) {
    var date = new Date(timestampInSeconds * 1000);
    var now = new Date().getTime();
    var ago = Math.round(now / 1000 - timestampInSeconds);
    return date.toLocaleTimeString() + ' (' + ago + ' s ago)';
  };

  var heartBeatSpan = document.getElementById('heartbeat');
  var ipSpan = document.getElementById('ip');
  var lastHeartBeat = null;

  var sonicGrids = Array.prototype.slice.call(document.getElementsByClassName('grid-points'));
  var sonicPoints = sonicGrids.map(function () { return []; });
  var sonicDistLabels = Array.prototype.slice.call(document.querySelectorAll('.us-last span'));
  var sonicDists = sonicDistLabels.map(function () { return null; })
  var sonicTimeLabels = Array.prototype.slice.call(document.querySelectorAll('.us-last small'));
  var sonicTimes = sonicTimeLabels.map(function () { return null; })

  var qrTbody = document.querySelector('tbody');
  var qrCodes = [];
  var pictureElSlots = [];
  var currentPictureIndex = -1;

  var text = function (el, content) {
    el.replaceChild(document.createTextNode(content), el.firstChild);
  };

  var prepend = function (el, child) {
    el.insertBefore(child, el.firstChild);
  };

  // let us open a web socket
  var ws = new WebSocket('ws://' + REMOTE_HOST + ':10010/');
  ws.onmessage = function (evt) {
    var msg = JSON.parse(evt.data);
    lastHeartBeat = msg.time;
    text(ipSpan, msg.ip);
    msg.ultrasonic.forEach(function (sonic, index) {
      Array.prototype.push.apply(sonicPoints[index], sonic.map(function (point) {
        var element = document.createElement('div');
        element.className = 'grid-point';
        element.style.top = Math.max(0, 400 - point.distance) / 4 + '%';
        element.style.right = '0';
        sonicGrids[index].appendChild(element);
        return {
          time: point.time,
          dist: point.distance,
          element: element
        };
      }));
    });
    Array.prototype.push.apply(qrCodes, msg.qr.map(function (code) {
      var tr = document.createElement('tr');
      var timeTd = document.createElement('td');
      var time = document.createTextNode(toFriendlyTime(code.time));
      timeTd.appendChild(time);
      tr.appendChild(timeTd);
      var contentTd = document.createElement('td');
      var content = document.createTextNode(code.content);
      contentTd.appendChild(content);
      tr.appendChild(contentTd);
      prepend(qrTbody, tr);
      return {
        time: code.time,
        timeTd: timeTd
      }
    }));
  };
  ws.onclose = function () {
    alert('WebSockets connection is closed.');
  };

  var refresh = function () {
    var time = new Date().getTime() / 1000;
    if (lastHeartBeat) {
      text(heartBeatSpan, toFriendlyTime(lastHeartBeat));
    }
    sonicPoints.forEach(function (points, index) {
      points.forEach(function (point) {
        if (point.time > sonicTimes[index]) {
          sonicTimes[index] = point.time;
          sonicDists[index] = Math.round(point.dist);
        }
        var ratio = distRight = (time - point.time) / 20;
        if (ratio < 1) {
          point.element.style.right = ratio * 100 + '%';
        } else {
          point.element.parentNode.removeChild(point.element);
          point.element = null;
        }
      });
    });
    sonicPoints = sonicPoints.map(function (points) {
      return points.filter(function (point) {
        return !!point.element;
      });
    });
    sonicDists.forEach(function (sonicDist, index) {
      var el = sonicDistLabels[index];
      if (sonicDist) {
        text(el, sonicDist + ' cm');
      }
    });
    sonicTimes.forEach(function (sonicTime, index) {
      var el = sonicTimeLabels[index];
      if (sonicTime) {
        text(el, toFriendlyTime(sonicTime));
      }
    });
    qrCodes.forEach(function (qr) {
      text(qr.timeTd, toFriendlyTime(qr.time));
    });
    window.requestAnimationFrame(refresh);
  };

  window.requestAnimationFrame(refresh);

  var send = function (type, value) {
    ws.send(JSON.stringify({
      'type': type,
      'value': value
    }));
  };

  window.servo = function (fl) {
   send('servo', fl);
  };

  var sr = document.getElementById('servo-range');
  var mc = document.getElementById('motor-checkbox');
  sr.addEventListener('change', function () {
    send('servo', parseFloat(sr.value));
  });
  mc.addEventListener('click', function () {
    send('switch', mc.checked);
  });
  Array.prototype.slice.call(document.getElementsByClassName('servo-action')).forEach(function (sa) {
    var ac = sa.getAttribute('name');
    sa.addEventListener('click', function () {
      send('turning', ac);
    });
  });

};
