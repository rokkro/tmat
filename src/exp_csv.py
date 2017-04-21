from display import get_coll, get_menu, color
from csv import DictWriter, DictReader
def setup():
    coll = get_coll()
    fname = input(color.BOLD + "*Please enter a filename. A .csv extension will be added.\n>>>" +
                  color.END).replace(" ","")
    if ".csv" not in fname:
        fname = fname + ".csv"
