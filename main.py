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
    HEIGHT: int = 900

    DEPTH: int = 6
    SPEED: float = 1.0
    SYMMETRIC: bool = True
    DELTA_FACTOR: float = 1 / 128

    WORLD_SCREEN_RATIO: int = 280

    BRUSH_SIZE: int = 1
    BRUSH_COLOR: Tuple[int, int, int] = (255, 160, 255)

    time: float

    active: bool
    drawing: bool

    color_scheme: ColorScheme

    steps: List[Dict[str, Any]]

    step_index: int
    step: Dict[str, Any]

    angle: Dict[str, float]
    radius: int
    center: pygame.Vector2

    clock: pygame.time.Clock
    screen: pygame.surface.Surface

    layers: List[pygame.Surface]

    def __init__(self):
        self.time = 0.0

        self.active = True
        self.drawing = True

        self.color_scheme = ColorScheme.Time

        self.steps = self.__calculate_steps()

        self.step_index = 0
        self.step = self.steps[self.step_index]

        self.angle = {"previous": self.step["angle"], "current": self.step["angle"]}
        self.radius = self.step["radius"]
        self.center = self.step["center"]

        pygame.init()
        pygame.display.set_caption("ReAnim8")

        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((Animator.WIDTH, Animator.HEIGHT))

        self.layers = [pygame.Surface(self.screen.get_size())]

        for _ in range(Animator.DEPTH):
            surface = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)

            self.layers.append(surface)

        self.layers[0].fill((0, 0, 0))

    def run(self):
        while self.active:
            self.__handle_events()

            if self.drawing == True:
                delta = Animator.DELTA_FACTOR * Animator.SPEED / self.radius

                self.__draw()
                self.__update_angle(delta)
                self.__update_step()

            self.__render()

            self.time += self.clock.tick(60) / 1000.0

        pygame.quit()

    def __handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.active = False
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    self.active = False

    def __draw(self) -> None:
        direction_angles = {
            Direction.North: 0 / 2 * math.pi,
            Direction.East: 1 / 2 * math.pi,
            Direction.South: 2 / 2 * math.pi,
            Direction.West: 3 / 2 * math.pi,
        }

        centers = {
            Direction.North: self.center.rotate_rad(direction_angles[Direction.North]),
            Direction.East: self.center.rotate_rad(direction_angles[Direction.East]),
            Direction.South: self.center.rotate_rad(direction_angles[Direction.South]),
            Direction.West: self.center.rotate_rad(direction_angles[Direction.West]),
        }

        bounding_rects = {
            # Direction.North: self.__get_bounding_rect(centers[Direction.North]),
            Direction.East: self.__get_bounding_rect(centers[Direction.East]),
            # Direction.South: self.__get_bounding_rect(centers[Direction.South]),
            Direction.West: self.__get_bounding_rect(centers[Direction.West]),
        }

        if self.step["direction"] == 1:
            start_angle = self.angle["previous"]
            end_angle = self.angle["current"]
        elif self.step["direction"] == -1:
            start_angle = self.angle["current"]
            end_angle = self.angle["previous"]

        layer = self.layers[self.step["depth"]]

        for direction in bounding_rects.keys():
            pygame.draw.arc(
                layer,
                self.__get_brush_color(),
                bounding_rects[direction],
                start_angle + direction_angles[direction],
                end_angle + direction_angles[direction],
                Animator.BRUSH_SIZE,
            )

    def __render(self) -> None:
        for layer in self.layers:
            self.screen.blit(layer, (0, 0))

        pygame.display.flip()

    def __calculate_steps(self) -> List[Dict[str, Any]]:
        steps = []

        for layer in range(1, Animator.DEPTH + 1):
            even_layer = layer % 2 == 0

            arc_count = 2**layer
            radius = 1 / arc_count
            angle = math.pi / 2 if even_layer else -math.pi / 2

            for arc in range(arc_count):
                even_arc = arc % 2 == 0

                offset = radius + 2 * arc * radius

                if even_layer:
                    center = pygame.Vector2(0, 2 - offset)
                    direction = -1 if even_arc else 1
                else:
                    center = pygame.Vector2(0, offset)
                    direction = 1 if even_arc else -1

                steps.append(
                    {
                        "depth": layer,
                        "direction": direction,
                        "angle": angle,
                        "radius": radius,
                        "center": center,
                    }
                )

        if Animator.SYMMETRIC == False:
            return steps

        for layer in range(Animator.DEPTH, 0, -1):
            even_layer = layer % 2 == 0

            arc_count = 2**layer
            radius = 1 / arc_count
            angle = -math.pi / 2 if even_layer else math.pi / 2

            for arc in range(arc_count):
                even_arc = arc % 2 == 0

                offset = radius + 2 * arc * radius

                if even_layer:
                    center = pygame.Vector2(0, offset)
                    direction = 1 if even_arc else -1
                else:
                    center = pygame.Vector2(0, 2 - offset)
                    direction = -1 if even_arc else 1

                steps.append(
                    {
                        "depth": layer,
                        "direction": direction,
                        "angle": angle,
                        "radius": radius,
                        "center": center,
                    }
                )

        return steps

    def __set_step(self, index: int) -> bool:
        if index < len(self.steps):
            self.step = self.steps[index]

            self.angle["previous"] = self.step["angle"]
            self.angle["current"] = self.step["angle"]
            self.radius = self.step["radius"]
            self.center = self.step["center"]

            return True
        else:
            return False

    def __update_step(self) -> None:
        step_complete = (
            self.step["direction"] == 1
            and self.angle["current"] >= self.step["angle"] + math.pi
        ) or (
            self.step["direction"] == -1
            and self.angle["current"] <= self.step["angle"] - math.pi
        )

        if step_complete:
            self.step_index += 1

            self.drawing = self.__set_step(self.step_index)

    def __update_angle(self, delta: float) -> None:
        self.angle["previous"] = self.angle["current"]

        if self.step["direction"] == 1:
            target_angle = min(
                self.angle["current"] + delta, self.step["angle"] + math.pi
            )
        elif self.step["direction"] == -1:
            target_angle = max(
                self.angle["current"] - delta, self.step["angle"] - math.pi
            )

        self.angle["current"] = target_angle

    def __get_bounding_rect(self, center: pygame.Vector2) -> pygame.Rect:
        position = center + pygame.Vector2(-self.radius, self.radius)

        bounding_rect = pygame.Rect(
            Animator.WIDTH // 2 + position.x * Animator.WORLD_SCREEN_RATIO,
            Animator.HEIGHT // 2 - position.y * Animator.WORLD_SCREEN_RATIO,
            2 * self.radius * Animator.WORLD_SCREEN_RATIO,
            2 * self.radius * Animator.WORLD_SCREEN_RATIO,
        )

        return bounding_rect

    def __get_normalized_angle(self, angle: float) -> float:
        normalized_angle = (math.degrees(angle) % 360 + 360) % 360

        return normalized_angle

    def __get_brush_color(self) -> Tuple[int, int, int]:
        if self.color_scheme == ColorScheme.Solid:
            return Animator.BRUSH_COLOR
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
            hue = self.__get_normalized_angle(self.angle["current"]) / 360

            rgb_normalized = colorsys.hsv_to_rgb(hue, 1.0, 1.0)

            return tuple(int(c * 255) for c in rgb_normalized)


def main():
    animator = Animator()

    animator.run()


if __name__ == "__main__":
    main()
