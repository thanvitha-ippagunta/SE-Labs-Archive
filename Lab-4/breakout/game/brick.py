"""Brick types used by the Breakout game."""

import pygame


NORMAL = "normal"
STRONG = "strong"
UNBREAKABLE = "unbreakable"

NORMAL_COLOR = (200, 90, 90)
STRONG_COLOR = (240, 170, 70)
UNBREAKABLE_COLOR = (130, 130, 145)
STRONG_DAMAGED_COLOR = (255, 215, 120)


class Brick:
    """A brick that may require one, several, or unlimited hits."""

    def __init__(self, x, y, width, height, brick_type=NORMAL):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.brick_type = brick_type

        if brick_type == NORMAL:
            self.hits_remaining = 1
            self.color = NORMAL_COLOR
        elif brick_type == STRONG:
            self.hits_remaining = 2
            self.color = STRONG_COLOR
        elif brick_type == UNBREAKABLE:
            self.hits_remaining = None
            self.color = UNBREAKABLE_COLOR
        else:
            raise ValueError(f"Unknown brick type: {brick_type}")

    @property
    def breakable(self):
        """Return True when this brick can eventually be destroyed."""
        return self.brick_type != UNBREAKABLE

    def hit(self):
        """Apply one ball hit and return True only when the brick is destroyed."""
        if not self.breakable:
            return False

        self.hits_remaining -= 1

        if self.brick_type == STRONG and self.hits_remaining == 1:
            self.color = STRONG_DAMAGED_COLOR

        return self.hits_remaining <= 0

    def get_rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.width, self.height)
