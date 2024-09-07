import Phaser from "phaser";



class GameScene extends Phaser.Scene {
    constructor() {
        super("GameScene");

    }

    preload() {
        this.load.image("island", "assets/island.png");
    }

    create() {
        this.add.image(400, 300, "island");
    }

    update() {}
}