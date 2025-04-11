# Show all rows/columns (or set a high number)
import pandas as pd

pd.set_option("display.max_rows", 100)
pd.set_option("display.max_columns", 100)
pd.set_option("display.width", 400)  # fits Emacs REPL width
pd.set_option("display.colheader_justify", "center")
