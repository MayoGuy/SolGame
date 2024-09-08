import Phaser from "phaser";
import { io } from "socket.io-client";

export default class GameScene extends Phaser.Scene {
  constructor() {
    super("GameScene");
    this.players = {};
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
    const camera = this.cameras.main;
    camera.setBounds(0, 0, 1200, 600); // Adjust as per your game world size
    console.log(data.username);

    const island = this.add.tileSprite(600, 400, 2400, 1600, "background");
    const island1 = this.add.sprite(200, 200, "island").setScale(0.2);
    this.add.sprite(120, 400, "island").setScale(0.1);
    this.add.sprite(450, 500, "island").setScale(0.1);
    this.add.sprite(1000, 700, "island").setScale(0.1);

    let text = this.add.text(10, 10, data.username, {
      fontSize: "32px",
      fill: "#fff",
    });
    // Enable drag panning
    this.input.on("pointermove", function (pointer) {
      if (pointer.isDown) {
        camera.scrollX -= pointer.x - pointer.prevPosition.x;
        camera.scrollY -= pointer.y - pointer.prevPosition.y;
      }
    });
    const color = ["yellow", "red", "green", "blue"][
      Math.floor(Math.random() * 4)
    ];

    this.color = color;
    this.username = data.username;
    this.inviteCode = data.inviteCode;

    this.socket = io("http://localhost:3000");
    this.socket.on("connect", this.socketConnect);
    this.socket.on("create_game", this.gameCreate);
    this.socket.on("update_players", this.playerUpdate);
  }

  socketConnect = () => {
    console.log("connected");
    if (this.inviteCode) {
      console.log(this.inviteCode);
      this.socket.emit("join_game", {
        game_id: this.inviteCode,
        player_name: this.username,
        player_color: this.color,
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
      player_color: this.color,
    });
  };

  playerUpdate = (data) => {
    this.players = data.players;
    console.log(this.players);
    let players = [];
    for (let i = 0; i < data.players.length; i++) {
      players.push(data.players[i][0]);
    }
    // Finding the current player's username and color from their Socket ID
    const currentPlayer = data.players.find(
      (player) => player[0] === this.socket.id
    );

    const username = currentPlayer[1];
    const color = currentPlayer[2];

    // display the username
    document.getElementById("username-display").innerHTML = username;

    // display the pfp
    document.getElementById("pfp-display").src = `/${color}.png`;
  };

  update() {}
}
