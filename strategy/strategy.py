class Strategy:
    def __init__(self, rows: int, cols: int, ships_dict: dict[int, int]):
        """
        Initializes the Strategy.

        :param rows: Number of rows in the enemy board.
        :param cols: Number of columns in the enemy board.
        :param ships_dict: Dictionary mapping ship_id -> count for enemy ships.
                           e.g. {1: 2, 2: 1, 3: 1, ...}

        The enemy board is initially unknown.
        """
        self.rows = rows
        self.cols = cols
        self.ships_dict = ships_dict
        
        # Tady vytvoříme 2D seznam otazníků '?', znamenající "neznámé pole"
        self.enemy_board = [['?' for _ in range(cols)] for _ in range(rows)]

    def get_next_attack(self) -> tuple[int, int]:
        """
        Returns the next (x, y) coordinates to attack.
        x = column, y = row.
        Must be within [0 .. cols-1], [0 .. rows-1].
        Assume we will never call this function if all ships are sunk.
        """
        # V současné chvíli se může zvolit náhodná pozice pro útok
        # Pokročilejší strategie by mohly zahrnovat různé algoritmy pro určení
        # nejlepšího bodu pro útok, například podle okolí zásahů.
        # Prozatím vybíráme první nevyzkoušené místo.
        for y in range(self.rows):
            for x in range(self.cols):
                if self.enemy_board[y][x] == '?':
                    return x, y
        raise ValueError("No valid attack spots left.")  # Pokud je board celý prozkoumán

    def register_attack(self, x: int, y: int, is_hit: bool, is_sunk: bool) -> None:
        """
        Called by the main simulation AFTER each shot, informing of the result:
          - is_hit: True if it's a hit
          - is_sunk: True if this shot sank a ship

        If is_sunk == True, we should decrement the count of one ship in ships_dict (you need to find out which ID).
        You should update the enemy board appropriately too.
        """
        # Zaznamenáme výsledek útoku
        if is_hit:
            self.enemy_board[y][x] = 'H'  # H = hit
        else:
            self.enemy_board[y][x] = 'M'  # M = miss

        if is_sunk:
            # Najdeme loď, která byla potopena a snížíme její počet v ships_dict
            for ship_id in list(self.ships_dict):
                if self.ships_dict[ship_id] > 0:
                    self.ships_dict[ship_id] -= 1
                    break

    def get_enemy_board(self) -> list[list[str]]:
        """
        Returns the current 2D state (knowledge) of the enemy board.
        '?' = unknown, 'H' = hit, 'M' = miss.
        You may optionally use 'S' for sunk ships (not required).
        You may optionally use 'X' for tiles that are impossible to contain a ship (not required).
        """
        # Vrátí aktuální stav našeho "znalostního" boardu
        return self.enemy_board

    def get_remaining_ships(self) -> dict[int, int]:
        """
        Returns the dictionary of ship_id -> count for ships we believe remain afloat.
        """
        # Vrátí stav zbylých lodí
        return {ship_id: count for ship_id, count in self.ships_dict.items() if count > 0}

    def all_ships_sunk(self) -> bool:
        """
        Returns True if all enemy ships are sunk (ships_dict counts are all zero).
        """
        # Pokud jsou všechny lodě potopeny, všechny hodnoty v ships_dict budou 0
        return all(count == 0 for count in self.ships_dict.values())
