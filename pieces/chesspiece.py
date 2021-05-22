import pygame
from piecetype import PieceType
from constants import BLACK, WHITE, TILE_SIZE


class ChessPiece(pygame.sprite.Sprite):
    def __init__(self, color, piece_type, coord, ghost=False):
        if coord == None:
            raise Exception("coord is None")
        if not isinstance(piece_type, PieceType):
            raise Exception("piece_type is not an Enum")

        self.__IMG_DIR = './img/'

        pygame.sprite.Sprite.__init__(self)

        self.color = color
        self.piece_type = piece_type
        self.coordinate = coord
        self._ghost = ghost
        self.selected = False
        self.direction = 1 if color == BLACK else -1

        if not ghost:
            self.image = pygame.image.load(self.__IMG_DIR + self.color + '_' + self.piece_type.name + '.png').convert_alpha()
        if not ghost:
            self.rect = pygame.Rect(self.coordinate.x * TILE_SIZE, self.coordinate.y * TILE_SIZE, TILE_SIZE, TILE_SIZE)

    def generate_coords_while_valid(self, board, coord_lambda):
        possible_movement_coords = []

        test_coord = coord_lambda(self.coordinate)

        while test_coord.is_valid():
            if board.is_occupied_by_self(test_coord, self.color):
                return possible_movement_coords
            possible_movement_coords.append(test_coord)
            if board.is_occupied_by_opponent(test_coord, self.color):
                return possible_movement_coords
            test_coord = coord_lambda(test_coord)

        return possible_movement_coords

    def filter_invalid_coords(self, coords, validity_lambda):
        valid_movements = []

        for coord in coords:
            if validity_lambda(self, coord):
                valid_movements.append(coord)

        return valid_movements

    def move(self, coord):
        if coord == None:
            raise Exception("coord is None")
        self.coordinate = coord
        if not self._ghost:
            self.rect = pygame.Rect(self.coordinate.x * TILE_SIZE, self.coordinate.y * TILE_SIZE, TILE_SIZE, TILE_SIZE)

    def rotate(self, angle):
        self.image = pygame.transform.rotate(self.image, angle)

    def create_ghost_piece(self):
        raise NotImplementedError()

    def generate_possible_moves(self, board, check_check=False):
        raise NotImplementedError()
