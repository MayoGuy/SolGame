import Phaser from "phaser";
import { io } from "socket.io-client";

export default class WaitingRoom extends Phaser.Scene {
  constructor() {
    super("GameScene");
    this.players = [];
    this.socket = null;
    this.color = "";
    this.username = "";
    this.inviteCode = "";
  }

  preload() {
    this.load.image("background", "/bg.png");
    this.load.image("island", "/island1.png");
  }

  create(data) {
    this.username = data.username;
    this.inviteCode = data.inviteCode;

    this.socket = io("http://localhost:3000");
    this.socket.on("connect", this.socketConnect);
    this.socket.on("create_game", this.gameCreate);
    this.socket.on("update_players", this.playerUpdate);
    this.socket.on("start_game", this.startGame);
    document.getElementById("waiting-room").classList.toggle("hidden");
  }

  socketConnect = () => {
    console.log("connected");
    if (this.inviteCode) {
      console.log(this.inviteCode);
      this.socket.emit("join_game", {
        game_id: this.inviteCode,
        player_name: this.username,
      });
    } else {
      this.socket.emit("create_game", 4);
    }
  };

  gameCreate = (data) => {
    console.log(data.game_id);
    this.inviteCode = data.game_id;
    this.socket.emit("join_game", {
      game_id: data.game_id,
      player_name: this.username,
    });
  };

  playerUpdate = (data) => {
    
    const gamelink = document.getElementById("waiting-room-gamecode");

    gamelink.innerHTML = `Game Code: ${this.inviteCode}`;
    gamelink.addEventListener("click", () => {
      navigator.clipboard.writeText(this.inviteCode);
      gamelink.innerHTML = `Copied to clipboard!`;

      setTimeout(() => {
        gamelink.innerHTML = `Game Code: ${this.inviteCode}`;
      }, 2000);
    })

    this.players = data.players;
    console.log(this.players);
    let players = [];
    for (let i = 0; i < data.players.length; i++) {
      players.push(data.players[i][0]);
    }
    const currentPlayer = data.players.find(
      (player) => player[0] === this.socket.id
    );
    const playerContainer = document.getElementById("waiting-room-players");
    playerContainer.innerHTML = ""
    this.players.forEach(player => {
      const playerElement = document.createElement("div");
      playerElement.classList.add("player-item"); 
  
      const colorImage = document.createElement("img");
      colorImage.src = `/${player[2]}.png`; 
      colorImage.alt = `/${player[2]} color`;
      colorImage.classList.add("player-color"); 
  
      const playerName = document.createElement("span");
      playerName.textContent = player[1];
      playerName.classList.add("player-name"); 
  
      playerElement.appendChild(colorImage);
      playerElement.appendChild(playerName);
  
      playerContainer.appendChild(playerElement);
  });

    //const username = currentPlayer[1];
    //const color = currentPlayer[2];

    //document.getElementById("username-display").innerHTML = username;

    //document.getElementById("pfp-display").src = `/${color}.png`;
  };

  startGame = (data) => {
    console.log(data);
  }

  update() {}
}
