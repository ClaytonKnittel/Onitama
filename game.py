
class colors:
	GRAY = 0
	RED = 1
	BLUE = 2

class pieces:
	EMPTY = 0
	RED_QUEEN = 1
	RED_PAWN = 2
	BLUE_QUEEN = 3
	BLUE_PAWN = 4

BOARD_WIDTH = 5
BOARD_HEIGHT = 5

TILES = [
		{
			"name" : "cobra",
			"moves" : ((-1, 0), (1, 1), (1, -1)),
			"color" : colors.RED,
			"go_first": colors.RED
		},
		{
			"name" : "rabbit",
			"moves" : ((-1, -1), (1, 1), (2, 0)),
			"color" : colors.RED,
			"go_first": colors.BLUE
		},
		{
			"name" : "ox",
			"moves" : ((0, 1), (1, 0), (0, -1)),
			"color" : colors.RED,
			"go_first": colors.BLUE
		},
		{
			"name" : "rooster",
			"moves" : ((-1, 0), (-1, -1), (1, 0), (1, 1)),
			"color" : colors.RED,
			"go_first": colors.RED
		},

		{
			"name" : "horse",
			"moves" : ((-1, 0), (0, 1), (0, -1)),
			"color" : colors.BLUE,
			"go_first": colors.RED
		},
		{
			"name" : "goose",
			"moves" : ((-1, 0), (-1, 1), (1, 0), (1, -1)),
			"color" : colors.BLUE,
			"go_first": colors.BLUE
		},
		{
			"name" : "eel",
			"moves" : ((-1, 1), (-1, -1), (1, 0)),
			"color" : colors.BLUE,
			"go_first": colors.BLUE
		},
		{
			"name" : "frog",
			"moves" : ((-2, 0), (-1, 1), (1, -1)),
			"color" : colors.BLUE,
			"go_first": colors.RED
		},

		{
			"name" : "tiger",
			"moves" : ((0, 2), (0, -1)),
			"color" : colors.GRAY,
			"go_first": colors.BLUE
		},
		{
			"name" : "elephant",
			"moves" : ((-1, 0), (-1, 1), (1, 0), (1, 1)),
			"color" : colors.GRAY,
			"go_first": colors.RED
		},
		{
			"name" : "crane",
			"moves" : ((-1, -1), (0, 1), (1, -1)),
			"color" : colors.GRAY,
			"go_first": colors.BLUE
		},
		{
			"name" : "crab",
			"moves" : ((-2, 0), (0, 1), (2, 0)),
			"color" : colors.GRAY,
			"go_first": colors.BLUE
		},
		{
			"name" : "boar",
			"moves" : ((-1, 0), (0, 1), (1, 0)),
			"color" : colors.GRAY,
			"go_first": colors.RED
		},
		{
			"name" : "mantis",
			"moves" : ((-1, 1), (0, -1), (1, 1)),
			"color" : colors.GRAY,
			"go_first": colors.RED
		},
		{
			"name" : "monkey",
			"moves" : ((-1, -1), (-1, 1), (1, -1), (1, 1)),
			"color" : colors.GRAY,
			"go_first": colors.BLUE
		},
		{
			"name" : "dragon",
			"moves" : ((-2, 1), (-1, -1), (1, -1), (2, 1)),
			"color" : colors.GRAY,
			"go_first": colors.RED
		}
	]

def redify(string):
	return "\033[0;31m" + string + "\033[0m"

def bluefy(string):
	return "\033[0;36m" + string + "\033[0m"

def grayfy(string):
	return "\033[0;37m" + string + "\033[0m"

def tile_str(piece):
	return [' ', redify('Q'), redify('p'), bluefy('Q'), bluefy('p')][piece]


def to_idx(row, col):
	return col + row * BOARD_WIDTH

def to_coord(idx):
	return idx // BOARD_WIDTH, idx % BOARD_WIDTH

def piece_color(piece):
	return (piece + 1) >> 1


class onitama:

	# Expects a list of tile names for each player (2 for red/blue, 1 tile in the middle)
	def __init__(self, red_tiles, middle_tile, blue_tiles):
		self.red_tiles = [get_tile(name) for name in red_tiles]
		self.middle_tile = get_tile(middle_tile)
		self.blue_tiles = [get_tile(name) for name in blue_tiles]
		# boards are indexed in row-major order, with red being in the first row and blue in the last
		self.board = [pieces.EMPTY] * (BOARD_WIDTH * BOARD_HEIGHT)
		self.turn = 0

		# set the pieces
		for col in range(BOARD_WIDTH):
			if col == BOARD_WIDTH // 2:
				self.board[to_idx(0, col)] = pieces.RED_QUEEN
				self.board[to_idx(BOARD_HEIGHT - 1, col)] = pieces.BLUE_QUEEN
			else:
				self.board[to_idx(0, col)] = pieces.RED_PAWN
				self.board[to_idx(BOARD_HEIGHT - 1, col)] = pieces.BLUE_PAWN


	def __str__(self):
		row_divider = "+" + "---+" * BOARD_WIDTH + '\n'

		board = row_divider
		for row in reversed(range(BOARD_HEIGHT)):
			board += '|'
			for col in range(BOARD_WIDTH):
				board += ' ' + tile_str(self.board[to_idx(row, col)]) + ' |'
			board += '\n' + row_divider

		tiles = redify(self.red_tiles[0]['name']) + " " + redify(self.red_tiles[1]['name']) + " " + \
				grayfy(self.middle_tile['name']) + " " + \
				bluefy(self.blue_tiles[0]['name']) + " " + bluefy(self.blue_tiles[1]['name'])
		return board + tiles

	def describe_move(self, move):
		piece_idx, tile_idx, move_idx = move
		r, c = to_coord(piece_idx)
		if self.turn_color() == colors.RED:
			tile = self.red_tiles[tile_idx]
		else:
			tile = self.blue_tiles[tile_idx]
		dc, dr = tile['moves'][move_idx]
		print("%s moves %s at (%d, %d) to (%d, %d) using %s" %
				(redify("red") if self.turn_color() == colors.RED else bluefy("blue"),
					"pawn" if self.board[piece_idx] == pieces.RED_PAWN or self.board[piece_idx] == pieces.BLUE_PAWN else "queen",
					c, r,
					c + dc, r + dr,
					tile['name']
					))

	# returns the color of the player whose turn it is
	def turn_color(self):
		return self.turn % 2 + 1

	# moves are in the format:
	#   (piece_idx, tile_idx, move_idx)
	#   piece_idx: the index of the piece being moved
	#   tile_idx: the index in the list of tiles whose turn this is that's being used
	#   move_idx: the index in the tile being used as the move
	def move(self, move):
		piece_idx, tile_idx, move_idx = move
		# make sure the piece beiing moved belongs to the current player
		assert(self.turn_color() == piece_color(self.board[piece_idx]))
		row, col = to_coord(piece_idx)
		if self.turn_color() == colors.RED:
			tile = self.red_tiles[tile_idx]
		else:
			tile = self.blue_tiles[tile_idx]
		dc, dr = tile['moves'][move_idx]
		# make sure the move is in bounds
		assert(0 <= row + dr < BOARD_HEIGHT)
		assert(0 <= col + dc < BOARD_WIDTH)
		# make sure the move doesn't go into a tile containing one of our own pieces
		assert(piece_color(self.board[to_idx(row + dr, col + dc)]) != self.turn_color())

		# move the piece there
		self.board[to_idx(row + dr, col + dc)] = self.board[piece_idx]
		self.board[piece_idx] = pieces.EMPTY

		# swap out the tile
		if self.turn_color() == colors.RED:
			self.red_tiles[tile_idx], self.middle_tile = self.middle_tile, self.red_tiles[tile_idx]
		else:
			self.blue_tiles[tile_idx], self.middle_tile = self.middle_tile, self.blue_tiles[tile_idx]

		# increment the turn counter
		self.turn += 1

	def legal_moves(self):
		tiles = self.red_tiles if self.turn_color() == colors.RED else self.blue_tiles
		for piece_idx in range(len(self.board)):
			if piece_color(self.board[piece_idx]) != self.turn_color():
				continue
			row, col = to_coord(piece_idx)
			for tile_idx in range(len(tiles)):
				moves = tiles[tile_idx]['moves']
				for move_idx in range(len(moves)):
					dc, dr = moves[move_idx]
					r = row + dr
					c = col + dc
					if 0 <= r < BOARD_HEIGHT and 0 <= c < BOARD_WIDTH and piece_color(self.board[to_idx(r, c)]) != self.turn_color():
						yield (piece_idx, tile_idx, move_idx)

	def get_winner(self):
		# check if red reached end
		if self.board[to_idx(BOARD_HEIGHT - 1, BOARD_WIDTH // 2)] == pieces.RED_QUEEN:
			return colors.RED
		if self.board[to_idx(0, BOARD_WIDTH // 2)] == pieces.BLUE_QUEEN:
			return colors.BLUE
		# check if the red queen doesn't exist any more
		if pieces.RED_QUEEN not in self.board:
			return colors.BLUE
		if pieces.BLUE_QUEEN not in self.board:
			return colors.RED
		return colors.GRAY

	def serialize(self):
		pass


def get_tile(name):
	return next(tile for tile in TILES if tile["name"] == name)


if __name__ == "__main__":
	from sys import argv
	import copy
	import random

	if len(argv) != 6:
		print("Expect %s <red tiles> <middle tile> <blue tiles>" % argv[0])
		exit(-1)
	o = onitama(argv[1:3], argv[3], argv[4:6])
	print(o)
	while o.get_winner() == colors.GRAY:
		moves = list(o.legal_moves())
		move = random.choice(moves)
		o.describe_move(move)
		o.move(move)
		print(o)

