import './style.css'

import GameScene from './gameScene'

import Phaser from 'phaser'

const config = {
    type: Phaser.WEBGL,
    width: window.innerWidth > 1200 ? 1200 : window.innerWidth,
    height: window.innerHeight > 800? 700 : window.innerHeight-100,
    canvas: gameCanvas,
    sclae: {
        mode: Phaser.Scale.WIDTH_CONTROLS_HEIGHT,
    },
    transparent: true,
    scene: [GameScene]
}


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
})


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
})

//const game = new Phaser.Game(config)