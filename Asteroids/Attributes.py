class Attributes:
    class Game:
        class Window:

            def __init__(self, size):
                self.size = size
                self.center = (size[0] / 2, size[1] / 2)
                self.minX = -size[0] / 2
                self.maxX = size[0] / 2
                self.minY = -size[1] / 2
                self.maxY = size[1] / 2

        def __init__(self, attributes):
            self.tick_rate = attributes.tick_rate
            self.resolution = attributes.resolution
            self.window = Attributes.Game.Window(self.resolution)

    class Menus:
        def __init__(self, attributes):
            self.text_color = attributes.text_color

    class Asteroid:
        def __init__(self, attributes):
            self.min_size = attributes.min_size
            self.max_size = attributes.max_size
            self.max_spawned = attributes.max_spawned
            self.spawn_delay = attributes.spawn_delay
            self.last_spawned = attributes.spawn_delay
            self.max_break_cluster = attributes.max_break_cluster
            self.spread_angle = attributes.spread_angle
            self.color = attributes.color

    class Ship:
        def __init__(self, attributes):
            self.size = attributes.size
            self.speed = attributes.speed
            self.rotation_modifier = attributes.rotation_modifier
            self.max_missiles = attributes.max_missiles
            self.color = attributes.color

    class Missile:
        def __init__(self, attributes):
            self.size = attributes.size
            self.tick_life = attributes.tick_life

    def __init__(self, attributes):
        self.game = Attributes.Game(attributes.Game)
        self.menus = Attributes.Menus(attributes.Menus)
        self.asteroid = Attributes.Asteroid(attributes.Asteroid)
        self.ship = Attributes.Ship(attributes.Ship)
        self.missile = Attributes.Missile(attributes.Missile)


class Defaults:
    class Game:
        tick_rate = 120
        resolution = (500, 500)

    class Menus:
        text_color = (0, 255, 0)

    class Asteroid:
        min_size = 10
        max_size = 50
        max_spawned = 20
        spawn_delay = 120
        max_break_cluster = 5
        spread_angle = 180

        color = (255, 255, 255)

    class Ship:
        size = 15
        speed = 1
        rotation_modifier = 2
        max_missiles = 10

        color = (0, 255, 0)

    class Missile:
        size = 5
        tick_life = 120 * 2  # Defaults.Game.tick_rate * 2
