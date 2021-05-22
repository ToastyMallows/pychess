from pieces.chesspiece import ChessPiece
from coordinate import Coordinate
from piecetype import PieceType


class Rook(ChessPiece):
    def __init__(self, color, coord, ghost=False):
        ChessPiece.__init__(self, color, PieceType.rook, coord, ghost)
        self.has_moved = False
        self.queenside = coord.x == 0
        self.kingside = not self.queenside

    def move(self, coord):
        super().move(coord)
        if not self.has_moved and not self._ghost:
            self.has_moved = True

    def create_ghost_piece(self):
        ghost_rook = Rook(self.color, self.coordinate, ghost=True)
        ghost_rook.has_moved = self.has_moved
        ghost_rook.queenside = self.queenside
        ghost_rook.kingside = self.kingside
        return ghost_rook

    def generate_possible_moves(self, board, check_check=False):
        possible_movement_coords = []
        indeterminate_coords = []

        def up_coord_func(coord): return Coordinate(coord.x, coord.y-1)
        def right_coord_func(coord): return Coordinate(coord.x+1, coord.y)
        def down_coord_func(coord): return Coordinate(coord.x, coord.y+1)
        def left_coord_func(coord): return Coordinate(coord.x-1, coord.y)

        indeterminate_coords.extend(self.generate_coords_while_valid(board, up_coord_func))
        indeterminate_coords.extend(self.generate_coords_while_valid(board, right_coord_func))
        indeterminate_coords.extend(self.generate_coords_while_valid(board, down_coord_func))
        indeterminate_coords.extend(self.generate_coords_while_valid(board, left_coord_func))

        indeterminate_coords = self.filter_invalid_coords(indeterminate_coords, board.movement_coord_validity)
        if not check_check:
            indeterminate_coords = self.filter_invalid_coords(indeterminate_coords, board.does_not_put_king_in_check)

        possible_movement_coords.extend(indeterminate_coords)

        return possible_movement_coords
