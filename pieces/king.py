from pieces.chesspiece import ChessPiece
from coordinate import Coordinate
from piecetype import PieceType


class King(ChessPiece):
    def __init__(self, color, coord, ghost=False):
        ChessPiece.__init__(self, color, PieceType.king, coord, ghost)
        self.has_moved = False

    def can_castle(self, board):
        # if king has moved, we can't castle
        if self.has_moved:
            return (False, False)

        rooks = board.get_pieces_by_type(PieceType.rook, self.color)

        # if there aren't any rooks, we can't castle
        if len(rooks) == 0:
            return (False, False)

        rook_valid = []
        for rook in rooks:
            if not rook.has_moved:
                rook_valid.append(rook)

        # if all rooks have moved, we can't castle
        if len(rook_valid) == 0:
            return (False, False)

        # if the king is in check, we can't castle
        if board.is_king_in_check(self.color):
            return (False, False)

        queenside_check = False
        kingside_check = False
        queenside_coords = []
        kingside_coords = []

        for rook in rook_valid:
            if rook.queenside:
                queenside_check = True
                queenside_coords.append(Coordinate(self.coordinate.x-1, self.coordinate.y))
                queenside_coords.append(Coordinate(self.coordinate.x-2, self.coordinate.y))
                continue
            if rook.kingside:
                kingside_check = True
                kingside_coords.append(Coordinate(self.coordinate.x+1, self.coordinate.y))
                kingside_coords.append(Coordinate(self.coordinate.x+2, self.coordinate.y))
                continue

        queenside_valid = queenside_check
        kingside_valid = kingside_check

        if queenside_check:
            for coord in queenside_coords:
                # if any square is not empty, we can't castle on this side
                # if any square would put the king in check, we can't castle on this side
                if board.puts_king_in_check(self, coord) or board.get_piece(coord) != None:
                    queenside_valid = False
                    break

        if kingside_check:
            for coord in kingside_coords:
                # if any square is not empty, we can't castle on this side
                # if any square would put the king in check, we can't castle on this side
                if board.puts_king_in_check(self, coord) or board.get_piece(coord) != None:
                    kingside_valid = False
                    break

        return (queenside_valid, kingside_valid)

    def move(self, coord):
        super().move(coord)
        if not self.has_moved and not self._ghost:
            self.has_moved = True

    def create_ghost_piece(self):
        ghost_king = King(self.color, self.coordinate, ghost=True)
        ghost_king.has_moved = self.has_moved
        return ghost_king

    def generate_possible_moves(self, board, check_check=False):

        if check_check:
            # king cannot put a king in check
            return []

        possible_movement_coords = []

        x = self.coordinate.x
        y = self.coordinate.y

        indeterminate_coords = [
            Coordinate(x+1, y),  # right
            Coordinate(x+1, y+1),  # down right
            Coordinate(x, y+1),  # down
            Coordinate(x-1, y+1),  # down left
            Coordinate(x-1, y),  # left
            Coordinate(x-1, y-1),  # up left
            Coordinate(x, y-1),  # up
            Coordinate(x+1, y-1)  # up right
        ]

        indeterminate_coords = self.filter_invalid_coords(indeterminate_coords, board.movement_coord_validity)
        indeterminate_coords = self.filter_invalid_coords(indeterminate_coords, board.does_not_put_king_in_check)

        # castling already checks for 'check', and none of the coords are 'invalid'
        castle_side_validity = self.can_castle(board)

        if any(castle_side_validity):
            if castle_side_validity[0]:  # queenside
                indeterminate_coords.append(Coordinate(x-2, y))
            if castle_side_validity[1]:  # kingside
                indeterminate_coords.append(Coordinate(x+2, y))

        possible_movement_coords.extend(indeterminate_coords)

        return possible_movement_coords
