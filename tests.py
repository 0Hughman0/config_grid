import unittest

from config_grid import ConfigGrid, Cell


class IntGrid(ConfigGrid):

    def preprocess_value(self, row, col, value):
        return int(value)


class BaseCase:

    def compare_cells(self, expected):
        t_grid = ConfigGrid.from_lines(expected)
        for cell, t_cell in zip(self.grid.cells, t_grid.cells):
            self.assertEqual(cell.row, t_cell.row)
            self.assertEqual(cell.col, t_cell.col)
            self.assertEqual(cell.value, t_cell.value)

    def test_headings(self):
        self.assertSequenceEqual(self.grid.row_headings, ("Row 1", "Row 2"))
        self.assertSequenceEqual(self.grid.col_headings, ("Col 1", "Col 2", "Col 3", "Col 4"))

    def test_subscripting(self):
        self.assertEqual(self.grid["Row 1"]["Col 3"], 3)
        self.assertEqual(self.grid["Row 2"]["Col 2"], 6)
        self.assertEqual(self.grid["Row 2"]["Col 4"], 8)

    def test_iters(self):
        cols_tuple = (("Col 1", (("Row 1", 1), ("Row 2", 5))),
                      ("Col 2", (("Row 1", 2), ("Row 2", 6))),
                      ("Col 3", (("Row 1", 3), ("Row 2", 7))),
                      ("Col 4", (("Row 1", 4), ("Row 2", 8))))
        for cols, t_cols in zip(self.grid.cols, cols_tuple):
            col_heading, col = cols
            t_col_heading, t_col = t_cols
            for rows, t_rows in zip(col, t_col):
                row_heading, value = rows
                t_row_heading, t_value = t_rows
                self.assertEqual(col_heading, t_col_heading)
                self.assertEqual(row_heading, t_row_heading)
                self.assertEqual(value, t_value)
        rows_tuple = (("Row 1", (("Col 1", 1), ("Col 2", 2), ("Col 3", 3), ("Col 4", 4))),
                      ("Row 2", (("Col 1", 5), ("Col 2", 6), ("Col 3", 7), ("Col 4", 8))))
        for rows, t_rows in zip(self.grid.rows, rows_tuple):
            row_heading, row = rows
            t_row_heading, t_row = t_rows
            for cols, t_cols in zip(row, t_row):
                col_heading, value = cols
                t_col_heading, t_value = t_cols
                self.assertEqual(col_heading, t_col_heading)
                self.assertEqual(row_heading, t_row_heading)
                self.assertEqual(value, t_value)
        cells_tuple = []
        for row_heading, row in rows_tuple:
            for col_heading, value in row:
                cells_tuple.append(Cell(row_heading, col_heading, value))
        for cell, t_cell in zip(self.grid.cells, cells_tuple):
            self.assertEqual(cell, t_cell)

    def test_col_row(self):
        self.assertSequenceEqual(tuple(self.grid.col("Col 1")), (1, 5))
        self.assertSequenceEqual(tuple(self.grid.col("Col 4")), (4, 8))
        self.assertSequenceEqual(tuple(self.grid.col("Col 3")), (3, 7))
        self.assertSequenceEqual(tuple(self.grid.row("Row 1")), (1, 2, 3, 4))
        self.assertSequenceEqual(tuple(self.grid.row("Row 2")), (5, 6, 7, 8))

    def test_appends(self):
        self.grid.append_row("Row 3", (9, 10, 11, 12))
        expected = \
            (("Test Grid", "Col 1", "Col 2", "Col 3", "Col 4"),
             (    "Row 1",       1,       2,       3,       4),
             (    "Row 2",       5,       6,       7,       8),
             (    "Row 3",       9,      10,      11,      12))
        self.compare_cells(expected)
        self.grid.append_col("Col 5", (1, 2, 3))
        expected = \
            (("Test Grid", "Col 1", "Col 2", "Col 3", "Col 4", "Col 5"),
             (    "Row 1",       1,       2,       3,       4,       1),
             (    "Row 2",       5,       6,       7,       8,       2),
             (    "Row 3",       9,      10,      11,      12,       3))
        self.compare_cells(expected)

    def test_sets(self):
        self.grid.set_row("Row 1", ("new 1", "new 2", "new 3", "new 4"))
        expected = \
            (("Test Grid", "Col 1", "Col 2", "Col 3", "Col 4"),
             (    "Row 1", "new 1", "new 2", "new 3", "new 4"),
             (    "Row 2",       5,       6,       7,       8))
        self.compare_cells(expected)
        new_col_values = ("new 9", "new 10")
        self.grid.set_col("Col 2", ("new 9", "new 10"))
        expected = \
            (("Test Grid", "Col 1", "Col 2", "Col 3", "Col 4"),
             (    "Row 1", "new 1", "new 9", "new 3", "new 4"),
             (    "Row 2",       5,"new 10",       7,       8))
        self.compare_cells(expected)

    def test_combine_all_new(self):
        to_combine = \
            (("Combine Grid", "Col 5", "Col 6", "Col 7", "Col 8"),
             (       "Row 1",       9,      10,      11,      12),
             (       "Row 2",      13,      14,      15,      16))
        expected = \
            (("Test Grid", "Col 1", "Col 2", "Col 3", "Col 4", "Col 5", "Col 6", "Col 7", "Col 8"),
             (    "Row 1",       1,       2,       3,       4,       9,      10,      11,      12),
             (    "Row 2",       5,       6,       7,       8,      13,      14,       15,     16))
        new_grid = ConfigGrid.from_lines(to_combine)
        self.grid.combine(new_grid)
        self.compare_cells(expected)

    def test_combine_overlap(self):
        to_combine = \
            (("Combine Grid", "Col 2", "Col 5",  "Col 6",  "Col 8"),
             (       "Row 1",      13,      14,       15,       16),
             (       "Row 2",       9,      10,       11,       12))
        expected = \
            (("Test Grid", "Col 1", "Col 2", "Col 3", "Col 4", "Col 5", "Col 6", "Col 8"),
             (    "Row 1",       1,      13,       3,       4,       14,      15,     16),
             (    "Row 2",       5,      9,       7,       8,       10,      11,      12))
        new_grid = ConfigGrid.from_lines(to_combine)
        self.grid.combine(new_grid)
        self.compare_cells(expected)

    def test_combine_overlap_ow_false(self):
        to_combine = \
            (("Combine Grid", "Col 2", "Col 5",  "Col 6",  "Col 8"),
             (       "Row 1",      13,      14,       15,       16),
             (       "Row 2",       9,      10,       11,       12))
        expected = \
            (("Test Grid", "Col 1", "Col 2", "Col 3", "Col 4", "Col 5", "Col 6", "Col 8"),
             (    "Row 1",       1,      2,       3,       4,       14,      15,      16),
             (    "Row 2",       5,      6,       7,       8,       10,      11,      12))
        new_grid = ConfigGrid.from_lines(to_combine)
        self.grid.combine(new_grid, False)
        self.compare_cells(expected)

class FromLinesCase(unittest.TestCase, BaseCase):

    def setUp(self):
        self.input = (("Test Grid", "Col 1", "Col 2", "Col 3", "Col 4"),
                      (    "Row 1",       1,       2,       3,       4),
                      (    "Row 2",       5,       6,       7,       8))
        self.grid = ConfigGrid.from_lines(self.input)


class FromCsvCase(unittest.TestCase, BaseCase):

    def setUp(self):
        with open(r"test_grid.csv") as file:
            self.grid = IntGrid.from_csv_file(file)


class FilledCase(unittest.TestCase, BaseCase):

    def setUp(self):
        filled_grid = ConfigGrid(("Row 1", "Row 2"),
                                 ("Col 1", "Col 2", "Col 3", "Col 4"),
                                 "Test Grid")
        for row in range(1, 3):
            for col in range(1, 5):
                filled_grid["Row {}".format(row)]["Col {}".format(col)] = ((row - 1) * 4) + col
        self.grid = filled_grid


if __name__ == "__main__":
    unittest.main()