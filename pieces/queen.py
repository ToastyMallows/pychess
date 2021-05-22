from pieces.chesspiece import ChessPiece
from coordinate import Coordinate
from piecetype import PieceType


class Queen(ChessPiece):
    def __init__(self, color, coord, ghost=False):
        ChessPiece.__init__(self, color, PieceType.queen, coord, ghost)

    def create_ghost_piece(self):
        return Queen(self.color, self.coordinate, ghost=True)

    def generate_possible_moves(self, board, check_check=False):
        possible_movement_coords = []
        indeterminate_coords = []

        def up_coord_func(coord): return Coordinate(coord.x, coord.y-1)
        def right_coord_func(coord): return Coordinate(coord.x+1, coord.y)
        def down_coord_func(coord): return Coordinate(coord.x, coord.y+1)
        def left_coord_func(coord): return Coordinate(coord.x-1, coord.y)
        def up_right_coord_func(coord): return Coordinate(coord.x+1, coord.y-1)
        def down_right_coord_func(coord): return Coordinate(coord.x+1, coord.y+1)
        def down_left_coord_func(coord): return Coordinate(coord.x-1, coord.y+1)
        def up_left_coord_func(coord): return Coordinate(coord.x-1, coord.y-1)

        indeterminate_coords.extend(self.generate_coords_while_valid(board, up_coord_func))
        indeterminate_coords.extend(self.generate_coords_while_valid(board, right_coord_func))
        indeterminate_coords.extend(self.generate_coords_while_valid(board, down_coord_func))
        indeterminate_coords.extend(self.generate_coords_while_valid(board, left_coord_func))
        indeterminate_coords.extend(self.generate_coords_while_valid(board, up_right_coord_func))
        indeterminate_coords.extend(self.generate_coords_while_valid(board, down_right_coord_func))
        indeterminate_coords.extend(self.generate_coords_while_valid(board, down_left_coord_func))
        indeterminate_coords.extend(self.generate_coords_while_valid(board, up_left_coord_func))

        indeterminate_coords = self.filter_invalid_coords(indeterminate_coords, board.movement_coord_validity)
        if not check_check:
            indeterminate_coords = self.filter_invalid_coords(indeterminate_coords, board.does_not_put_king_in_check)

        possible_movement_coords.extend(indeterminate_coords)

        return possible_movement_coords
