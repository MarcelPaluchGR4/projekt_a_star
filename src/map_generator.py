from random import randint


class MapGenerator:
    """class generating map"""

    MAP_WIDTH = 20
    MAP_HEIGHT = 20
    PASSABLE_TO_UNPASSABLE_RATIO = 0.2

    def __init__(
        self, is_map_random: bool = False, is_start_random: bool = False
    ) -> None:
        self.map = self.create_map(is_map_random)
        self.set_start(is_start_random)
        for _ in self.map:
            print(_)

    def create_map(self, is_map_random: bool) -> list[list]:
        if is_map_random:
            random_map = [
                [0 for _ in range(self.MAP_WIDTH)] for _ in range(self.MAP_HEIGHT)
            ]
            total_elements = self.MAP_HEIGHT * self.MAP_WIDTH
            number_of_unpassable = int(
                total_elements * self.PASSABLE_TO_UNPASSABLE_RATIO
            )
            for _ in range(number_of_unpassable):
                random_map[randint(0, self.MAP_WIDTH - 1)][
                    randint(0, self.MAP_HEIGHT - 1)
                ] = 1
            return random_map
        return [[0 for _ in range(self.MAP_WIDTH)] for _ in range(self.MAP_HEIGHT)]

    def set_start(self, is_start_random: bool) -> None:
        if is_start_random:
            self.map[randint(0, self.MAP_WIDTH - 1)][
                randint(0, self.MAP_HEIGHT - 1)
            ] = "S"
            self.map[randint(0, self.MAP_WIDTH - 1)][
                randint(0, self.MAP_HEIGHT - 1)
            ] = "M"
            return
        self.map[-1][0] = "S"
        self.map[0][-1] = "M"


MapGenerator()
