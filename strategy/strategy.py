import random

class Strategy:
    def __init__(self, rows: int, cols: int, ships_dict: dict[int, int]):
        self.rows = rows
        self.cols = cols
        self.ships_dict = ships_dict
        self.enemy_board = [['?' for _ in range(cols)] for _ in range(rows)]

    def get_next_attack(self) -> tuple[int, int]:
        # 1. Zkus najít sousední políčka okolo 'H' (zásah)
        for y in range(self.rows):
            for x in range(self.cols):
                if self.enemy_board[y][x] == 'H':
                    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < self.cols and 0 <= ny < self.rows and self.enemy_board[ny][nx] == '?':
                            return nx, ny
        
        # 2. Pokud nejsou žádné aktivní zásahy, použij náhodnou strategii nebo checkerboard (střídat liché a sudé)
        for y in range(self.rows):
            for x in range(self.cols):
                if self.enemy_board[y][x] == '?' and (x + y) % 2 == 0:
                    return x, y

        # 3. Jako záloha, pokud všechny checkerboard políčka jsou prozkoumána, najdi první volné políčko
        for y in range(self.rows):
            for x in range(self.cols):
                if self.enemy_board[y][x] == '?':
                    return x, y

        raise ValueError("No valid attack spots left.")

    def register_attack(self, x: int, y: int, is_hit: bool, is_sunk: bool) -> None:
        if is_hit:
            self.enemy_board[y][x] = 'H'
        else:
            self.enemy_board[y][x] = 'M'

        if is_sunk:
            # Označ okolí potopené lodi jako neplatné (volitelně)
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.cols and 0 <= ny < self.rows and self.enemy_board[ny][nx] == '?':
                    self.enemy_board[ny][nx] = 'X'

            # Najdi, která loď byla potopena, a odeber ji
            for ship_id in list(self.ships_dict):
                if self.ships_dict[ship_id] > 0:
                    self.ships_dict[ship_id] -= 1
                    break

    def get_enemy_board(self) -> list[list[str]]:
        return self.enemy_board

    def get_remaining_ships(self) -> dict[int, int]:
        return {ship_id: count for ship_id, count in self.ships_dict.items() if count > 0}

    def all_ships_sunk(self) -> bool:
        return all(count == 0 for count in self.ships_dict.values())

