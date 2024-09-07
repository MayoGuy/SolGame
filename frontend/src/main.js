import './style.css'
import { io } from 'socket.io-client'

import Phaser from 'phaser'

const config = {
    type: Phaser.WEBGL,
    width: window.innerWidth,
    height: window.innerHeight-100,
    canvas: gameCanvas,
}

const socket = io("http://localhost:3000")

socket.on("connect", () => {
    console.log("connected")
})


socket.on("create_game", () => {
    
})

const game = new Phaser.Game(config)