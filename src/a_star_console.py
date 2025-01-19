import math

PATH_TO_GRID_FILE = "grid.txt"


class Astar:
    """klasa Astar, wyszukuje najkrotsza droge w gridzie przy uzyciu algorytmu A*"""

    def __init__(self) -> None:
        self.open_list = []
        self.closed_list = set()
        # slownik gdzie kluczami sa obecne punkty,
        # a wartosciami punkt z ktorego dotarlismy do tego punktu
        self.path_map = {}
        self.start = (
            0,
            19,
        )  # Start, zadeklarowany na sztywno, gdyz zawsze bedzie to punkt w lewym dolnym rogu
        self.end = (19, 0)  # Koniec, tak samo na sztywno, zawsze bedzie to lewy dolny
        self.rows = 20
        self.cols = 20
        # kazal Pan dodac funkcjonalnosc, ze robot moze skruszyc sciany i przez nie przejsc
        # wobec tego zaznaczenie w gridzie czegos jako 4 sprawia ze ta sciana jest mozliwa
        # do skruszenia
        self.crushed_walls = 0
        self.grid = self.get_grid()
        self.get_path()
        self.print_path()
        if self.crushed_walls > 0:
            print(f"crushed walls: {self.crushed_walls}")

    def get_path(self) -> None:
        """znajdz sciezke"""
        self.g_costs = {self.start: 0}
        self.f_costs = {self.start: self.heuristic(self.start, self.end)}

        # dodaj start do listy otwartej
        self.open_list.append((self.f_costs[self.start], self.start))

        while self.open_list:
            # znajdz komorke z najnizszym kosztem
            current = self.get_lowest_cost_point()

            if current == self.end:
                # tutaj recznie musialem dodac uzupelnianie sciezki dla ostatniego punktu, inaczej nie zaznacza ostatniego
                i, j = self.start
                self.grid[i][j] = 3
                self.reconstruct_path()
                return

            self.open_list.remove((self.f_costs[current], current))
            self.closed_list.add(current)

            neighbors = self.get_neighbors(current)
            for neighbor in neighbors:
                # jezeli sasiad na liscie zamknietej albo = 5 (sciezka zablokowana) przejdz do kolejnego
                if (
                    neighbor in self.closed_list
                    or self.grid[neighbor[0]][neighbor[1]] == 5
                ):
                    continue
                # sprawdzenie kosztu dotarcia do sasiada
                # dodajemy 1, gdyz koszt pojedynczego ruchu to 1
                checked_g_cost = self.g_costs[current] + 1
                if (
                    neighbor not in self.g_costs
                    or checked_g_cost < self.g_costs[neighbor]
                ):
                    # aktualizacja kosztow
                    self.path_map[neighbor] = current
                    self.g_costs[neighbor] = checked_g_cost
                    self.f_costs[neighbor] = checked_g_cost + self.heuristic(
                        neighbor, self.end
                    )

                    # dodanie sasiada do listy otwartej jesli go tam nie ma
                    if neighbor not in [x[1] for x in self.open_list]:
                        self.open_list.append((self.f_costs[neighbor], neighbor))

    def get_lowest_cost_point(self) -> tuple[int, int]:
        """zwraca wspolrzedne elementu o najnizszym koszcie"""
        lowest_cost = min(self.open_list, key=lambda x: x[0])
        return lowest_cost[1]

    def reconstruct_path(self) -> None:
        """stworz sciezke"""
        current = self.end
        while current != self.start:
            self.check_if_crushable_wall(current)
            self.grid[current[0]][current[1]] = 3
            current = self.path_map[current]

    def heuristic(self, a: tuple[int, int], b: tuple[int, int]) -> float:
        """heurystyka"""
        return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)

    def get_neighbors(self, current: dict) -> list:
        # w tej funkcji musialem odpowiednio ustawic kierunki,
        # aby funkcja nadawala priorytet poruszaniu sie najpierw w prawo, pozniej w gore
        row, col = current
        neighbors = []

        # w prawo
        if col < self.cols - 1:
            neighbors.append((row, col + 1))

        # w gore
        if row > 0:
            neighbors.append((row - 1, col))

        # w dol
        if row < self.rows - 1:
            neighbors.append((row + 1, col))

        # w lewo
        if col > 0:
            neighbors.append((row, col - 1))

        return neighbors

    def get_grid(self) -> list[list[int]]:
        """wczytaj grid"""
        grid = []
        helper = []
        with open(PATH_TO_GRID_FILE, "r") as file:
            for line in file:
                # na koncu wczytywanych linii jest znak nowej linii ktory trzeba wywalic
                line = line.strip("\n")
                row = line.split(" ")
                # tutaj rzutuje sobie wynik na inta (lepiej wyglada przy wyswietlaniu w terminalu)
                for item in row:
                    helper.append(int(item))
                grid.append(helper)
                helper = []
        return grid

    def print_path(self) -> None:
        """wyprintuj grid po znalezieniu sciezki"""
        for row in self.grid:
            print(row)

    def check_if_crushable_wall(self, current: tuple[int, int]) -> None:
        """sprawdz czy punkt zawiera sciane mozliwa do skruszenia"""
        if self.grid[current[0]][current[1]] == 4:
            print(f"wall crushed at {current[0]}, {current[1]}")
            self.crushed_walls += 1


Astar()
