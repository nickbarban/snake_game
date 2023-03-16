from random import randint

from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.widget import Widget


class SnakePart(Widget):
    pass


def collide_widgets(wid1, wid2):
    if wid1.right <= wid2.x:
        return False
    if wid1.x >= wid2.right:
        return False
    if wid1.top <= wid2.y:
        return False
    if wid1.y >= wid2.top:
        return False
    return True


class GameScreen(Widget):
    step_size = 40
    movement_x = 0
    movement_y = 0
    snake_parts = []

    def new_game(self):
        to_be_removed = []
        for child in self.children:
            if isinstance(child, SnakePart):
                to_be_removed.append(child)
        for child in to_be_removed:
            self.remove_widget(child)
        self.snake_parts = []
        self.movement_x = 0
        self.movement_y = 0
        head = SnakePart()
        head.pos = (0, 0)
        self.snake_parts.append(head)
        self.add_widget(head)

    def on_touch_up(self, touch):
        print("on touch up: [" + str(touch.x) + "][" + str(touch.y) + "][" + str(touch.opos[0]) + "][" + str(touch.opos[1]) + "]")
        dx = touch.x - touch.opos[0]
        dy = touch.y - touch.opos[1]
        print("dx=" + str(dx))
        print("dy=" + str(dy))
        if abs(dx) > abs(dy):
            # Move left or right
            self.movement_y = 0
            if dx > 0:
                print("Move right")
                self.movement_x = self.step_size
            else:
                print("Move left")
                self.movement_x = - self.step_size
        else:
            # Move up or down
            self.movement_x = 0
            if dy > 0:
                print("Move up")
                self.movement_y = self.step_size
            else:
                print("Move down")
                self.movement_y = - self.step_size

    def next_frame(self, *args):
        # Move the snake
        food = self.ids.food
        head = self.snake_parts[0]
        last_x = self.snake_parts[-1].x
        last_y = self.snake_parts[-1].y
        # Move the body
        for i, part in enumerate(self.snake_parts):
            if i == 0:
                continue
            else:
                part.new_x = self.snake_parts[i-1].x
                part.new_y = self.snake_parts[i-1].y
        for part in self.snake_parts[1:]:
            part.x = part.new_x
            part.y = part.new_y
        # Move the head
        head.x += self.movement_x
        head.y += self.movement_y
        # Check for snake colliding with food
        if collide_widgets(head, food):
            food.x = randint(0, Window.width - food.width)
            food.y = randint(0, Window.height - food.height)
            new_snake_part = SnakePart()
            new_snake_part.x = last_x
            new_snake_part.y = last_y
            self.snake_parts.append(new_snake_part)
            self.add_widget(new_snake_part)
        # Check for snake colliding with wall
        for part in self.snake_parts[1:]:
            if collide_widgets(part, head):
                self.new_game()
        # Check for snake colliding with snake
        if not collide_widgets(self, head):
            self.new_game()
        pass


class MainApp(App):
    def on_start(self):
        self.root.new_game()
        Clock.schedule_interval(self.root.next_frame, .5)

    pass


MainApp().run()
