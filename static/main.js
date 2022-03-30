function formatBytes(bytes, decimals = 2) {
    if (bytes === 0) return '0 Bytes';

    const k = 1024;
    const dm = decimals < 0 ? 0 : decimals;
    const sizes = ['Bytes/s', 'KBs', 'MB/s', 'GB/s'];

    const i = Math.floor(Math.log(bytes) / Math.log(k));

    return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
}


$(document).ready(function() {
      // socket
      var socket = io.connect('http://localhost:5000', namespaces=['/dashboard']);

      socket.on('connect', function() {
          console.log('Connected');
          $('#transport').text('(Connected)');
      });
      socket.on('ping_from_server', function(msg) {

          $('#latency').text(msg.data.toFixed() + 'ms');
      });

      socket.on('my_response', function(msg) {
          $('#log').append('<br>Received: ' + msg.data)
          socket.emit('join_dashboard')
      });

      socket.on('disconnect', function() {
          $('#transport').text('(disconnected)');
      });

      socket.on('dl_result', function(msg) {
          $('#dl_speed').text(formatBytes(msg.data));
      });
      socket.on('ul_result', function(msg) {
          $('#ul_speed').text(formatBytes(msg.data));
      });



      $('form#emit').submit(function(event) {
          socket.emit('start_speedtest');
          console.log('start speedtest');
          return false;
      });
})