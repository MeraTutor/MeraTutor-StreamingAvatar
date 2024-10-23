'use strict';

let express = require('express');
let http = require('http');
let socketIo = require('socket.io');

// NOTE Setup server
let httpServer = http.createServer(express());
let socketServer = socketIo(httpServer);
let sockets = [];
let port = 8080;

httpServer.listen(port);

// NOTE Setup socket listener

socketServer.on('connection', (socket) => {
  sockets.push(socket);

  let socketId = sockets.length;

  socket.on('img', (payload) => {
    socket.broadcast.emit('img', payload);
  });
});