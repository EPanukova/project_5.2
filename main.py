import pygame                                   # dedline 27.09.20 23:59:59
from random import random
from math import sqrt


SCREEN_SIZE = (1280, 720)


class Vector:
    """Class vector"""

    def __init__(self, x, y=None):
        """Initialization method"""
        if y is None:
            self.x = x[0]
            self.y = x[1]
        elif y is not None:
            self.x = x
            self.y = y

    def __sub__(self, other):
        """Vector difference"""
        return Vector(self.x - other.x, self.y - other.y)

    def __add__(self, other):
        """Sum of vectors"""
        return Vector(self.x + other.x, self.y + other.y)

    def len(self):
        """Return vector length"""
        return int(sqrt((self.x * self.x + self.y * self.y)))

    def __mul__(self, other):
        """Return multiplication by scalar and scalar product"""
        if isinstance(other, Vector):
            return int(self.x * other.x + self.y * other.y)
        return Vector(self.x * other, self.y * other)

    def int_pair(self):
        """Return int pair - point"""
        return (int(self.x), int(self.y))


class Line:
    """Class line"""

    coefficient = 1

    def __init__(self):
        """Initialization method """
        self.all_speeds = []
        self.all_points = []


    def set_points(self):
        """Recalculation of point coordinates"""
        for point in range(len(self.all_points)):

            self.all_points[point].y += self.all_speeds[point].y
            self.all_points[point].x += self.all_speeds[point].x

            if self.all_points[point].x > SCREEN_SIZE[0] or self.all_points[point].x < 0:
                self.all_speeds[point] = Vector(- self.all_speeds[point].x, self.all_speeds[point].y)
            if self.all_points[point].y > SCREEN_SIZE[1] or self.all_points[point].y < 0:
                self.all_speeds[point] = Vector(self.all_speeds[point].x, -self.all_speeds[point].y)

    def add_point(self, point, speed):
        """Adding to a line dot"""
        self.all_points.append(point)
        self.all_speeds.append(speed * self.coefficient)

    def draw_points(self, points, width=4, color=(10, 25, 255)):
        """Drawing a points method"""
        for point in points:
            pygame.draw.circle(gameDisplay, color, point.int_pair(), width)
        for point_number in range(-1, len(points) - 1):
            pygame.draw.line(gameDisplay, color, (int(points[point_number].x), int(points[point_number].y)),
                             (int(points[point_number + 1].x), int(points[point_number + 1].y)), width)


class Joint(Line):
    """Class Joint"""

    def __init__(self, count):
        """Initialization method"""
        super().__init__()
        self.count = count

    def set_points(self):
        """Set point method from Line"""
        super().set_points()
        self.get_joint()

    def add_point(self, point, speed):
        """Add point method from Line"""
        super().add_point(point, speed)
        self.get_joint()

    def get_point(self, points, alpha, deg=None):
        """Get point method"""
        if deg is None:
            deg = len(points) - 1
        if deg == 0:
            return points[0]

        return points[deg]*alpha + self.get_point(points, alpha, deg - 1) * (1 - alpha)

    def get_joint(self):
        """Calculate points on the curve by adding points"""

        result = []

        if len(self.all_points) < 3:
            return []

        for i in range(-2, len(self.all_points) - 2):
            pnt = []
            pnt.append(((self.all_points[i], self.all_points[i + 1]), 0.5))
            pnt.append(self.all_points[i + 1])
            pnt.append(((self.all_points[i + 1], self.all_points[i + 2]), 0.5))
            result.extend(self.get_points(pnt))

        return result

    def draw_points(self, points, width=4, color=(255, 255, 255)):
        """Drawing a lines method"""
        for point_number in range(-1, len(points) - 1):
            pygame.draw.line(gameDisplay, color, (int(points[point_number].x), int(points[point_number].y)),
                             (int(points[point_number + 1].x), int(points[point_number + 1].y)), width)

    def get_points(self, points):
        """Get points method, counter"""
        alpha = 1 / self.count
        result = []
        for i in range(self.count):
            result.append(self.get_point(points, i * alpha))

        return result


def display_help():
    """Help display function"""

    gameDisplay.fill((50, 50, 50))
    font1 = pygame.font.SysFont("arial", 30)
    font2 = pygame.font.SysFont("serif", 30)
    data = []
    data.append(["F1", "Помощь"])
    data.append(["R", "Перезапуск"])
    data.append(["P", "Воспроизвести / Пауза"])
    data.append(["Num+", "Добавить точку"])
    data.append(["Num-", "Удалить точку"])
    data.append(["F6", "Ускорение"])
    data.append(["F5", "Замедление"])
    data.append(["", ""])
    data.append([str(steps), "текущих точек"])

    pygame.draw.lines(gameDisplay, (255, 50, 50, 255), True, [
                      (0, 0), (800, 0), (800, 600), (0, 600)], 5)
    for item, text in enumerate(data):
        gameDisplay.blit(font1.render(
            text[0], True, (128, 128, 255)), (100, 100 + 30 * item))
        gameDisplay.blit(font2.render(
            text[1], True, (128, 128, 255)), (200, 100 + 30 * item))


if __name__ == "__main__":

    pygame.init()
    gameDisplay = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("Screen Saver")

    steps = 20
    working = True
    line_points = Line()
    line_speeds = Joint(steps)
    show_help = False
    pause = False

    color_param = 0
    color = pygame.Color(0)

    while working:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                working = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    working = False
                if event.key == pygame.K_r:
                    line_points = Line()
                    line_speeds = Joint(steps)
                if event.key == pygame.K_p:
                    pause = not pause
                if event.key == pygame.K_KP_PLUS:
                    steps += 1
                if event.key == pygame.K_F1:
                    show_help = not show_help
                if event.key == pygame.K_KP_MINUS:
                    steps -= 1 if steps > 1 else 0
                if event.key == pygame.K_F5:
                    Line.coefficient -= 0.1
                if event.key == pygame.K_F6:
                    Line.coefficient += 0.1

            if event.type == pygame.MOUSEBUTTONDOWN:
                line_points.add_point(Vector(event.pos), Vector(random() * 2, random() * 2))

        gameDisplay.fill((0, 0, 0))
        color_param = (color_param + 1) % 360
        color.hsla = (color_param, 100, 50, 100)

        line_points.draw_points(line_points.all_points)
        line_speeds.draw_points(line_speeds.get_joint(), 4, color)

        if not pause:
            line_points.set_points()
            line_speeds.set_points()
        if show_help:
            display_help()

        pygame.display.flip()

    pygame.display.quit()
    pygame.quit()
    exit(0)


