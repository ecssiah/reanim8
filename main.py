import colorsys
from enum import Enum
import math
from typing import Tuple, Dict, List, Any

import pygame


class Direction(Enum):
    North = 0
    East = 1
    South = 2
    West = 3


class ColorScheme(Enum):
    Solid = 0
    Time = 1
    Angle = 2
    Depth = 3
    InvDepth = 4


class Animator:
    WIDTH = 1200
    HEIGHT = 800

    SPEED = 1.0
    DEPTH = 7
    BRUSH_SIZE = 1.0
    DISPLAY_FACTOR = 256

    layers: List[pygame.Surface]
    steps: List[Dict[str, Any]]

    def __init__(self):
        pygame.init()

        pygame.display.set_caption("ReAnim8")

        self.active = True
        self.drawing = True

        self.color_scheme = ColorScheme.InvDepth

        self.time = 0.0

        self.__calculate_steps()

        self.step_index = 0

        self.step = self.steps[self.step_index]

        self.facing = Direction.North
        self.angle = self.step["angle"]
        self.radius = self.step["radius"]
        self.center = self.step["center"]

        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((Animator.WIDTH, Animator.HEIGHT))

        self.layers = [pygame.Surface(self.screen.get_size())]

        for _ in range(Animator.DEPTH):
            self.layers.append(pygame.Surface(self.screen.get_size(), pygame.SRCALPHA))

        self.layers[0].fill((0, 0, 0))

    def run(self):
        while self.active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.active = False

            if self.drawing == True:
                if self.step["direction"] == 1:
                    if self.angle > self.step["angle"] + math.pi:
                        self.step_index += 1

                        if self.step_index < len(self.steps):
                            self.step = self.steps[self.step_index]

                            self.angle = self.step["angle"]
                            self.radius = self.step["radius"]
                            self.center = self.step["center"]
                        else:
                            self.drawing = False
                elif self.step["direction"] == -1:
                    if self.angle < self.step["angle"] - math.pi:
                        self.step_index += 1

                        if self.step_index < len(self.steps):
                            self.step = self.steps[self.step_index]

                            self.angle = self.step["angle"]
                            self.radius = self.step["radius"]
                            self.center = self.step["center"]
                        else:
                            self.drawing = False

                base_position = self.__get_position(
                    self.radius, self.angle, self.center
                )

                positions = {
                    # Direction.North: base_position,
                    Direction.East: base_position.rotate_rad(1 / 2 * math.pi),
                    # Direction.South: base_position.rotate_rad(2 / 2 * math.pi),
                    Direction.West: base_position.rotate_rad(3 / 2 * math.pi),
                }

                for facing, position in positions.items():
                    self.facing = facing

                    pygame.draw.circle(
                        self.layers[self.step["depth"]],
                        self.__get_brush_color(),
                        self.__to_screen(position),
                        Animator.BRUSH_SIZE,
                    )

                delta = (
                    self.step["direction"]
                    * (1 / 128)
                    * Animator.SPEED
                    * (1 / self.radius)
                )

                self.angle += delta

            for layer in self.layers:
                self.screen.blit(layer, (0, 0))

            pygame.display.flip()

            self.time += self.clock.tick(60) / 1000.0

        pygame.quit()

    def __calculate_steps(self) -> None:
        self.steps = []

        for p in range(1, Animator.DEPTH + 1, 1):
            L = 2**p // 2

            for i in range(L):
                if p == 1:
                    direction = 1
                else:
                    if p % 2 == 0:
                        if i % 2 == 0:
                            direction = 1
                        else:
                            direction = -1
                    else:
                        if i % 2 == 0:
                            direction = -1
                        else:
                            direction = 1

                angle = math.pi / 2 if p % 2 == 0 else -math.pi / 2

                radius = 1.0 / 2 ** (p - 1)

                if p % 2 == 0:
                    center = pygame.Vector2(0, 2.0 - (radius + 2 * radius * i))
                else:
                    center = pygame.Vector2(0, radius + 2 * radius * i)

                step = {
                    "depth": p,
                    "direction": direction,
                    "angle": angle,
                    "radius": radius,
                    "center": center,
                }

                self.steps.append(step)

        for p in range(Animator.DEPTH, 0, -1):
            L = 2**p // 2

            for i in range(L):
                if p == 1:
                    direction = 1
                else:
                    if p % 2 == 0:
                        if i % 2 == 0:
                            direction = -1
                        else:
                            direction = 1
                    else:
                        if i % 2 == 0:
                            direction = 1
                        else:
                            direction = -1

                angle = -math.pi / 2 if p % 2 == 0 else math.pi / 2

                radius = 1.0 / 2 ** (p - 1)

                if p % 2 == 0:
                    center = pygame.Vector2(0, radius + 2 * radius * i)
                else:
                    center = pygame.Vector2(0, 2.0 - (radius + 2 * radius * i))

                step = {
                    "depth": p,
                    "direction": direction,
                    "angle": angle,
                    "radius": radius,
                    "center": center,
                }

                self.steps.append(step)

    def __get_position(
        self, radius: float, angle: float, center: pygame.Vector2
    ) -> pygame.Vector2:
        circle_position = radius * pygame.Vector2(math.cos(angle), -math.sin(angle))

        return circle_position + pygame.Vector2(center.x, -center.y)

    def __to_screen(self, position: pygame.Vector2):
        screen_x = Animator.DISPLAY_FACTOR * position.x + Animator.WIDTH // 2
        screen_y = Animator.DISPLAY_FACTOR * position.y + Animator.HEIGHT // 2

        return (screen_x, screen_y)

    def __get_normalized_angle(self, angle: float) -> float:
        normalized_angle = (math.degrees(angle) % 360 + 360) % 360

        return normalized_angle

    def __get_brush_color(self) -> Tuple[int, int, int]:
        if self.color_scheme == ColorScheme.Solid:
            return (255, 0, 255)
        elif self.color_scheme == ColorScheme.Depth:
            return (
                25 + 230 * (self.step["depth"] / Animator.DEPTH),
                25 + 230 * (self.step["depth"] / Animator.DEPTH),
                25 + 230 * (self.step["depth"] / Animator.DEPTH),
            )
        elif self.color_scheme == ColorScheme.InvDepth:
            return (
                25 + 230 * ((Animator.DEPTH - self.step["depth"]) / Animator.DEPTH),
                25 + 230 * ((Animator.DEPTH - self.step["depth"]) / Animator.DEPTH),
                25 + 230 * ((Animator.DEPTH - self.step["depth"]) / Animator.DEPTH),
            )
        elif self.color_scheme == ColorScheme.Time:
            return (
                int((math.sin(self.time) + 1) / 2 * 255),
                int(
                    (
                        math.sin(
                            self.time + 2 * math.pi / 3,
                        )
                        + 1
                    )
                    / 2
                    * 255
                ),
                int((math.sin(self.time + 4 * math.pi / 3) + 1) / 2 * 255),
            )
        elif self.color_scheme == ColorScheme.Angle:
            match self.facing:
                case Direction.North:
                    angle = self.angle - 0 / 2 * math.pi
                case Direction.East:
                    angle = self.angle - 1 / 2 * math.pi
                case Direction.South:
                    angle = self.angle - 2 / 2 * math.pi
                case Direction.West:
                    angle = self.angle - 3 / 2 * math.pi

            hue = self.__get_normalized_angle(angle) / 360

            rgb_normalized = colorsys.hsv_to_rgb(hue, 1.0, 1.0)

            return tuple(int(c * 255) for c in rgb_normalized)


def main():
    animator = Animator()

    animator.run()


if __name__ == "__main__":
    main()
