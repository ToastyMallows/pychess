import pygame
from pygame.locals import *
from enum import Enum
from copy import copy
from coordinate import Coordinate
from piecetype import PieceType
from movement import PossibleMovement
from constants import BLACK, WHITE, WIN_HEIGHT, WIN_WIDTH, BLACK_COLOR, WHITE_COLOR, GREY_COLOR, RED_COLOR, GOLD_COLOR, TILE_SIZE
from board import Board
from pieces.bishop import Bishop
from pieces.king import King
from pieces.knight import Knight
from pieces.queen import Queen
from pieces.pawn import Pawn
from pieces.rook import Rook

all_pieces_group = pygame.sprite.Group()
possible_movement_group = pygame.sprite.Group()

turn = WHITE

display_surface = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))


def build_black_pieces():
    black_pieces = []
    # rooks
    black_pieces.append(Rook(BLACK, Coordinate(0, 0)))
    black_pieces.append(Rook(BLACK, Coordinate(7, 0)))
    # knights
    black_pieces.append(Knight(BLACK, Coordinate(1, 0)))
    black_pieces.append(Knight(BLACK, Coordinate(6, 0)))
    # bishops
    black_pieces.append(Bishop(BLACK, Coordinate(2, 0)))
    black_pieces.append(Bishop(BLACK, Coordinate(5, 0)))
    # queen
    black_pieces.append(Queen(BLACK, Coordinate(3, 0)))
    # king
    black_pieces.append(King(BLACK, Coordinate(4, 0)))
    # pawns
    for x in range(8):
        black_pieces.append(Pawn(BLACK, Coordinate(x, 1)))
    return black_pieces


def build_white_pieces():
    white_pieces = []
    # rooks
    white_pieces.append(Rook(WHITE, Coordinate(0, 7)))
    white_pieces.append(Rook(WHITE, Coordinate(7, 7)))
    # knights
    white_pieces.append(Knight(WHITE, Coordinate(1, 7)))
    white_pieces.append(Knight(WHITE, Coordinate(6, 7)))
    # bishops
    white_pieces.append(Bishop(WHITE, Coordinate(2, 7)))
    white_pieces.append(Bishop(WHITE, Coordinate(5, 7)))
    # queen
    white_pieces.append(Queen(WHITE, Coordinate(3, 7)))
    # king
    white_pieces.append(King(WHITE, Coordinate(4, 7)))
    # pawns
    for x in range(8):
        white_pieces.append(Pawn(WHITE, Coordinate(x, 6)))
    return white_pieces


def draw_sprite(sprite):
    display_surface.blit(sprite.image, sprite.rect)


def draw_background(board):
    for x in range(8):
        for y in range(8):
            color = None
            if (x % 2 == 0 and y % 2 == 0) or (x % 2 != 0 and y % 2 != 0):
                color = WHITE_COLOR
            else:
                color = GREY_COLOR

            space_piece = board.get_piece(Coordinate(x, y))
            if space_piece != None:
                if space_piece.selected:
                    color = GOLD_COLOR
                if isinstance(space_piece, King):
                    # check check
                    if board.is_king_in_check(space_piece.color):
                        color = RED_COLOR

            pygame.draw.rect(display_surface, color, pygame.Rect(x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE))


def draw_board():
    possible_movement_group.draw(display_surface)
    all_pieces_group.draw(display_surface)


def build_default_board(board):
    pieces = []
    pieces.extend(build_black_pieces())
    pieces.extend(build_white_pieces())
    board.populate(pieces)
    return pieces


def clear_all_selections():
    global all_pieces_group
    for s in all_pieces_group.sprites():
        s.selected = False
    global possible_movement_group
    for move in possible_movement_group:
        move.kill()
    possible_movement_group = pygame.sprite.Group()


def handle_mouse_click(event, board):
    position = event.pos

    clicked_pieces = [s for s in all_pieces_group.sprites() if s.rect.collidepoint(position)]
    clicked_moves = [s for s in possible_movement_group.sprites() if s.rect.collidepoint(position)]

    if len(clicked_moves) == 0 and len(clicked_pieces) == 0:
        # blank area was clicked
        clear_all_selections()
        return

    # clicked movement positions get resolved first
    # in order to handle overlaps (movement is an occupied space)
    if len(clicked_moves) == 1:
        # user clicked on a movement space
        # move the piece
        move = clicked_moves[0]
        if move.is_castle_movement():
            board.move_for_castle(move.coordinate, move.piece)
        else:
            _ = board.move_piece(move.coordinate, move.piece)
        clear_all_selections()
        global turn
        turn = WHITE if turn == BLACK else BLACK
        return

    if len(clicked_pieces) == 1:
        # user clicked on something
        piece = clicked_pieces[0]
        if piece.color != turn:
            # user clicked on opponents piece when it
            # was not their turn
            return
        clear_all_selections()
        # user clicked on a Chess Piece
        # generate all movements
        piece.selected = True
        current_possible_moves = generate_possible_moves(piece, board)
        for move in current_possible_moves:
            possible_movement_group.add(PossibleMovement(move, piece))


def generate_possible_moves(piece, board, check_check=False):
    return piece.generate_possible_moves(board, check_check)


def main():
    pygame.init()

    pygame.display.set_caption('Chess')

    board = Board()

    pieces = build_default_board(board)
    for piece in pieces:
        all_pieces_group.add(piece)

    run = True
    checkmate = False
    killed = False
    while run:
        display_surface.fill(BLACK_COLOR)

        draw_background(board)

        draw_board()

        pygame.display.update()

        if checkmate and not killed:
            board.get_pieces_by_type(PieceType.king, turn)[0].rotate(90)
            killed = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONUP and not checkmate:
                handle_mouse_click(event, board)
                checkmate = board.is_checkmate(turn)


# Execute game loop
main()
