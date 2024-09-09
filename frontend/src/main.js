import "./style.css";

import WaitingRoom from "./waitingRoom";
import Phaser from "phaser";

const config = {
  type: Phaser.WEBGL,
  width:1200,
  height: 600,
  canvas: gameCanvas,
  transparent: true,
  scene: [WaitingRoom],
};

const createButton = document.getElementById("create-game");

createButton.addEventListener("click", () => {
  const name = document.getElementById("username").value;

  if (!name) {
    alert("Please enter a username");
    return;
  }
  document.getElementById("create-overlay").classList.toggle("hidden");
  const game = new Phaser.Game(config);
  game.scene.start("GameScene", { username: name });
  changeNavbar();
});

const joinButton = document.getElementById("join-game");

joinButton.addEventListener("click", () => {
  const code = document.getElementById("invite-code").value;
  if (!code) {
    alert("Please enter a invite code");
    return;
  }
  const name = document.getElementById("username").value;

  if (!name) {
    alert("Please enter a username");
    return;
  }
  document.getElementById("create-overlay").classList.toggle("hidden");
  const game = new Phaser.Game(config);
  game.scene.start("GameScene", { inviteCode: code, username: name });
  changeNavbar();
});

// manipulate the navbar
function changeNavbar() {
  // replace the instructions resign button
  const instructionsLink = document.getElementById("instructions");

  //create the button
  const resignButton = document.createElement("button");
  resignButton.id = "resign-button";

  instructionsLink.replaceWith(resignButton);
}