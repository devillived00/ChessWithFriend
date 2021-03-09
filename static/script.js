$(document).ready(function() {

    var socket = io.connect('http://127.0.0.1:5000/play');

    $('#move2').on('click', function(){
        var moved = 'Player has moved';

        socket.emit('move', moved)
    });

    socket.on('from flask', function(){
        $("#board").load(location.href + " #board>*","");
        $("#turn").load(location.href + " #turn>*","");
    });
});

