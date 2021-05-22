from pieces.chesspiece import ChessPiece
from coordinate import Coordinate
from piecetype import PieceType


class Knight(ChessPiece):
    def __init__(self, color, coord, ghost=False):
        ChessPiece.__init__(self, color, PieceType.knight, coord, ghost)

    def create_ghost_piece(self):
        return Knight(self.color, self.coordinate, ghost=True)

    def generate_possible_moves(self, board, check_check=False):
        possible_movement_coords = []

        x = self.coordinate.x
        y = self.coordinate.y

        indeterminate_coords = [
            Coordinate(x+2, y+1),
            Coordinate(x+2, y-1),
            Coordinate(x+1, y+2),
            Coordinate(x+1, y-2),
            Coordinate(x-2, y+1),
            Coordinate(x-2, y-1),
            Coordinate(x-1, y+2),
            Coordinate(x-1, y-2)
        ]

        indeterminate_coords = self.filter_invalid_coords(indeterminate_coords, board.movement_coord_validity)
        if not check_check:
            indeterminate_coords = self.filter_invalid_coords(indeterminate_coords, board.does_not_put_king_in_check)

        possible_movement_coords.extend(indeterminate_coords)

        return possible_movement_coords
