import './style.css'
import { io } from 'socket.io-client'
import GameScene from './gameScene'

import Phaser from 'phaser'

const config = {
    type: Phaser.WEBGL,
    width: window.innerWidth > 1200 ? 1200 : window.innerWidth,
    height: window.innerHeight > 800? 700 : window.innerHeight-100,
    canvas: gameCanvas,
    scale: {
        mode: Phaser.Scale.FIT,
    },

    scene: [GameScene]
}

const socket = io("http://localhost:3000")

socket.on("connect", () => {
    console.log("connected")
})


socket.on("create_game", () => {
    
})

const game = new Phaser.Game(config)