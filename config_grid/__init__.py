import csv

from .utilities import Cell, UniqueList, LineDict


class ConfigGrid:
    """
    Config Grid class

    Utility class for creating and using config grids with a header column and row.

    can be initialised empty, with the row and column titles (see __init__) or from a 2D iterator of lines and rows.

    A from_csv_file factory is also provided for convenience.

    Saving to files is also supported
    """

    def __init__(self, row_headings, col_headings, title=None, default=""):
        """
        Initialisation for a blank ConfigGrid.

        Initialisation creates 2 nested LineDicts, with keys corresponding to the row and headings provided.
        This is stored as the protected _data attribute.

        Requires known row_headings and col_headings and then fill using the __setitem__ [ ] method
        e.g.

            grid = ConfigGrid(("Mon", "Tues", "Weds", "Thur"), ("Breakfast", "Lunch", "Dinner"))
            for day in ("Mon", "Tues", "Weds", "Thur"):
                grid[day]["Breakfast"] = "Toast"
                grid[day]["Lunch"] = "Soup"
                grid[day]["Dinner"] = "Curry!"
            grid["Tues"]["Lunch"] = "Something different!"

        :param row_headings:
            List containing the names/ keys that correspond to the row headings in your table (will be converted to a tuple [if not already one!])
        :param col_headings:
            As row_headings, but with the col headings
        :param title:
            Title of your table. Not really necessary, but when printed/ exported, this will be in the top left corner
         """
        self.title = title
        if title is None:
            self.title = self.__name__
        self.default = default
        self.path = ""
        self.row_headings = UniqueList(row_headings)
        self.col_headings = UniqueList(col_headings)
        self._data = LineDict(self.row_headings)
        for row_heading in self.row_headings:
            self._data[row_heading] = LineDict(self.col_headings, default)

    @staticmethod
    def process_lines(lines):
        """
        Helper staticmethod that separates row and column headers from the data in a table. Will also extract the
        first value as the title. Used by both from_lines and from_csv_file
        :param lines:
            simply takes any 2D iterable where the first dimension contains each row in the table,
            and the second dimension contains the contents in each row INCLUDING ROW AND COLUMN HEADERS.
            e.g.

                lines = ((""         ,   "Mon",  "Tues",  "Weds",  "Thur"),
                         ("Breakfast", "Toast", "Toast", "Toast", "Toast"),
                         ("Lunch"    ,  "Soup",  "Curry",  "Soup",  "Soup"),
                         ("Dinner"   , "Curry", "Curry", "Curry", "Curry"))

        :return: (row_headings, col_headings, data, title)
            row_headings: list containing the extracted row_headings found along the left hand column
            col_headings: list containing the extracted col_headings found along the top row
            data: list of Cell objects, that contain their row and column and their value
            title: the item found in the top left of the table
        """
        lines = iter(lines)
        title, *col_headings = lines.__next__()
        row_headings = []
        data = []
        for row in lines:
                row = iter(row)
                row_heading = row.__next__()
                row_headings.append(row_heading)
                for col_heading, value in zip(col_headings, row):
                    data.append(Cell(row=row_heading, col=col_heading, value=value))
        return row_headings, col_headings, data, title

    @classmethod
    def from_lines(cls, lines):
        """
        Alternative constructor for ConfigGrid, returns filled initialised instance of ConfigGrid,
        populated with the input lines.

        Generally expects a tuple representation of your table, and then the grid is initialised from that.
        e.g.

            lines = ((""         ,   "Mon",  "Tues",  "Weds",  "Thur"),
                     ("Breakfast", "Toast", "Toast", "Toast", "Toast"),
                     ("Lunch"    ,  "Soup",  "Curry",  "Soup",  "Soup"),
                     ("Dinner"   , "Curry", "Curry", "Curry", "Curry"))
            grid = ConfigGrid.from_lines(lines)

        :param lines:
            2D iterable, that returns each row in the first dimension, and the contents of each row in the second.
            The fist row and column are taken as the col_headings and row_headings respectively. The top left taken as
            the title of your table
        :return: an initialised and filled instance of ConfigGrid, from the contents of lines
        """
        row_headings, col_headings, data, title = cls.process_lines(lines)
        obj = cls(row_headings, col_headings, title)
        for cell in data:
            obj[cell.row][cell.col] = cls.preprocess_value(obj, cell.row, cell.col, cell.value)
        return obj

    @classmethod
    def from_csv_file(cls, file, csv_reader_args=None):
        """
        Alternative constructor allowing for easy loading from csv files . returns initialised and populated config grid
        based on file provided. utilises csv.reader
            e.g.

            with open("grid.csv") as grid_file:
                grid = ConfigGrid.from_csv_file(grid_file)

            ConfigGrid will try and sniff your file for its dialect, but you can bypass this by providing a dict of
            csv.reader args as csv_reader_args optional argument. There is also a write_to_file (see below)

        :param file:
            file object that contains the grid. NOTE: ConfigGrid will set seek to 0
        :param csv_reader_args:
            dictionary of dialect arguments that will be passed to csv.reader if provided
            (see csv.reader for details)
        :return: an initialised and filled instance of ConfigGrid, from the contents of file
        """
        file.seek(0)
        if csv_reader_args:
            reader_obj = csv.reader(file, csv_reader_args)
        else:
            try:
                dialect = csv.Sniffer().sniff(file.read(1024))
            except csv.Error:
                dialect = csv.excel
                dialect.delimiter = ","
                dialect.lineterminator = "\n"
            file.seek(0)
            reader_obj = csv.reader(file, dialect)
        return cls.from_lines(reader_obj)

    def __repr__(self):
        header_row = "\t".join([self.title] + self.col_headings)
        data_rows = []
        for row_heading, row_cells in self.rows:
            data_rows.append("\t".join((str(row_heading),) + tuple(str(value) for col, value in row_cells)))
        return "\n".join((header_row,) + tuple(data_rows))

    def __getitem__(self, row_heading):
        """
        Method used for accessing specific cells, it's expected that you'll also call __getitem__ on the LineDict
        returned e.g.

            cell = grid["Row 1"]["Col 2"]

        if you just desire an iterator over the contents of a row, use the row(row_heading) method

        :param item:
            desired row key
        :return:
            The LineDict containing the contents of the row selected. This LineDict is also subscriptable
        """
        return self._data[row_heading]

    def __setitem__(self, row_heading, value):
        """
        Same as __getitem__ except for setting values. e.g.
            grid["Row 1"]["Col 2"] = "foo"

        The introduction of new keys with this method is no allowed.

        :param row_heading: name of the row being modified
        :param value: value to set row to
        """
        self._data.__setitem__(row_heading, value)

    def __eq__(self, other):
        """
        True if rows and headings of both grids are equal
        :param other: ConfigGrid to compare to
        :return:
        """
        return set(self.row_headings) == set(other.row_headings) and set(self.col_headings) == set(other.col_headings)

    def __add__(self, other):
        """
        Shorthand for return current_grid.combine(other_grid)
        :param other: another ConfigGrid
        :return: combination of both grids
        """
        return self.combine(other)

    def preprocess_value(self, row, col, value):
        """
        Allows customisation of initialisation process.

        This method is applied to every cell upon initialisation. Taking row, col and value as parameter.
        The default implementation makes no changes, and simply returns value.

        To customise this behaviour, subclass ConfigGrid.

        e.g.
            class TimeGrid(ConfigGrid):

                def preprocess_value(self, row, col, value):
                    return datetime.strptime(pattern, value)

        :param row: the row this cell is found at
        :param col: the col this cell is found at
        :param value: the value of the cell
        :return: the unmodified cell
        """
        return value

    def postprocess_value(self, row, col, value):
        """
        Allows customisation of writing process.

        This method is applied to every cell upon initialisation. Taking row, col and value as parameter.
        The default implementation makes no changes, and simply returns value.

        To customise this behaviour, subclass ConfigGrid.

        e.g.
            class TimeGrid(ConfigGrid):

                def preprocess_value(self, row, col, value):
                    return datetime.strptime(pattern, value)

        :param row: the row this cell is found at
        :param col: the col this cell is found at
        :param value: the value of the cell
        :return: the unmodified cell
        """
        return value

    def save_to_file(self, file, csv_writer_args=None):
        """
        Save ConfigGrid to file using csv.writer

        :param file: file object for writing to
        :param csv_writer_args: dict of arguments to be passed to csv.writer see csv.writer documentation for details
        """
        writer = csv.writer(file, lineterminator="\n") if not csv_writer_args else csv.writer(file, **csv_writer_args)
        fieldnames = [self.title] + self.col_headings
        writer.writerow(fieldnames)
        for row_heading, row in self.rows:
            data_bit = tuple(self.postprocess_value(row_heading, col_heading, value) for col_heading, value in row)
            combined = (row_heading,) + data_bit
            writer.writerow(combined)

    @property
    def rows(self):
        """
        Property for iterating over the contents of each row in order.
        e.g.
        
        for row_heading, row in grid.rows:
            for col_heading, value in row:
                print("Value at {}, {} is {}".format(row_heading, col_heading, value))

        :return: (row_heading, <row_generator>)
            provides a tuple with the current row, and a generator expression that returns (col_heading, value) for 
            each position in the row
        """
        for row_heading in self.row_headings:
            yield row_heading, ((col_heading, self._data[row_heading][col_heading])
                                     for col_heading in self.col_headings)

    @property
    def cols(self):
        """
        Property for iterating over the contents of each column in order.
        e.g.
        
        for col_heading, column in grid.cols:
            for row_heading, value in column:
                print("Value at {}, {} is {}".format(row_heading, col_heading, value))

        :return: (col_heading, <col_generator>)
            provides a tuple with the current column, and a generator expression that returns (row_heading, value) for 
            each position in the column
        """
        for col_heading in self.col_headings:
            yield col_heading, ((row_heading, self._data[row_heading][col_heading])
                                     for row_heading in self.row_headings)

    @property
    def cells(self):
        """
        Property for iterating over each value in the grid, rasters across the grid from left to right, top to bottom.
        
        e.g.
            for cell in grid.cells:
                print("Value at {}, {} is {}".format(cell.row, cell.col, cell.value))
        :return:
            a generator that yields Cell objects for each cell in the grid
        """
        for row_heading in self.row_headings:
            for column_heading in self.col_headings:
                yield Cell(row=row_heading, col=column_heading, value=self._data[row_heading][column_heading])

    def col(self, col):
        """
        Returns the values of the given col, in order.
        
        :param col:
            name/ key for the col required
        :return: 
            a generator that yields the data in the col, in order
        """
        return (self._data[row][col] for row in self.row_headings)

    def row(self, row):
        """
        Returns the values of the given row, in order.
        
        :param row:
            name/ key for the row required
        :return: 
            a generator that yields the data in the row, in order
        """
        return (self._data[row][col] for col in self.col_headings)

    def append_col(self, col_heading, col):
        """
        Add a column to the end of the grid

        :param col_heading: name of new column
        :param col: iterator containing values within new column
        """
        col = tuple(col)
        if not len(self.row_headings) == len(col):
            raise IndexError("Different number of incoming values, to rows to fill")
        self.col_headings.append(col_heading)
        for row_heading, value in zip(self.row_headings, col):
            self._data[row_heading][col_heading] = value

    def append_row(self, row_heading, row):
        """
        Add a row to the bottom of the grid

        :param col_heading: name of new row
        :param col: iterator containing values within new row
        """
        row = tuple(row)
        if not len(self.col_headings) == len(row):
            raise IndexError("Different number of incoming values, to cols to fill")
        self.row_headings.append(row_heading)
        self._data[row_heading] = LineDict(self.col_headings)
        for col_heading, value in zip(self.col_headings, row):
            self._data[row_heading][col_heading] = value

    def set_row(self, row_heading, values):
        """
        Replace the current values in the row specified by row_heading, with those in values

        :param row_heading: Name of row to change
        :param values: iterator containing values in order to update
        """
        values = tuple(values)
        if not len(self.col_headings) == len(values):
            raise IndexError("Different number of incoming values, to cols to fill")
        for col_heading, new_val in zip(self.col_headings, values):
            self._data[row_heading][col_heading] = new_val

    def set_col(self, col_heading, values):
        """
        Replace the current values in the col specified by col_heading, with those in values

        :param row_heading: Name of col to change
        :param values: iterator containing values, in order, to update
        """
        values = tuple(values)
        if not len(self.row_headings) == len(values):
            raise IndexError("Different number of incoming values, to rows to fill")
        for row_heading, new_val in zip(self.row_headings, values):
            self._data[row_heading][col_heading] = new_val

    def combine(self, other, overwrite=True):
        """
        Combine the rows and values from other in self. By default will add new rows/ columns to the end of the grid,
        and will overwrite any matching columns/ rows.

        CAN ONLY MODIFY ONE OF ROWS OR COLUMNS NOT BOTH.

        if overwrite=False, any matching cells will not be over-writen by those in other.

        :param other: another ConfigGrid
        :param overwrite: do overwrite current matching cells with new ones?
        """
        new_rows = list(heading for heading in other.row_headings if heading not in self.row_headings)
        new_cols = list(heading for heading in other.col_headings if heading not in self.col_headings)
        if len(new_rows) > 0 and len(new_cols) > 0:
            raise KeyError("Can only add to one row or column at a time, incoming grid does not match in either")
        for heading in new_rows:
            self.append_row(heading, other.row(heading))
        for heading in new_cols:
            self.append_col(heading, other.col(heading))
        if overwrite:
            if new_rows:
                overlap_rows = (heading for heading in other.row_headings if heading in self.row_headings)
                for heading in overlap_rows:
                    self.set_row(heading, other.row(heading))
            if new_cols:
                overlap_cols = (heading for heading in other.col_headings if heading in self.col_headings)
                for heading in overlap_cols:
                    self.set_col(heading, other.col(heading))

    def swap_rows(self, row1, row2):
        row1_i = self.row_headings.index(row1)
        row2_i = self.row_headings.index(row2)
        self.row_headings.swap(row1_i, row2_i)
        
    def swap_cols(self, col1, col2):
        col1_i = self.col_headings.index(col1)
        col2_i = self.col_headings.index(col2)
        self.col_headings.swap(col1_i, col2_i)
