import { io, Socket } from "socket.io-client";
import {
    onAddPlayerPersonal,
    onAddPlayer,
    onStart,
    onMove
} from "../services/eventHandlers";

/** @type {Socket} */
let socket = null;

export const connectSocket = (url, playerName, playerId) => {
    if (!socket) {
        socket = io(url, {
            transports: ["websocket"],
        });

        socket.on("connect", () => {
            socket.send(JSON.stringify({
                event: "initialize",
                data: {
                    player_id: playerId,
                    player_name: playerName,
                }
            }))
        })

        socket.on("message", (data) => {
            try {
                data = JSON.parse(data);
                switch (data.event) {
                    case "add_player_personal":
                        onAddPlayerPersonal(data.data);
                        break;
                    case "add_player":
                        onAddPlayer(data.data);
                        break;
                    case "start":
                        onStart();
                        break;
                    case "move":
                        onMove(data.data);
                        break;
                }
            } catch (e) {
                console.error("Failed to parse message as JSON:", e);
                return;
            }
        })
        
        console.log(`Connected to ${url}`);
    };
};


export const disconnectSocket = (url) => {
    if (socket) {
        socket.disconnect();
        console.log("Socket disconnected");
        socket = null;
    }
}




