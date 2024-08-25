import math
import arcade
import pymunk
from game_logic import ImpulseVector


class Bird(arcade.Sprite):
    """
    Bird class. This represents an angry bird. All the physics is handled by Pymunk,
    the init method only set some initial properties
    """
    def __init__(
        self,
        image_path: str,
        impulse_vector: ImpulseVector,
        x: float,
        y: float,
        space: pymunk.Space, 
        mass: float = 5,
        radius: float = 12,
        max_impulse: float = 100,
        power_multiplier: float = 50,
        elasticity: float = 0.8,
        friction: float = 1,
        collision_layer: int = 0,
    ):
        super().__init__(image_path, 1)
        moment = pymunk.moment_for_circle(mass, 0, radius)
        body = pymunk.Body(mass, moment)
        body.position = (x, y)

        impulse = min(max_impulse, impulse_vector.impulse) * power_multiplier
        impulse_pymunk = impulse * pymunk.Vec2d(1, 0)

        body.apply_impulse_at_local_point(impulse_pymunk.rotated(impulse_vector.angle))

        shape = pymunk.Circle(body, radius)
        shape.elasticity = elasticity
        shape.friction = friction
        shape.collision_type = collision_layer

        space.add(body, shape)

        self.body = body
        self.shape = shape

    def update(self):
        """
        Update the position of the bird sprite based on the physics body position
        """
        self.center_x = self.shape.body.position.x
        self.center_y = self.shape.body.position.y
        self.radians = self.shape.body.angle




class YellowBird(Bird):
    def __init__(self, 
                 image_path: str, 
                 impulse_vector: ImpulseVector, 
                 x: float, y: float, 
                 space: pymunk.Space, 
                 mass: float = 5, 
                 radius: float = 12, 
                 max_impulse: float = 100, 
                 power_multiplier: float = 50, 
                 elasticity: float = 0.8, 
                 friction: float = 1, 
                 collision_layer: int = 0, 
                 impulse_multiplier: float = 2
                 ):
        super().__init__(image_path, 
                         impulse_vector, 
                         x, 
                         y, 
                         space, 
                         mass, 
                         radius, 
                         max_impulse, 
                         power_multiplier, 
                         elasticity, 
                         friction, 
                         collision_layer)
        self.impulse_multiplier = impulse_multiplier
        self.has_boosted = False

    def on_click(self):
        if not self.has_boosted:
            impulse = self.impulse_multiplier * self.body.velocity.length
            impulse_vector = pymunk.Vec2d(impulse, 0).rotated(self.body.angle)
            self.body.apply_impulse_at_local_point(impulse_vector)
            self.has_boosted = True


class BlueBird(Bird):
    def __init__(self, 
                 image_path: str, 
                 impulse_vector: ImpulseVector, 
                 x: float, y: float, 
                 space: pymunk.Space, 
                 sprites_list: arcade.SpriteList,
                 birds_list: arcade.SpriteList,
                 mass: float = 5, 
                 radius: float = 12,
                 max_impulse: float = 100, 
                 power_multiplier: float = 50, 
                 elasticity: float = 0.8, 
                 friction: float = 1, 
                 collision_layer: int = 0, 
                 angle_offset: float = 30
                 ):
        super().__init__(image_path, 
                         impulse_vector, 
                         x, 
                         y, 
                         space, 
                         mass, 
                         radius, 
                         max_impulse, 
                         power_multiplier, 
                         elasticity, 
                         friction, 
                         collision_layer)
        self.angle_offset = angle_offset
        self.has_split = False
        self.sprites_list = sprites_list  
        self.birds_list = birds_list      

    def on_click(self):
        if not self.has_split:
            angles = [self.body.angle + math.radians(self.angle_offset),
                      self.body.angle,
                      self.body.angle - math.radians(self.angle_offset)]

            for angle in angles:
                velocity = self.body.velocity.rotated(angle - self.body.angle)

                new_bird = Bird(
                    self.texture.name,  
                    ImpulseVector(velocity.length, angle),
                    self.body.position.x,
                    self.body.position.y,
                    self.shape.space,
                    mass=self.shape.body.mass,
                    radius=self.shape.radius,
                    max_impulse=velocity.length,
                    power_multiplier=1,  
                    elasticity=self.shape.elasticity,
                    friction=self.shape.friction,
                    collision_layer=self.shape.collision_type
                )

                new_bird.body.velocity = velocity

                self.sprites_list.append(new_bird)
                self.birds_list.append(new_bird)

            self.remove_from_sprite_lists()
            self.shape.space.remove(self.shape, self.body)
            self.has_split = True  


class Pig(arcade.Sprite):
    def __init__(
        self,
        x: float,
        y: float,
        space: pymunk.Space,
        mass: float = 2,
        elasticity: float = 0.8,
        friction: float = 0.4,
        collision_layer: int = 0,
    ):
        super().__init__("assets/img/pig_failed.png", 0.1)
        moment = pymunk.moment_for_circle(mass, 0, self.width / 2 - 3)
        body = pymunk.Body(mass, moment)
        body.position = (x, y)
        shape = pymunk.Circle(body, self.width / 2 - 3)
        shape.elasticity = elasticity
        shape.friction = friction
        shape.collision_type = collision_layer
        space.add(body, shape)
        self.body = body
        self.shape = shape

    def update(self):
        self.center_x = self.shape.body.position.x
        self.center_y = self.shape.body.position.y
        self.radians = self.shape.body.angle


class PassiveObject(arcade.Sprite):
    """
    Passive object that can interact with other objects.
    """
    def __init__(
        self,
        image_path: str,
        x: float,
        y: float,
        space: pymunk.Space,
        mass: float = 2,
        elasticity: float = 0.8,
        friction: float = 1,
        collision_layer: int = 0,
    ):
        super().__init__(image_path, 1)

        moment = pymunk.moment_for_box(mass, (self.width, self.height))
        body = pymunk.Body(mass, moment)
        body.position = (x, y)
        shape = pymunk.Poly.create_box(body, (self.width, self.height))
        shape.elasticity = elasticity
        shape.friction = friction
        shape.collision_type = collision_layer
        space.add(body, shape)
        self.body = body
        self.shape = shape

    def update(self):
        self.center_x = self.shape.body.position.x
        self.center_y = self.shape.body.position.y
        self.radians = self.shape.body.angle


class Column(PassiveObject):
    def __init__(self, x, y, space):
        super().__init__("assets/img/column.png", x, y, space)

class Beam(PassiveObject):
    def __init__(self, x, y, space):
        super().__init__("assets/img/beam.png", x, y, space)


class StaticObject(arcade.Sprite):
    def __init__(
            self,
            image_path: str,
            x: float,
            y: float,
            space: pymunk.Space,
            mass: float = 2,
            elasticity: float = 0.8,
            friction: float = 1,
            collision_layer: int = 0,
    ):
        super().__init__(image_path, 1)