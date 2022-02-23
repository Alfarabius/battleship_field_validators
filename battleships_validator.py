from copy import deepcopy


class FieldValidator:
	VISITED = 2
	SHIP = 1
	SEA = 0
	VALID = {1: 4, 2: 3, 3: 2, 4: 1}

	def __init__(self, field: list):
		self._field: list = field
		self._height: int = len(field)
		self._width: int = len(field[0])
		self._current = (0, 0)
		self._ships_dict = {1: 0, 2: 0, 3: 0, 4: 0}

	def __out_of_width(self) -> bool:
		return self._current[1] + 1 == self._width

	def __out_of_height(self) -> bool:
		return self._current[0] + 1 == self._height

	def __out_of_left_border(self) -> bool:
		return self._current[1] == 0

	def __check_borders(self) -> tuple:
		return (
			width_condition := not self.__out_of_width(),
			height_condition := not self.__out_of_height(),
			width_condition and height_condition,
			not self.__out_of_left_border() and height_condition
		)

	def __get_adjacent_cells(self) -> tuple:
		(
			not_out_of_width,
			not_out_of_height,
			not_out_of_bounds,
			not_out_of_left_border
		) = self.__check_borders()
		c = self._current

		bottom = self._field[c[0] + 1][c[1]] if not_out_of_height else None
		right = self._field[c[0]][c[1] + 1] if not_out_of_width else None
		diagonal = self._field[c[0] + 1][c[1] + 1] if not_out_of_bounds else None
		left_diagonal = self._field[c[0] + 1][c[1] - 1] if not_out_of_left_border else None

		return bottom, diagonal, right, left_diagonal

	def __visit_ships(self):
		not_out_of_width, not_out_of_height, _, _ = self.__check_borders()

		self._field[self._current[0]][self._current[1]] = self.VISITED

		if not_out_of_height and self._field[self._current[0] + 1][self._current[1]] == self.SHIP:
			self._field[self._current[0] + 1][self._current[1]] = self.VISITED

		if not_out_of_width and self._field[self._current[0]][self._current[1] + 1] == self.SHIP:
			self._field[self._current[0]][self._current[1] + 1] = self.VISITED

	def __check_ship(self) -> bool:
		size = 1

		while True:
			neighbors = self.__get_adjacent_cells()

			if (
					(n := neighbors.count(self.SHIP)) > 1
					or neighbors[1] == self.SHIP
					or neighbors[3] == self.SHIP
			):
				return False

			self.__visit_ships()

			if b := neighbors[0] == self.SHIP:
				self._current = (self._current[0] + 1, self._current[1])
			if r := neighbors[2] == self.SHIP:
				self._current = (self._current[0], self._current[1] + 1)

			size += 1 if b or r else 0

			if n == 0:
				break

		try:
			self._ships_dict[size] += 1
		except KeyError:
			return False

		return True

	def __validate_field(self) -> bool:
		for r, row in enumerate(self._field):
			for c, cell in enumerate(row):
				self._current = r, c

				if cell == self.VISITED:
					continue

				if cell == self.SHIP:
					result = self.__check_ship()
					if not result:
						return result

		return self._ships_dict == self.VALID

	def __call__(self, result=True) -> bool:
		result = self.__validate_field()
		return result


def validate_battlefield(field):
	return FieldValidator(field)()


if __name__ == '__main__':
	battle_field = \
		[
			[1, 0, 0, 0, 0, 1, 1, 0, 0, 0],
			[1, 0, 1, 0, 0, 0, 0, 0, 1, 0],
			[1, 0, 1, 0, 1, 1, 1, 0, 1, 0],
			[1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
			[0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
			[0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		]

	wrong_field = deepcopy(battle_field)
	wrong_field[0][1] = 1

	print(validate_battlefield(battle_field))
	print(validate_battlefield(wrong_field))
