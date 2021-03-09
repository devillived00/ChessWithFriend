$(document).ready(function() {

    var socket_chat = io.connect('http://127.0.0.1:5000/chat');

    $('#send').on('click', function(){
        var client = 'client send a message';
        socket_chat.emit('client', client)
    });

    socket_chat.on('from client', function(){
        window.location.reload();
    });
});