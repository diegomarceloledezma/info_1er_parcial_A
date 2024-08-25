import math
import logging
import arcade
import pymunk

from game_object import Bird, Column, Pig, YellowBird, BlueBird, Beam
from game_logic import get_impulse_vector, Point2D, get_distance

logging.basicConfig(level=logging.DEBUG)
logging.getLogger("arcade").setLevel(logging.WARNING)
logging.getLogger("pymunk").setLevel(logging.WARNING)
logging.getLogger("PIL").setLevel(logging.WARNING)

logger = logging.getLogger("main")

WIDTH = 1800
HEIGHT = 800
TITLE = "Angry Birds"
GRAVITY = -900


class LevelManager:
    def __init__(self, space: pymunk.Space, sprites: arcade.SpriteList, world: arcade.SpriteList, bird: arcade.SpriteList):
        self.space = space
        self.sprites = sprites
        self.world = world
        self.bird = bird
        self.current_level = 0
        self.levels = [
            self.level_1,
            self.level_2,
            self.level_3,
        ]
        self.pig_count = 0

    def load_level(self):
        self.clear_level()
        self.current_level += 1
        if self.current_level <= len(self.levels):
            self.levels[self.current_level - 1]()
            logger.info(f"Estas en el nivel: {self.current_level}")
        else:
            arcade.exit()  
            logger.info("Game Over!!!")

    def clear_level(self):
        for obj in self.world:
            obj.remove_from_sprite_lists()
            self.space.remove(obj.shape, obj.body)
        for obj in self.bird:
            obj.remove_from_sprite_lists()
            self.space.remove(obj.shape, obj.body)
        self.world.clear()
        self.sprites.clear()
        self.pig_count = 0

    def level_1(self):
        self.add_pig(WIDTH / 2 + 100, 100)
        self.add_column(WIDTH / 2 + 200, 50)
        self.add_pig(WIDTH / 2 + 300, 100)
        self.add_column(WIDTH / 2 + 400, 50)

    def level_2(self):
        self.add_column(WIDTH / 2 - 40, 50)
        self.add_column(WIDTH / 2 + 40, 50)
        self.add_column(WIDTH / 2 - 40, 150)
        self.add_column(WIDTH / 2 + 40, 150)
        self.add_column(WIDTH / 2 - 40, 250)
        self.add_column(WIDTH / 2 + 40, 250)
        self.add_column(WIDTH / 2 - 120, 50)
        self.add_column(WIDTH / 2 + 120, 50)
        self.add_column(WIDTH / 2 - 120, 150)
        self.add_column(WIDTH / 2 + 120, 150)
        self.add_column(WIDTH / 2 - 205, 50)
        self.add_column(WIDTH / 2 + 205, 50)
        self.add_beam(WIDTH / 2, 100)
        self.add_beam(WIDTH / 2, 200)
        self.add_beam(WIDTH / 2, 300)
        self.add_beam(WIDTH / 2 + 80, 200)
        self.add_beam(WIDTH / 2 - 80, 200)
        self.add_beam(WIDTH / 2 - 80, 100)
        self.add_beam(WIDTH / 2 + 80, 100)
        self.add_beam(WIDTH / 2 - 160, 100)
        self.add_beam(WIDTH / 2 + 160, 100)        
        self.add_pig(WIDTH / 2, 120)
        self.add_pig(WIDTH / 2 + 80, 50)
        self.add_pig(WIDTH / 2 - 80, 50)
        self.add_pig(WIDTH / 2, 250)
        self.add_pig(WIDTH / 2 - 160, 170)
        self.add_pig(WIDTH / 2 + 160, 170)


    def level_3(self):
        self.add_column(WIDTH / 2 - 40, 50)
        self.add_column(WIDTH / 2 + 40, 50)
        self.add_column(WIDTH / 2 - 40, 150)
        self.add_column(WIDTH / 2 + 40, 150)
        self.add_column(WIDTH / 2 - 120, 50)
        self.add_column(WIDTH / 2 + 120, 50)
        self.add_beam(WIDTH / 2, 100)
        self.add_beam(WIDTH / 2, 200)
        self.add_beam(WIDTH / 2 - 80, 100)
        self.add_beam(WIDTH / 2 + 80, 100)        
        self.add_pig(WIDTH / 2, 120)
        self.add_pig(WIDTH / 2 + 80, 50)
        self.add_pig(WIDTH / 2 - 80, 50)

        self.add_column(WIDTH / 2 + 595, 50)
        self.add_column(WIDTH / 2 + 520, 50)
        self.add_beam(WIDTH / 2 + 560, 100)
        self.add_column(WIDTH / 2 + 592, 150)
        self.add_column(WIDTH / 2 + 525, 153)
        self.add_beam(WIDTH / 2 + 560, 200)
        self.add_column(WIDTH / 2 + 595, 250)
        self.add_column(WIDTH / 2 + 525, 250)
        self.add_beam(WIDTH / 2 + 560, 300)
        self.add_pig(WIDTH / 2 + 555, 130)
        self.add_pig(WIDTH / 2 + 555, 50)
        self.add_pig(WIDTH / 2 + 555, 220)
        self.add_pig(WIDTH / 2 + 555, 340)

    def add_pig(self, x, y):
        pig = Pig(x, y, self.space)
        self.sprites.append(pig)
        self.world.append(pig)
        self.pig_count += 1

    def add_column(self, x, y):
        column = Column(x, y, self.space)
        self.sprites.append(column)
        self.world.append(column)

    def add_beam(self, x, y):
        beam = Beam(x, y, self.space)
        self.sprites.append(beam)
        self.world.append(beam)

    def pig_destroyed(self):
        self.pig_count -= 1
        logger.info(f"La cantidad de cerdos que quedan son: {self.pig_count}")
        if self.pig_count <= 0:
            self.load_level()


class App(arcade.Window):
    def __init__(self):
        super().__init__(WIDTH, HEIGHT, TITLE)
        self.background = arcade.load_texture("assets/img/background3.png")
        self.space = pymunk.Space()
        self.space.gravity = (0, GRAVITY)

        floor_body = pymunk.Body(body_type=pymunk.Body.STATIC)
        floor_shape = pymunk.Segment(floor_body, [0, 15], [WIDTH, 15], 0.0)
        floor_shape.friction = 10
        self.space.add(floor_body, floor_shape)

        self.sprites = arcade.SpriteList()
        self.birds = arcade.SpriteList()
        self.world = arcade.SpriteList()

        self.level_manager = LevelManager(self.space, self.sprites, self.world, self.birds)
        self.level_manager.load_level()

        self.start_point = Point2D()
        self.end_point = Point2D()
        self.distance = 0
        self.draw_line = False

        self.handler = self.space.add_default_collision_handler()
        self.handler.post_solve = self.collision_handler

        self.selected_bird = "Red"

    def collision_handler(self, arbiter, space, data):
        impulse_norm = arbiter.total_impulse.length
        if impulse_norm < 100:
            return True
        if impulse_norm > 1200:
            for obj in self.world:
                if obj.shape in arbiter.shapes:
                    obj.remove_from_sprite_lists()
                    self.space.remove(obj.shape, obj.body)
                    if isinstance(obj, Pig):
                        self.level_manager.pig_destroyed()
        return True

    def on_update(self, delta_time: float):
        self.space.step(1 / 60.0)
        self.sprites.update()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.KEY_1:
            self.selected_bird = "Yellow"
            logger.debug("Yellow Bird selecionado!")
        elif key == arcade.key.KEY_2:
            self.selected_bird = "Red"
            logger.debug("Red Bird selecionado!")
        elif key == arcade.key.KEY_3:
            self.selected_bird = "Blue"
            logger.debug("Blue Bird selecionado!")

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.start_point = Point2D(x, y)
            self.end_point = Point2D(x, y)
            self.draw_line = True
        elif button == arcade.MOUSE_BUTTON_RIGHT:
            for bird in self.birds:
                if hasattr(bird, 'on_click'): 
                    bird.on_click()

    def on_mouse_drag(self, x: int, y: int, dx: int, dy: int, buttons: int, modifiers: int):
        if buttons == arcade.MOUSE_BUTTON_LEFT:
            self.end_point = Point2D(x, y)
            

    def on_mouse_release(self, x: int, y: int, button: int, modifiers: int):
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.draw_line = False
            impulse_vector = get_impulse_vector(self.start_point, self.end_point)

            end_x, end_y = self.end_point.x, self.end_point.y

            if self.selected_bird == "Yellow":
                bird = YellowBird("assets/img/chuck.png", impulse_vector, end_x, end_y, self.space)
            elif self.selected_bird == "Blue":
                bird = BlueBird("assets/img/blue.png", impulse_vector, end_x, end_y, self.space, self.sprites, self.birds)
            else:
                bird = Bird("assets/img/red-bird3.png", impulse_vector, end_x, end_y, self.space)

            self.sprites.append(bird)
            self.birds.append(bird)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(0, 0, WIDTH, HEIGHT, self.background)
        self.sprites.draw()
        if self.draw_line:
            max_distance = 100
            distance = math.sqrt((self.end_point.x - self.start_point.x) ** 2 + (self.end_point.y - self.start_point.y) ** 2)

            if distance > max_distance:
                angle = math.atan2(self.end_point.y - self.start_point.y, self.end_point.x - self.start_point.x)
                self.end_point.x = self.start_point.x + max_distance * math.cos(angle)
                self.end_point.y = self.start_point.y + max_distance * math.sin(angle)

            arcade.draw_line(self.start_point.x, self.start_point.y, self.end_point.x, self.end_point.y, arcade.color.BLACK, 3)


def main():
    app = App()
    arcade.run()


if __name__ == "__main__":
    main()