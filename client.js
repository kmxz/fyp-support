window.onload = function () {

  var REMOTE_HOST = window.location.hostname;

  var toFriendlyTime = function (timestampInSeconds) {
    var date = new Date(timestampInSeconds * 1000);
    var now = new Date().getTime();
    var ago = Math.round(now / 1000 - timestampInSeconds);
    return ago + ' s ago (' + date.toLocaleTimeString() + ')';
  };

  var heartBeatSpan = document.querySelector('.alert-info span');
  var lastHeartBeat = null;

  var sonicGrids = Array.prototype.slice.call(document.getElementsByClassName('grid-points'));
  var sonicPoints = sonicGrids.map(function () { return []; });
  var sonicDistLabels = Array.prototype.slice.call(document.querySelectorAll('.us-last span'));
  var sonicDists = sonicDistLabels.map(function () { return null; })
  var sonicTimeLabels = Array.prototype.slice.call(document.querySelectorAll('.us-last small'));
  var sonicTimes = sonicTimeLabels.map(function () { return null; })

  var qrTbody = document.querySelector('tbody');
  var qrCodes = [];

  // let us open a web socket
  var ws = new WebSocket('ws://' + REMOTE_HOST + ':10010/');
  ws.onmessage = function (evt) {
    console.log(evt.data);
    var msg = JSON.parse(evt.data);
    lastHeartBeat = msg.time;
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
      qrTbody.appendChild(tr);
      return {
        time: code.time,
        timeTd: timeTd
      }
    }));
  };
  ws.onclose = function () {
    alert('WebSockets connection is closed.');
  };

  var text = function (el, content) {
    el.replaceChild(document.createTextNode(content), el.firstChild);
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
    if (!window.s) {
      window.requestAnimationFrame(refresh);
    }
  };

  window.requestAnimationFrame(refresh);

  window.test = (function () {
    var qr = [];
    var us = [[],[],[]];
    var getTime = function () { return new Date().getTime() / 1000; }
    return {
      us: function (num, dist) {
        us[num - 1].push({ time: getTime(), distance: dist });
      },
      qr: function (cont) {
        qr.push({ time: getTime(), content: cont });
      },
      send: function () {
        var data = { time: getTime(), ultrasonic: us, qr: qr };
        qr = [];
        us = us.map(function () { return []; });
        var xhr = new XMLHttpRequest();
        xhr.open('POST', 'http://' + REMOTE_HOST + ':10020/');
        xhr.send(JSON.stringify(data));
      }
    };
  }());

};
