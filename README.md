# config_grid

## A lightweight convenient grid class

config_grid provides the class ConfigGrid that allows for the construction and manipulation of 2D gridded structures.

No need to install the whole of Pandas for this simple task!

### Constructors provided:

From within your code create readable grids, and quickly initialise into ConfigGrid objects. e.g.

`ConfigGrid.from_lines`:

    lines = (("Meals"    ,   "Mon",  "Tues",  "Weds",  "Thur"),
             ("Breakfast", "Toast", "Toast", "Toast", "Toast"),
             ("Lunch"    ,  "Soup", "Curry",  "Soup",  "Soup"),
             ("Dinner"   , "Curry", "Curry", "Curry", "Curry"))
    grid = ConfigGrid.from_lines(lines)

Quickly load grids from csv files, with automatic sniffing (or the option to provide the dialtect manually!). e.g.

`ConfigGrid.from_csv_file`:

    with open("grid.csv") as grid_file:
        grid = ConfigGrid.from_csv_file(grid_file)

Or initalise your grid with the headings, and then fill later. e.g.

`ConfigGrid.__init__`:

    grid = ConfigGrid(("Mon", "Tues", "Weds", "Thur"), ("Breakfast", "Lunch", "Dinner"))
    for day in ("Mon", "Tues", "Weds", "Thur"):
        grid[day]["Breakfast"] = "Toast"
        grid[day]["Lunch"] = "Soup"
        grid[day]["Dinner"] = "Curry!"
    grid["Tues"]["Lunch"] = "Something different!"

### Access items intuitively

Access using:

`ConfigGrid.__getitem__` e.g.

    grid["Row 1"]["Col 2"] -> value at that position

`ConfigGrid.col` and `ConfigGrid.row` e.g.

    grid.col("Col 1") -> returns values found in column

Iterate using:

`ConfigGrid.cols` and `ConfigGrid.rows` e.g.

    for col_heading, column in grid.cols:
        for row_heading, value in column:
            print("Value at {}, {} is {}".format(row_heading, col_heading, value))

`ConfigGrid.cells` e.g.

    for cell in grid.cells:
        print("Value at {}, {} is {}".format(cell.row, cell.col, cell.value))

### Easily modify prexisting grids:

Using convenience methods:

`ConfigGrid.__setitem__` e.g.

    grid["Row 1"]["Col 2"] = 42

`ConfigGrid.append_row` and `ConfigGrid.append_col` e.g.

    grid.append_row("Extra row", (1, 2, 3, 4))

`ConfigGrid.set_row` and `ConfigGrid.set_col` e.g.

    grid.append_row("Existing Row", (1, 2, 3, 4))

`ConfigGrid.combine` and `ConfigGrid.__add__` will add two grids together, combining either rows or cols e.g.

    grid.combine(other_grid)

`ConfigGrid.swap_cols` and `ConfigGrid.swap_rows` e.g.

    grid.swap_cols("Col 1", "Col 2")

or change the order of the cols and rows by sorting the `col_headings` and `row_headings` attribute e.g.

    grid.col_headings.sort(key=lambda food: food.calories)

### Finally easily write to a csv file for portability

     with open("new_grid.csv", "w") as f:
        grid.save_to_file(f)

### Customise the read and write process by subclassing

`ConfigGrid.preprocess_value` and `ConfigGrid.postprocess_value` are applied to every cell upon reading and writing to
csv files. Allows for easy customisation of this process by subclassing and overwriting these methods e.g.

     class TimeGrid(ConfigGrid):

        def preprocess_value(self, row, col, value):
            return datetime.strptime(pattern, value)

        def postprocess_value(self, row, col, value):
            return value.ctime()

# Installation

* Clone the repository to wherever you want it with `git clone https://github.com/0Hughman0/config_grid/`
* Run the setup.py by navigating to the config_grid folder in your chosen shell, and simply run `python setup.py install`