import { useEffect, useRef } from 'react';

const useWebSocket = (url, onMessage, start) => {
  const socketRef = useRef(null);

  useEffect(() => {
    if (!start) return;

    const socket = new WebSocket(url);
    socketRef.current = socket;

    socket.onopen = () => {
      console.log("WebSocket connection established");
      socket.send(JSON.stringify({ message: 'ping' })); // 仅发送一次 ping 消息
    };

    socket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      onMessage(data);
    };

    socket.onerror = (error) => {
      console.error('WebSocket Error: ', error);
    };

    socket.onclose = (e) => {
      console.error('WebSocket closed unexpectedly');
    };

    return () => {
      console.log("WebSocket connection closed");
      socket.close();
    };
  }, [url, start]);

  return socketRef.current;
};

export default useWebSocket;
