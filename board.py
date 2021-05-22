from copy import copy
from coordinate import Coordinate
from constants import WHITE, BLACK
from piecetype import PieceType


class Board():
    def __init__(self, _2darray=None):
        self.__OFF_SCREEN_COORDINATE = Coordinate(-1, -1)
        if _2darray == None:
            # initialize default board
            self.board = self.__init_board__()
            self.__board_populated = False
        else:
            self.board = _2darray
            self.__board_populated = True
        self.last_move = None

    def __init_board__(self):
        board = []
        for _ in range(8):
            row = []
            for __ in range(8):
                row.append(None)
            board.append(row)
        return board

    def populate(self, array_of_pieces):
        if self.__board_populated:
            raise Exception("board already populated")
        for piece in array_of_pieces:
            self.board[piece.coordinate.y][piece.coordinate.x] = piece
        self.__board_populated = True

    def get_piece(self, coord):
        if not self.__board_populated:
            raise Exception("board not populated")
        return self.board[coord.y][coord.x]

    def get_pieces_by_type(self, piece_type, color):
        if not self.__board_populated:
            raise Exception("board not populated")
        pieces = []
        for row in self.board:
            for piece in row:
                if piece == None:
                    continue
                if piece.piece_type == piece_type and piece.color == color:
                    pieces.append(piece)
        return pieces

    # sets a piece on the board and updates piece coords
    def set_piece(self, coord, piece):
        if not self.__board_populated:
            raise Exception("board not populated")
        self.board[coord.y][coord.x] = piece
        if piece != None:
            piece.move(coord)

    def is_occupied(self, coord):
        return self.get_piece(coord) != None

    def is_occupied_by_self(self, coord, color):
        piece = self.get_piece(coord)
        return piece != None and piece.color == color

    def is_occupied_by_opponent(self, coord, color):
        piece = self.get_piece(coord)
        return piece != None and piece.color != color

    def is_occupied_by_opponent_piecetype(self, coord, color, piece_type):
        piece = self.get_piece(coord)
        return piece != None and piece.color != color and piece.piece_type == piece_type

    def movement_coord_validity(self, piece, coord):
        return coord.is_valid() and not self.is_occupied_by_self(coord, piece.color)

    # Moves a piece and returns the killed piece that was in its place,
    # or None if there was no killed piece.
    # If a killed piece is returned, its coords are set to (-1,-1).
    def move_piece(self, new_coord, piece):
        # get killed piece and set that position to None
        killed_piece = self.get_piece(new_coord)
        if killed_piece != None:
            killed_piece.move(self.__OFF_SCREEN_COORDINATE)
        self.set_piece(new_coord, None)

        # set the piece to its new home and set the
        # old position to None
        old_coords = copy(piece.coordinate)
        self.set_piece(new_coord, piece)
        self.set_piece(old_coords, None)

        return killed_piece

    def move_for_castle(self, new_coord, king):
        queenside = (new_coord.x - king.coordinate.x) == -2

        rook = None
        if queenside:
            rook = self.get_piece(Coordinate(0, king.coordinate.y))
        else:
            rook = self.get_piece(Coordinate(7, king.coordinate.y))

        if rook == None:
            raise Exception("Couldn't find " + king.color + " Rook to castle")

        rook_end_coord = None
        if queenside:
            rook_end_coord = Coordinate(new_coord.x + 1, king.coordinate.y)
        else:
            rook_end_coord = Coordinate(new_coord.x - 1, king.coordinate.y)

        no_kill_king = self.move_piece(new_coord, king)
        no_kill_rook = self.move_piece(rook_end_coord, rook)

        if no_kill_king != None or no_kill_rook != None:
            raise Exception("Killed piece from castle movement (illegal move)")

    def move_for_en_passant(self, new_coord, pawn):
        pass

    def puts_king_in_check(self, orig_piece, new_coord):
        # make new board with all None objects

        found_piece = None
        new_pieces = []
        # create new pieces from old board
        for row in self.board:
            for piece in row:
                if piece == None:
                    continue
                new_piece = piece.create_ghost_piece()
                if orig_piece.coordinate == new_piece.coordinate:
                    if found_piece != None:
                        # already found the piece we want to move, error
                        raise Exception("found a duplicate piece when copying the board")
                    found_piece = new_piece
                new_pieces.append(new_piece)

        if found_piece == None:
            raise Exception("Original " + orig_piece.color + " " + orig_piece.piece_type + " not found")

        # TODO: combine these?
        new_board = Board()
        new_board.populate(new_pieces)

        _ = new_board.move_piece(new_coord, found_piece)

        will_king_be_in_check = new_board.is_king_in_check(orig_piece.color)

        del new_board

        return will_king_be_in_check

    def does_not_put_king_in_check(self, orig_piece, new_coord):
        return not self.puts_king_in_check(orig_piece, new_coord)

    # checks if the color passed in has its king in check
    # given the current board configuration passed in (or global board)
    def is_king_in_check(self, color):
        opponents_color = WHITE if color == BLACK else BLACK

        # get current color's king
        found_pieces = self.get_pieces_by_type(PieceType.king, color)

        if len(found_pieces) > 1 or len(found_pieces) == 0:
            raise Exception(str(len(found_pieces)) + " kings found")

        king_coords = found_pieces[0].coordinate

        # iterate through all opponent's pieces
        # and see if any of their movements intersects with the
        # current color's king
        for row in self.board:
            for piece in row:
                if piece == None:
                    continue
                if piece.color != opponents_color:
                    continue
                possible_movement_coords = piece.generate_possible_moves(self, check_check=True)
                if possible_movement_coords.count(king_coords) > 0:
                    # a possible movement for this piece is taking the king
                    # the king is in check
                    return True

        # no pieces have possible moves that intersect the king
        # the king is not in check
        return False

    def is_checkmate(self, color):
        if not self.is_king_in_check(color):
            return False

        # iterate through all pieces of current color
        # and see if any of their movements will make the king
        # not be in check anymore
        for row in self.board:
            for piece in row:
                if piece == None:
                    continue
                if piece.color != color:
                    continue
                possible_movement_coords = piece.generate_possible_moves(self)
                if len(possible_movement_coords) > 0:
                    return False

        # no pieces could move anywhere that the king
        # would not remain in check
        return True
