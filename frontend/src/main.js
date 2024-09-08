import "./style.css";

import GameScene from "./gameScene";

import Phaser from "phaser";

const config = {
  type: Phaser.WEBGL,
  width: window.innerWidth > 1200 ? 1200 : window.innerWidth,
  height: window.innerHeight > 800 ? 700 : window.innerHeight - 100,
  canvas: gameCanvas,
  scale: {
    mode: Phaser.Scale.FIT,
  },
  transparent: true,
  scene: [GameScene],
};

const createButton = document.getElementById("create-game");

createButton.addEventListener("click", () => {
  const name = document.getElementById("username").value;

  if (!name) {
    alert("Please enter a username");
    return;
  }
  document.getElementById("overlay").classList.toggle("hidden");
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
  document.getElementById("overlay").classList.toggle("hidden");
  const game = new Phaser.Game(config);
  game.scene.start("GameScene", { inviteCode: code, username: name });
  changeNavbar();
});

// manipulate the navbar
function changeNavbar() {
  // display the username
  const name = document.getElementById("username").value;
  document.getElementById("username-display").innerHTML = name;

  // replace the instructions resign button
  const instructionsLink = document.getElementById("instructions");

  //create the button
  const resignButton = document.createElement("button");
  resignButton.id = "resign-button";

  instructionsLink.replaceWith(resignButton);
}