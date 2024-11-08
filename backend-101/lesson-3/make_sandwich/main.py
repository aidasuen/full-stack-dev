# main.py
from utils import (
    open_fridge,
    find_butter,
    find_sausage,
    find_cheese,
    take_sausage,
    take_cheese,
    take_butter,
    put_on_table,
    close_fridge,
    open_breadbox,
    take_bread,
    take_butter_for_spread,
    spread_butter,
    take_sausage_for_slicing,
    slice_sausage,
    take_cheese_for_slicing,
    slice_cheese,
    put_on_bread,
    eat
)

def make_sandwich():
    open_fridge()
    find_butter()
    find_sausage()
    find_cheese()
    take_sausage()
    take_cheese()
    take_butter()
    put_on_table()
    close_fridge()
    open_breadbox()
    take_bread()
    take_butter_for_spread()
    spread_butter()
    take_sausage_for_slicing()
    slice_sausage()
    take_cheese_for_slicing()
    slice_cheese()
    put_on_bread()
    eat()

make_sandwich()
