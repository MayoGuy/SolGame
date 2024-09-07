import Phaser from "phaser";



export default class GameScene extends Phaser.Scene {
    constructor() {
        super("GameScene");
    }

    preload() {
        this.load.image('background', '/bg.png');
        this.load.image('island', '/island1.png');
    }

    create() {
        const camera = this.cameras.main;
        camera.setBounds(0, 0, 1200, 600);  // Adjust as per your game world size



        const island = this.add.tileSprite(600, 400, 1200, 800, 'background');
        const island1 = this.add.sprite(200, 200, 'island').setScale(0.2);
        this.add.sprite(120, 400, 'island').setScale(0.1);
        this.add.sprite(450, 500, 'island').setScale(0.1);
        this.add.sprite(1000, 700, 'island').setScale(0.1);
        // Enable drag panning
        this.input.on('pointermove', function (pointer) {
            if (pointer.isDown) {
                camera.scrollX -= (pointer.x - pointer.prevPosition.x);
                camera.scrollY -= (pointer.y - pointer.prevPosition.y);
            }
        });
    }

    update() {}
}