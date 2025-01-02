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
    WIDTH: int = 1200
    HEIGHT: int = 800

    SPEED: float = 6.0
    DEPTH: int = 7
    BRUSH_SIZE: int = 1
    DISPLAY_FACTOR: int = 192

    layers: List[pygame.Surface]
    steps: List[Dict[str, Any]]

    angles: Dict[str, float]

    def __init__(self):
        pygame.init()

        pygame.display.set_caption("ReAnim8")

        self.active = True
        self.drawing = True

        self.color_scheme = ColorScheme.Solid

        self.time = 0.0

        self.__calculate_steps()

        self.step_index = 0

        self.step = self.steps[self.step_index]

        self.facing = Direction.North
        self.angles = {"previous": self.step["angle"], "current": self.step["angle"]}
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
                self.__draw()

            for layer in self.layers:
                self.screen.blit(layer, (0, 0))

            pygame.display.flip()

            self.time += self.clock.tick(60) / 1000.0

        pygame.quit()

    def __draw(self) -> None:
        step_complete = (
            self.step["direction"] == 1
            and self.angles["current"] > self.step["angle"] + math.pi
        ) or (
            self.step["direction"] == -1
            and self.angles["current"] < self.step["angle"] - math.pi
        )

        if step_complete:
            self.__update_step()

        position_top = pygame.Vector2(
            self.center.x - self.radius, self.center.y + self.radius
        )
        position_bottom = pygame.Vector2(
            self.center.x - self.radius, -self.center.y + self.radius
        )

        size = pygame.Vector2(2 * self.radius, 2 * self.radius)

        bounding_rect_top = pygame.Rect(
            Animator.WIDTH // 2 + position_top.x * Animator.DISPLAY_FACTOR,
            Animator.HEIGHT // 2 - position_top.y * Animator.DISPLAY_FACTOR,
            size.x * Animator.DISPLAY_FACTOR,
            size.y * Animator.DISPLAY_FACTOR,
        )

        bounding_rect_bottom = pygame.Rect(
            Animator.WIDTH // 2 + position_bottom.x * Animator.DISPLAY_FACTOR,
            Animator.HEIGHT // 2 - position_bottom.y * Animator.DISPLAY_FACTOR,
            size.x * Animator.DISPLAY_FACTOR,
            size.y * Animator.DISPLAY_FACTOR,
        )

        if self.angles["current"] >= self.angles["previous"]:
            pygame.draw.arc(
                self.layers[self.step["depth"]],
                self.__get_brush_color(),
                bounding_rect_top,
                self.angles["previous"],
                self.angles["current"],
                Animator.BRUSH_SIZE,
            )

            pygame.draw.arc(
                self.layers[self.step["depth"]],
                self.__get_brush_color(),
                bounding_rect_bottom,
                self.angles["previous"] + math.pi,
                self.angles["current"] + math.pi,
                Animator.BRUSH_SIZE,
            )
        else:
            pygame.draw.arc(
                self.layers[self.step["depth"]],
                self.__get_brush_color(),
                bounding_rect_top,
                self.angles["current"],
                self.angles["previous"],
                Animator.BRUSH_SIZE,
            )

            pygame.draw.arc(
                self.layers[self.step["depth"]],
                self.__get_brush_color(),
                bounding_rect_bottom,
                self.angles["current"] + math.pi,
                self.angles["previous"] + math.pi,
                Animator.BRUSH_SIZE,
            )

        delta = self.step["direction"] * (1 / 128) * Animator.SPEED * (1 / self.radius)

        self.angles["previous"] = self.angles["current"]
        self.angles["current"] += delta

    def __calculate_steps(self) -> None:
        self.steps = []

        for layer in range(1, Animator.DEPTH + 1, 1):
            arc_count = 2**layer // 2
            radius = 1.0 / 2 ** (layer - 1)
            angle = math.pi / 2 if layer % 2 == 0 else -math.pi / 2

            for i in range(arc_count):
                if layer == 1:
                    direction = 1
                else:
                    if layer % 2 == 0:
                        direction = 1 if i % 2 == 0 else -1
                    else:
                        direction = -1 if i % 2 == 0 else 1

                if layer % 2 == 0:
                    offset = 2.0 - radius * (1 + 2 * i)
                else:
                    offset = radius * (1 + 2 * i)

                center = pygame.Vector2(0, offset)

                step = {
                    "depth": layer,
                    "direction": direction,
                    "angle": angle,
                    "radius": radius,
                    "center": center,
                }

                self.steps.append(step)

        for layer in range(Animator.DEPTH, 0, -1):
            arc_count = 2**layer // 2
            radius = 1.0 / 2 ** (layer - 1)
            angle = -math.pi / 2 if layer % 2 == 0 else math.pi / 2

            for i in range(arc_count):
                if layer == 1:
                    direction = 1
                else:
                    if layer % 2 == 0:
                        direction = -1 if i % 2 == 0 else 1
                    else:
                        direction = 1 if i % 2 == 0 else -1

                if layer % 2 == 0:
                    offset = radius * (1 + 2 * i)
                else:
                    offset = 2.0 - radius * (1 + 2 * i)

                center = pygame.Vector2(0, offset)

                step = {
                    "depth": layer,
                    "direction": direction,
                    "angle": angle,
                    "radius": radius,
                    "center": center,
                }

                self.steps.append(step)

    def __update_step(self) -> None:
        self.step_index += 1

        if self.step_index < len(self.steps):
            self.step = self.steps[self.step_index]

            self.angles["previous"] = self.step["angle"]
            self.angles["current"] = self.step["angle"]
            self.radius = self.step["radius"]
            self.center = self.step["center"]
        else:
            self.drawing = False

    def __get_normalized_angle(self, angle: float) -> float:
        normalized_angle = (math.degrees(angle) % 360 + 360) % 360

        return normalized_angle

    def __get_brush_color(self) -> Tuple[int, int, int]:
        if self.color_scheme == ColorScheme.Solid:
            return (255, 100, 255)
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
                int((math.sin(self.time + 0 * math.pi / 3) + 1) / 2 * 255),
                int((math.sin(self.time + 2 * math.pi / 3) + 1) / 2 * 255),
                int((math.sin(self.time + 4 * math.pi / 3) + 1) / 2 * 255),
            )
        elif self.color_scheme == ColorScheme.Angle:
            hue = self.__get_normalized_angle(self.angles["current"]) / 360

            rgb_normalized = colorsys.hsv_to_rgb(hue, 1.0, 1.0)

            return tuple(int(c * 255) for c in rgb_normalized)


def main():
    animator = Animator()

    animator.run()


if __name__ == "__main__":
    main()
