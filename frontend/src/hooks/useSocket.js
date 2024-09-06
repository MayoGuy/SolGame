import { useState, useEffect } from 'react'
import io from 'socket.io-client'

const useSocket = () => {
    const [socket, setSocket] = useState(null);

    const connectSocket = (url) => {
        const newSocket = io(url);
        setSocket(newSocket);
    };


    useEffect(() => {
        return () => {
            if (socket) socket.disconnect();
        }
    }, [socket]);

    return [socket, connectSocket];
}


export default useSocket;