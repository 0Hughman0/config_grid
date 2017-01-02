# config_grid

## A lightweight convenient grid class

config_grid provides the class ConfigGrid that allows for the construction and manipulation of 2D gridded structures.

No need to install the whole of Pandas for this simple task!

### Constructors provided:

From within your code create readable grids, and quickly initialise into ConfigGrid objects. e.g.

`ConfigGrid.from_lines`:

    lines = (("Meals"    ,   "Mon",                 "Tues",  "Weds",  "Thur"),
             ("Breakfast", "Toast",                "Toast", "Toast", "Toast"),
             ("Lunch"    ,  "Soup", "Something Different!",  "Soup",  "Soup"),
             ("Dinner"   , "Curry",                "Curry", "Curry", "Curry"))
    grid = ConfigGrid.from_lines(lines)

    print(grid)
    Meals      Mon    Tues                  Weds   Thur
    Breakfast  Toast  Toast                 Toast  Toast
    Lunch      Soup   Something Different!  Soup   Soup
    Dinner     Curry  Curry                 Curry  Curry


Quickly load grids from csv files, with automatic sniffing (or the option to provide the dialtect manually!). e.g.

`ConfigGrid.from_csv_file`:

    with open("grid.csv") as grid_file:
        grid = ConfigGrid.from_csv_file(grid_file)

    print(grid)
    Meals      Mon    Tues                  Weds   Thur
    Breakfast  Toast  Toast                 Toast  Toast
    Lunch      Soup   Something Different!  Soup   Soup
    Dinner     Curry  Curry                 Curry  Curry

Or initalise your grid with the headings, and then fill later. e.g.

`ConfigGrid.__init__`:

    grid = ConfigGrid(("Breakfast", "Lunch", "Dinner"), ("Mon", "Tues", "Weds", "Thur"), "Meals")
    for day in ("Mon", "Tues", "Weds", "Thur"):
        grid["Breakfast"][day] = "Toast"
        grid["Lunch"][day] = "Soup"
        grid["Dinner"][day] = "Curry!"
    grid["Lunch"]["Tues"] = "Something different!"

    print(grid)
    Meals      Mon     Tues                  Weds    Thur
    Breakfast  Toast   Toast                 Toast   Toast
    Lunch      Soup    Something Different!  Soup    Soup
    Dinner     Curry!  Curry!                Curry!  Curry!

### Access items intuitively

Access using:

`ConfigGrid.__getitem__` e.g.

    grid["Row 1"]["Col 2"] -> value at that position

`ConfigGrid.col` and `ConfigGrid.row` e.g.

    grid.col("Col 1") -> returns values found in column

Iterate using:

`ConfigGrid.cols` and `ConfigGrid.rows` e.g.

    for col_heading, column in zip(grid.col_hds, grid.cols):
        for row_heading, value in zip(grid.row_hds, column):
            print("Value at {}, {} is {}".format(row_heading, col_heading, value))
    Value at Breakfast, Mon is Toast
    Value at Lunch, Mon is Soup
    Value at Dinner, Mon is Curry!
    Value at Breakfast, Tues is Toast
    Value at Lunch, Tues is Something Different!
    Value at Dinner, Tues is Curry!
    Value at Breakfast, Weds is Toast
    Value at Lunch, Weds is Soup
    Value at Dinner, Weds is Curry!
    Value at Breakfast, Thur is Toast
    Value at Lunch, Thur is Soup
    Value at Dinner, Thur is Curry!

`ConfigGrid.cells` e.g.

    for cell in grid.cells:
        print("Value at {}, {} is {}".format(cell.row, cell.col, cell.value))

    Value at Breakfast, Mon is Toast
    Value at Breakfast, Tues is Toast
    Value at Breakfast, Weds is Toast
    Value at Breakfast, Thur is Toast
    Value at Lunch, Mon is Soup
    Value at Lunch, Tues is Something Different!
    Value at Lunch, Weds is Soup
    Value at Lunch, Thur is Soup
    Value at Dinner, Mon is Curry!
    Value at Dinner, Tues is Curry!
    Value at Dinner, Weds is Curry!
    Value at Dinner, Thur is Curry!

### Easily modify prexisting grids:

Using convenience methods:

`ConfigGrid.__setitem__` e.g.

    grid["Dinner"]["Thur"] = "Chicken & rice"

    print(grid)
    Meals      Mon     Tues                  Weds    Thur
    Breakfast  Toast   Toast                 Toast   Toast
    Lunch      Soup    Something Different!  Soup    Soup
    Dinner     Curry!  Curry!                Curry!  Chicken & rice

`ConfigGrid.append_row` and `ConfigGrid.append_col` e.g.

    grid.append_row("Midnight Snack", ["Shmores!"] * 4)

    print(grid)
    Meals           Mon       Tues                  Weds      Thur
    Breakfast       Toast     Toast                 Toast     Toast
    Lunch           Soup      Something Different!  Soup      Soup
    Dinner          Curry!    Curry!                Curry!    Chicken & rice
    Midnight Snack  Shmores!  Shmores!              Shmores!  Shmores!

`ConfigGrid.set_row` and `ConfigGrid.set_col` e.g.

    grid.set_row("Breakfast", ["Still Full :L"] * 4)

    print(grid)
    Meals           Mon            Tues                  Weds           Thur
    Breakfast       Still Full :L  Still Full :L         Still Full :L  Still Full :L
    Lunch           Soup           Something Different!  Soup           Soup
    Dinner          Curry!         Curry!                Curry!         Chicken & rice
    Midnight Snack  Shmores!       Shmores!              Shmores!       Shmores!

`ConfigGrid.combine` and `ConfigGrid.__add__` will add two grids together, combining either rows or cols e.g.

    friday_meals = ((              "",            "Fri"),
                    (     "Breakfast",         "Cereal"),
                    (         "Lunch", "Fish 'n' Chips"),
                    (        "Dinner",    "Takeaway :3"),
                    ("Midnight Snack",             None)) # Full!
    other_grid = ConfigGrid.from_lines(friday_meals)
    grid.combine(other_grid)

    print(grid)
    Meals           Mon            Tues                  Weds           Thur            Fri
    Breakfast       Still Full :L  Still Full :L         Still Full :L  Still Full :L   Cereal
    Lunch           Soup           Something Different!  Soup           Soup            Fish 'n' Chips
    Dinner          Curry!         Curry!                Curry!         Chicken & rice  Takeaway :3
    Midnight Snack  Shmores!       Shmores!              Shmores!       Shmores!        None

`ConfigGrid.swap_cols` and `ConfigGrid.swap_rows` e.g.

    grid.swap_cols("Tues", "Thur") # Not sure why!?

    print(grid)

    Meals           Mon            Thur            Weds           Tues                  Fri
    Breakfast       Still Full :L  Still Full :L   Still Full :L  Still Full :L         Cereal
    Lunch           Soup           Soup            Soup           Something Different!  Fish 'n' Chips
    Dinner          Curry!         Chicken & rice  Curry!         Curry!                Takeaway :3
    Midnight Snack  Shmores!       Shmores!        Shmores!       Shmores!              None

or change the order of the cols and rows by sorting the `col_headings` and `row_headings` attribute e.g.

    grid.col_hds.sort() # make use of sort(key=?) for more powerful usage

    print(grid)

    Meals           Fri             Mon            Thur            Tues                  Weds
    Breakfast       Cereal          Still Full :L  Still Full :L   Still Full :L         Still Full :L
    Lunch           Fish 'n' Chips  Soup           Soup            Something Different!  Soup
    Dinner          Takeaway :3     Curry!         Chicken & rice  Curry!                Curry!
    Midnight Snack  None            Shmores!       Shmores!        Shmores!              Shmores!

### Finally easily write to a csv file for portability

     with open("new_grid.csv", "w") as f:
        grid.save_to_file(f)

     # new_grid.csv:
    Meals,Fri,Mon,Thur,Tues,Weds
    Breakfast,Cereal,Still Full :L,Still Full :L,Still Full :L,Still Full :L
    Lunch,Fish 'n' Chips,Soup,Soup,Something Different!,Soup
    Dinner,Takeaway :3,Curry!,Chicken & rice,Curry!,Curry!
    Midnight Snack,,Shmores!,Shmores!,Shmores!,Shmores!

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
