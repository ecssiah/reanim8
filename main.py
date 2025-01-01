import colorsys
import math
from typing import Tuple

import pygame


class Phase:
    Initial = 0
    Snake = 1
    Final = 2


class Animator:
    SIZE = 800

    SPEED = 8.0
    DEPTH = 4
    BRUSH_SIZE = 1.0
    DISPLAY_FACTOR = 180

    PHASES = [
        # Phase 1
        {
            "direction": 1.0,
            "radius": 1.0,
            "center": pygame.Vector2(0, 1),
            "start": 1 / 2 * math.pi,
            "end": 3 / 2 * math.pi,
        },
        {
            "direction": -1.0,
            "radius": 1.0,
            "center": pygame.Vector2(0, -1),
            "start": 5 / 2 * math.pi,
            "end": 1 / 2 * math.pi,
        },
        {
            "direction": -1.0,
            "radius": 0.5,
            "center": pygame.Vector2(0, -0.5),
            "start": 5 / 2 * math.pi,
            "end": 3 / 2 * math.pi,
        },
        {
            "direction": 1.0,
            "radius": 0.5,
            "center": pygame.Vector2(0, -1.5),
            "start": 1 / 2 * math.pi,
            "end": 5 / 2 * math.pi,
        },
        {
            "direction": 1.0,
            "radius": 0.25,
            "center": pygame.Vector2(0, -1.25),
            "start": 1 / 2 * math.pi,
            "end": 3 / 2 * math.pi,
        },
        {
            "direction": -1.0,
            "radius": 0.25,
            "center": pygame.Vector2(0, -1.75),
            "start": 5 / 2 * math.pi,
            "end": 1 / 2 * math.pi,
        },
        # Phase 2
        {
            "direction": 1.0,
            "radius": 0.25,
            "center": pygame.Vector2(0, -1.25),
            "start": 3 / 2 * math.pi,
            "end": 5 / 2 * math.pi,
        },
        {
            "direction": -1.0,
            "radius": 0.25,
            "center": pygame.Vector2(0, -0.75),
            "start": 3 / 2 * math.pi,
            "end": 1 / 2 * math.pi,
        },
        {
            "direction": 1.0,
            "radius": 0.25,
            "center": pygame.Vector2(0, -0.25),
            "start": 3 / 2 * math.pi,
            "end": 5 / 2 * math.pi,
        },
        # Phase 3
        {
            "direction": -1.0,
            "radius": 0.50,
            "center": pygame.Vector2(0, 0.50),
            "start": 3 / 2 * math.pi,
            "end": 1 / 2 * math.pi,
        },
        {
            "direction": 1.0,
            "radius": 0.50,
            "center": pygame.Vector2(0, 1.5),
            "start": 3 / 2 * math.pi,
            "end": 5 / 2 * math.pi,
        },
        {
            "direction": 1.0,
            "radius": 0.25,
            "center": pygame.Vector2(0, 1.75),
            "start": 1 / 2 * math.pi,
            "end": 3 / 2 * math.pi,
        },
        {
            "direction": -1.0,
            "radius": 0.25,
            "center": pygame.Vector2(0, 1.25),
            "start": 5 / 2 * math.pi,
            "end": 3 / 2 * math.pi,
        },
        {
            "direction": -1.0,
            "radius": 0.25,
            "center": pygame.Vector2(0, 1.25),
            "start": 3 / 2 * math.pi,
            "end": 1 / 2 * math.pi,
        },
        {
            "direction": 1.0,
            "radius": 0.25,
            "center": pygame.Vector2(0, 1.75),
            "start": 3 / 2 * math.pi,
            "end": 5 / 2 * math.pi,
        },
        {
            "direction": 1.0,
            "radius": 0.50,
            "center": pygame.Vector2(0, 1.50),
            "start": 1 / 2 * math.pi,
            "end": 3 / 2 * math.pi,
        },
        {
            "direction": -1.0,
            "radius": 0.25,
            "center": pygame.Vector2(0, 0.75),
            "start": 5 / 2 * math.pi,
            "end": 3 / 2 * math.pi,
        },
        {
            "direction": 1.0,
            "radius": 0.25,
            "center": pygame.Vector2(0, 0.25),
            "start": 1 / 2 * math.pi,
            "end": 3 / 2 * math.pi,
        },
        # Phase 3
        {
            "direction": 1.0,
            "radius": 0.50,
            "center": pygame.Vector2(0, 0.5),
            "start": 3 / 2 * math.pi,
            "end": 5 / 2 * math.pi,
        },
        {
            "direction": 1.0,
            "radius": 0.25,
            "center": pygame.Vector2(0, 0.75),
            "start": 1 / 2 * math.pi,
            "end": 3 / 2 * math.pi,
        },
        {
            "direction": -1.0,
            "radius": 0.25,
            "center": pygame.Vector2(0, 0.25),
            "start": 5 / 2 * math.pi,
            "end": 3 / 2 * math.pi,
        },
        {
            "direction": 1.0,
            "radius": 0.25,
            "center": pygame.Vector2(0, -0.25),
            "start": 1 / 2 * math.pi,
            "end": 3 / 2 * math.pi,
        },
        {
            "direction": -1.0,
            "radius": 0.25,
            "center": pygame.Vector2(0, -0.75),
            "start": 5 / 2 * math.pi,
            "end": 3 / 2 * math.pi,
        },
        {
            "direction": -1.0,
            "radius": 0.50,
            "center": pygame.Vector2(0, -0.50),
            "start": 3 / 2 * math.pi,
            "end": 1 / 2 * math.pi,
        },
        {
            "direction": 1.0,
            "radius": 1.0,
            "center": pygame.Vector2(0, 1.0),
            "start": 3 / 2 * math.pi,
            "end": 5 / 2 * math.pi,
        },
    ]

    def __init__(self):
        pygame.init()

        pygame.display.set_caption("ReAnim8")

        self.active = True
        self.drawing = True

        self.time = 0.0

        self.phase_index = 0
        self.phase = Animator.PHASES[self.phase_index]

        self.angle = self.phase["start"]
        self.radius = self.phase["radius"]
        self.center = self.phase["center"]

        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((Animator.SIZE, Animator.SIZE))

        self.screen.fill((0, 0, 0))

    def run(self):
        while self.active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.active = False

            if self.drawing == True:
                if self.phase["direction"] == 1:
                    if self.angle > self.phase["end"]:
                        self.phase_index += 1

                        if self.phase_index < len(Animator.PHASES):
                            self.phase = Animator.PHASES[self.phase_index]

                            self.angle = self.phase["start"]
                            self.radius = self.phase["radius"]
                            self.center = self.phase["center"]
                        else:
                            self.drawing = False
                elif self.phase["direction"] == -1:
                    if self.angle < self.phase["end"]:
                        self.phase_index += 1

                        if self.phase_index < len(Animator.PHASES):
                            self.phase = Animator.PHASES[self.phase_index]

                            self.angle = self.phase["start"]
                            self.radius = self.phase["radius"]
                            self.center = self.phase["center"]
                        else:
                            self.drawing = False

                position = self.get_position(self.radius, self.angle, self.center)

                pygame.draw.circle(
                    self.screen,
                    self.get_brush_color_by_time(self.time),
                    self.to_screen(position),
                    Animator.BRUSH_SIZE,
                )

                self.angle += self.phase["direction"] * 1 / 100.0 * Animator.SPEED

            pygame.display.flip()

            self.time += self.clock.tick(60) / 1000.0

        pygame.quit()

    def get_position(
        self, radius: float, angle: float, center: pygame.Vector2
    ) -> pygame.Vector2:
        circle_position = radius * pygame.Vector2(math.cos(angle), -math.sin(angle))

        return circle_position + pygame.Vector2(center.x, -center.y)

    def to_screen(self, position: pygame.Vector2):
        screen_x = Animator.DISPLAY_FACTOR * position.x + Animator.SIZE // 2
        screen_y = Animator.DISPLAY_FACTOR * position.y + Animator.SIZE // 2

        return (screen_x, screen_y)

    def get_normalized_angle(self, angle: float) -> float:
        return (angle % 360 + 360) % 360

    def get_brush_color_by_phase(self, phase_index: int) -> Tuple[int, int, int]:
        if phase_index >= 0 and phase_index <= 5:
            return (138, 255, 245)
        elif phase_index > 5 and phase_index <= 12:
            return (156, 116, 247)
        elif phase_index > 12:
            return (247, 116, 145)

    def get_brush_color_by_angle(self, angle: float) -> Tuple[int, int, int]:
        hue = self.get_normalized_angle(angle) / 360.0

        rgb_normalized = colorsys.hsv_to_rgb(hue, 1.0, 1.0)

        return tuple(int(c * 255) for c in rgb_normalized)

    def get_brush_color_by_time(self, time: float) -> Tuple[int, int, int]:
        red = int((math.sin(time) + 1) / 2 * 255)
        green = int((math.sin(time + 2 * math.pi / 3) + 1) / 2 * 255)
        blue = int((math.sin(time + 4 * math.pi / 3) + 1) / 2 * 255)

        return red, green, blue


def main():
    animator = Animator()

    animator.run()


if __name__ == "__main__":
    main()
