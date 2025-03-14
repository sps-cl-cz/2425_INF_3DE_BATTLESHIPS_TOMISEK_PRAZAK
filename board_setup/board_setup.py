import random  # Ensure the random module is imported

class BoardSetup:
    def __init__(self, rows: int, cols: int, ships_dict: dict[int, int]):
        """
        Initializes BoardSetup.

        :param rows: Number of rows in the board.
        :param cols: Number of columns in the board.
        :param ships_dict: Dictionary mapping ship_id -> count.
                           e.g. {1: 2, 2: 1, 3: 1, ...}
        """
        self.rows = rows
        self.cols = cols
        self.ships_dict = ships_dict
        self.board = [[0 for _ in range(cols)] for _ in range(rows)]  # Initialize the board with water (0)

    def get_board(self) -> list[list[int]]:
        """
        Returns the current 2D board state.
        0 = water, 1..7 = specific ship ID.
        """
        return self.board

    def get_tile(self, x: int, y: int) -> int:
        """
        Returns the value at board coordinate (x, y).
        0 = water, or 1..7 = ship ID.
        
        Raises an IndexError if the coordinates are out of bounds.
        Note: x is column, y is row.
        """
        if not (0 <= x < self.cols and 0 <= y < self.rows):
            raise IndexError("Coordinates are out of bounds.")
        return self.board[y][x]

    def place_ships(self) -> None:
        """
        Places ships onto the board according to self.ships_dict.

        - Must ensure no overlap.
        - Must stay within board bounds.
        - Cannot place ships with touching sides (diagonals are OK).
        - If it's impossible, raise ValueError.
        """
        for ship_id, count in self.ships_dict.items():
            for _ in range(count):
                placed = False
                while not placed:
                    direction = random.choice(["horizontal", "vertical"])  # Randomly choose ship orientation
                    
                    # Try to place the ship horizontally
                    if direction == "horizontal":
                        ship_length = ship_id  # Assuming ship length is the same as its ID (you can change this)
                        x = random.randint(0, self.cols - ship_length)  # Random start column
                        y = random.randint(0, self.rows - 1)  # Random row
                        
                        # Check if the space is free and no adjacent ships
                        if all(self.board[y][x + i] == 0 for i in range(ship_length)):
                            # Check if it doesn't touch any other ship
                            if not self._touches_adjacent_cells(x, y, ship_length, "H"):
                                # Place the ship
                                for i in range(ship_length):
                                    self.board[y][x + i] = ship_id
                                placed = True
                    
                    # Try to place the ship vertically
                    elif direction == "vertical":
                        ship_length = ship_id  # Same assumption here
                        x = random.randint(0, self.cols - 1)  # Random column
                        y = random.randint(0, self.rows - ship_length)  # Random start row
                        
                        # Check if the space is free and no adjacent ships
                        if all(self.board[y + i][x] == 0 for i in range(ship_length)):
                            # Check if it doesn't touch any other ship
                            if not self._touches_adjacent_cells(x, y, ship_length, "V"):
                                # Place the ship
                                for i in range(ship_length):
                                    self.board[y + i][x] = ship_id
                                placed = True
                
                if not placed:
                    raise ValueError("Unable to place ships. No valid placement found.")
    
    def _touches_adjacent_cells(self, x: int, y: int, ship_length: int, direction: str) -> bool:
        """
        Helper function to check if the ship touches any adjacent ships.
        
        - direction is either 'H' (horizontal) or 'V' (vertical).
        - Returns True if there is a touch (side-by-side), False otherwise.
        """
        # Check around the ship's placement to ensure no adjacency
        directions = [
            (-1, 0), (1, 0), (0, -1), (0, 1),  # Left, Right, Above, Below
            (-1, -1), (1, 1), (-1, 1), (1, -1)  # Diagonals are allowed
        ]
        
        if direction == "H":
            for i in range(ship_length):
                for dx, dy in directions:
                    new_x, new_y = x + i + dx, y + dy
                    if 0 <= new_x < self.cols and 0 <= new_y < self.rows:
                        if self.board[new_y][new_x] != 0:
                            return True
        elif direction == "V":
            for i in range(ship_length):
                for dx, dy in directions:
                    new_x, new_y = x + dx, y + i + dy
                    if 0 <= new_x < self.cols and 0 <= new_y < self.rows:
                        if self.board[new_y][new_x] != 0:
                            return True
        return False

    def reset_board(self) -> None:
        """
        Resets the board back to all 0 (water).
        """
        self.board = [[0 for _ in range(self.cols)] for _ in range(self.rows)]

    def board_stats(self) -> dict:
        """
        Returns a dict with simple stats about the board:
            {
              "empty_spaces": <int>,
              "occupied_spaces": <int>
            }
        """
        empty_spaces = sum(cell == 0 for row in self.board for cell in row)
        occupied_spaces = self.rows * self.cols - empty_spaces
        return {
            "empty_spaces": empty_spaces,
            "occupied_spaces": occupied_spaces
        }
