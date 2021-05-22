from pieces.chesspiece import ChessPiece
from piecetype import PieceType
from coordinate import Coordinate


class Pawn(ChessPiece):
    def __init__(self, color, coord, ghost=False):
        ChessPiece.__init__(self, color, PieceType.pawn, coord, ghost)

        self.first_move = True

    def move(self, coord):
        super().move(coord)
        if self.first_move and not self._ghost:
            self.first_move = False

    def create_ghost_piece(self):
        ghost_pawn = Pawn(self.color, self.coordinate, ghost=True)
        ghost_pawn.first_move = self.first_move
        return ghost_pawn

    def generate_possible_moves(self, board, check_check=False):
        possible_movement_coords = []
        x = self.coordinate.x
        y = self.coordinate.y
        d = self.direction
        indeterminate_coords = []

        one_space = Coordinate(x, y + d)
        two_space = Coordinate(x, y + d + d)
        left_space = Coordinate(x - 1, y + d)
        right_space = Coordinate(x + 1, y + d)

        if one_space.is_valid() and not board.is_occupied(one_space):
            indeterminate_coords.append(one_space)
        if two_space.is_valid() and not board.is_occupied(two_space) and self.first_move:
            indeterminate_coords.append(two_space)
        if left_space.is_valid() and board.is_occupied_by_opponent(left_space, self.color):
            indeterminate_coords.append(left_space)
        if right_space.is_valid() and board.is_occupied_by_opponent(right_space, self.color):
            indeterminate_coords.append(right_space)

        indeterminate_coords = self.filter_invalid_coords(indeterminate_coords, board.movement_coord_validity)
        if not check_check:
            indeterminate_coords = self.filter_invalid_coords(indeterminate_coords, board.does_not_put_king_in_check)

        possible_movement_coords.extend(indeterminate_coords)

        return possible_movement_coords
