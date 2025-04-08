# csv2db  
This script imports CSV data into an SQLite database.
Download the script from GitHub. You can also find the Python source code in the `/python_code` folder.

## Before you run
The script reads a CSV file and inserts the values into an SQLite database. It assumes that the CSV file has a header row with column names. If it does not, you will need to add these manually. The script also assumes that the SQLite database contains tables matching the CSV column names.

## How to run
You can either run the script from the terminal or by double-clicking it with the left mouse button.
When you run the script, you will first be asked to provide the path to the database (`.db`) file, relative to the script’s location, as well as the relative path to the CSV file. If you are unsure of the relative paths, you can run the script from the same directory as your `.db` and `.csv` files.

Finally, press Enter to exit the script after the values have been inserted into the database.

