// Global variables
let spaceship;
let enemies = [];
let projectiles = [];
let enemyProjectiles = [];
let gameOver = false;

function setup() {
  createCanvas(800, 600);
  startGame();
}

function draw() {
  background(0);
  spaceship.show();
  spaceship.move();

  if (!gameOver) {
    for (let projectile of projectiles) {
      projectile.show();
      projectile.move();
      for (let i = enemies.length - 1; i >= 0; i--) {
        if (projectile.hits(enemies[i])) {
          enemies.splice(i, 1);
          projectile.destroy();
        }
      }
    }

    for (let enemyProjectile of enemyProjectiles) {
      enemyProjectile.show();
      enemyProjectile.move();
      if (enemyProjectile.hits(spaceship)) {
        console.log("Game Over");
        gameOver = true;
      }
    }

    for (let enemy of enemies) {
      enemy.show();
      enemy.move();
      if (random() < 0.001) {
        enemyProjectiles.push(new Projectile(enemy.x, enemy.y, true));
      }
    }

    projectiles = projectiles.filter(p => !p.toDelete);
    enemyProjectiles = enemyProjectiles.filter(p => !p.toDelete);
  } else {
    textSize(32);
    fill(255);
    textAlign(CENTER, CENTER);
    text("Game Over", width / 2, height / 2);
    text("Press SPACE to restart", width / 2, height / 2 + 40);
  }
}

function startGame() {
  spaceship = new Spaceship();
  enemies = [];
  projectiles = [];
  enemyProjectiles = [];
  gameOver = false;

  for (let i = 0; i < 10; i++) {
    enemies.push(new Enemy(i * 80 + 80, 60));
  }
}

function keyPressed() {
  if (gameOver && key === ' ') {
    startGame();
  } else if (!gameOver) {
    if (key === ' ') {
      let projectile = new Projectile(spaceship.x, height - 20);
      projectiles.push(projectile);
    } else if (keyCode === RIGHT_ARROW) {
      spaceship.setDir(1);
    } else if (keyCode === LEFT_ARROW) {
      spaceship.setDir(-1);
    }
  }
}

class Spaceship {
  constructor() {
    this.x = width / 2;
    this.xdir = 0;
  }

  show() {
    fill(255);
    rectMode(CENTER);
    rect(this.x, height - 20, 20, 60);
  }

  move() {
    this.x += this.xdir * 5;
  }

  setDir(dir) {
    this.xdir = dir;
  }
}

class Enemy {
  constructor(x, y) {
    this.x = x;
    this.y = y;
    this.xdir = 1;
    this.speed = 2;
    this.amplitude = 50;
    this.frequency = 0.02;
    this.offset = random(0, 100);
  }

  show() {
    fill(255, 0, 0);
    ellipse(this.x, this.y, 60, 60);
  }

  move() {
    this.x += this.xdir * this.speed;
    this.y += sin((frameCount + this.offset) * this.frequency) * this.amplitude * this.frequency;
    if (this.x > width || this.x < 0) {
      this.xdir *= -1;
      this.y += 20;
    }
  }
}

class Projectile {
  constructor(x, y, isEnemy = false) {
    this.x = x;
    this.y = y;
    this.toDelete = false;
    this.isEnemy = isEnemy;
  }

  show() {
    fill(this.isEnemy ? 255 : 0, this.isEnemy ? 0 : 255, 0);
    ellipse(this.x, this.y, 8, 8);
  }

  move() {
    this.y += this.isEnemy ? 5 : -5;
  }

  hits(target) {
    let d = dist(this.x, this.y, target.x, target.y);
    return d < 30;
  }

  destroy() {
    this.toDelete = true;
  }
}

function keyReleased() {
  if (key !== ' ') {
    spaceship.setDir(0);
  }
}