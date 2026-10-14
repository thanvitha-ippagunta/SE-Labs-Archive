"""Main game state and update logic for Breakout."""

import pygame

from game.ball import Ball
from game.brick import Brick, NORMAL, STRONG, UNBREAKABLE
from game.collision import handle_ball_brick_collision
from game.paddle import Paddle
from game.renderer import HEIGHT, WIDTH

BRICK_ROWS = 4
BRICK_COLS = 8
BRICK_WIDTH = 68
BRICK_HEIGHT = 22
BRICK_GAP = 6
BRICK_TOP_MARGIN = 50

STARTING_LIVES = 3
BASE_BRICK_SCORE = 100


class GameEngine:
    """Owns game objects, score, lives, combo, and game state."""

    def __init__(self):
        self.restart_game()

    def _build_bricks(self):
        """Create a board containing normal, strong, and unbreakable bricks."""
        bricks = []
        total_width = BRICK_COLS * (BRICK_WIDTH + BRICK_GAP) - BRICK_GAP
        start_x = (WIDTH - total_width) / 2

        for row in range(BRICK_ROWS):
            for col in range(BRICK_COLS):
                x = start_x + col * (BRICK_WIDTH + BRICK_GAP)
                y = BRICK_TOP_MARGIN + row * (BRICK_HEIGHT + BRICK_GAP)

                # A simple predictable pattern makes all three types easy to test.
                if row == 0 and col % 3 == 0:
                    brick_type = UNBREAKABLE
                elif row in (0, 1) or (row == 2 and col % 3 == 1):
                    brick_type = STRONG
                else:
                    brick_type = NORMAL

                bricks.append(Brick(x, y, BRICK_WIDTH, BRICK_HEIGHT, brick_type))

        return bricks

    def _reset_ball(self):
        self.ball = Ball(x=WIDTH / 2, y=HEIGHT - 50)

    def _reset_paddle(self):
        self.paddle = Paddle(x=WIDTH / 2, y=HEIGHT - 30)

    def _breakable_bricks_left(self):
        return sum(1 for brick in self.bricks if brick.breakable)

    def restart_game(self):
        """Restore all state for a fresh three-life game."""
        self._reset_paddle()
        self._reset_ball()
        self.bricks = self._build_bricks()
        self.lives = STARTING_LIVES
        self.score = 0
        self.combo = 1
        self.game_over = False
        self.won = False

    def handle_input(self, keys_pressed):
        if self.game_over or self.won:
            return

        dx = 0
        if keys_pressed[pygame.K_LEFT]:
            dx -= self.paddle.speed
        if keys_pressed[pygame.K_RIGHT]:
            dx += self.paddle.speed
        self.paddle.move(dx, WIDTH)

    def handle_keydown(self, key):
        if key == pygame.K_r and (self.game_over or self.won):
            self.restart_game()

    def update(self):
        if self.game_over or self.won:
            return

        self.ball.update()
        self.ball.bounce_off_walls(WIDTH)

        if self.ball.get_rect().colliderect(self.paddle.get_rect()) and self.ball.vy > 0:
            self.ball.bounce_off_paddle(self.paddle.get_rect())

        for brick in self.bricks[:]:
            if handle_ball_brick_collision(self.ball, brick):
                destroyed = brick.hit()

                if destroyed:
                    self.bricks.remove(brick)
                    self.score += BASE_BRICK_SCORE * self.combo
                    self.combo += 1
                break

        if self._breakable_bricks_left() == 0:
            self.won = True
            return

        if self.ball.is_below(HEIGHT):
            self.lives -= 1
            self.combo = 1

            if self.lives <= 0:
                self.game_over = True
            else:
                self._reset_ball()

    def draw(self, surface, font):
        from game import renderer

        renderer.draw_scene(surface, self.paddle, self.ball, self.bricks)
        renderer.draw_text(
            surface,
            font,
            f"Bricks left: {self._breakable_bricks_left()}",
            (10, 10),
        )
        renderer.draw_text(surface, font, f"Lives: {self.lives}", (250, 10))
        renderer.draw_text(surface, font, f"Score: {self.score}", (380, 10))
        renderer.draw_text(surface, font, f"Combo: x{self.combo}", (520, 10))

        if self.game_over:
            renderer.draw_banner(surface, font, "GAME OVER - Press R to restart")
        elif self.won:
            renderer.draw_banner(surface, font, "YOU WIN! - Press R to restart")
