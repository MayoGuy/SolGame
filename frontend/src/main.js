import './style.css'

import Phaser from 'phaser'

const config = {
    type: Phaser.WEBGL,
    width: window.innerWidth,
    height: window.innerHeight-100,
    canvas: gameCanvas,
}


const game = new Phaser.Game(config)