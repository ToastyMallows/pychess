import pygame
from constants import TILE_SIZE, GOLD_COLOR
from piecetype import PieceType


class PossibleMovement(pygame.sprite.Sprite):
    def __init__(self, coord, piece):
        if coord == None:
            raise Exception("coord is None")

        pygame.sprite.Sprite.__init__(self)

        self.coordinate = coord
        self.piece = piece
        self.rect = pygame.Rect(coord.x * TILE_SIZE, coord.y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill(GOLD_COLOR)

    def is_castle_movement(self):
        # the only time a king can move 2 spaces is for castling
        return self.piece.piece_type == PieceType.king and abs(self.coordinate.x - self.piece.coordinate.x) == 2
