# ############################################################################

__license__ = \
	"""This file is part of the Wizium distribution (https://github.com/jsgonsette/Wizium).
	Copyright (c) 2019 Jean-Sebastien Gonsette.

	This program is free software : you can redistribute it and / or modify
	it under the terms of the GNU General Public License as published by
	the Free Software Foundation, version 3.

	This program is distributed in the hope that it will be useful, but
	WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.See the GNU
	General Public License for more details.

	You should have received a copy of the GNU General Public License
	along with this program.If not, see <http://www.gnu.org/licenses/>."""

__author__ = "Jean-Sebatien Gonsette"
__email__ = "jeansebastien.gonsette@gmail.com"

# ############################################################################

import os
import sys
import re
import platform
import random
import time
import functools
import operator
from libWizium import Wizium

# ############################################################################

PATH = './../Wizium/Binaries/Linux/libWizium.so'
# DICO_PATH = './../../Dictionaries/Fr_Simple.txt'
DICO_PATH = '/home/mooney/projects/crosswords/crosswords_v2/db/our_words.txt'


# ============================================================================
def draw (wiz):
    """Draw the grid content, with a very simple formating

    wiz     Wizium instance"""
# ============================================================================
    lines = wiz.grid_read ()
    for l in lines:
        print (''.join ([s + '   ' for s in l]))

def write_out(wiz, filename):
    lines = wiz.grid_read ()
    path = "./puzzles/"+filename+"/grid.txt"
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as output_file:
        for line in lines:
            output_file.write(line)


# ============================================================================
def set_grid_1 (wiz):
    """Set the grid skeleton with a pattern of black boxes

    wiz     Wizium instance"""
# ============================================================================

    tx = [0, 2, 3]

    wiz.grid_set_size (11,11)
    wiz.grid_set_box (5, 5, 'BLACK')

    for i in range (3):
        wiz.grid_set_box (tx [i], 5-tx [i], 'BLACK')
        wiz.grid_set_box (5+tx [i], tx [i], 'BLACK')
        wiz.grid_set_box (10-tx [i], 5+tx [i], 'BLACK')
        wiz.grid_set_box (5-tx [i], 10-tx [i], 'BLACK')

    wiz.grid_set_box (5, 1, 'BLACK')
    wiz.grid_set_box (5, 9, 'BLACK')



# ============================================================================
def load_dictionary (wiz, dico_path):
    """Load the dictionary content from a file

    wiz         Wizium instance
    dico_path   Path to the dictionary to load
    """
# ============================================================================

    # Read file content
    with open (dico_path, 'r') as f:
        words = f.readlines ()

    # Remove what is not a letter, if any
    words = [re.sub('[^a-zA-Z]+', '', s) for s in words]

    # Load dictionary
    wiz.dic_clear ()
    n = wiz.dic_add_entries (words)

    print ("Number of words: ")
    print (" - in file: ", len (words))
    print (" - added: ", n)
    print (" - final: ", wiz.dic_gen_num_words ())


# ============================================================================
def solve (wiz, max_black=0, heuristic_level=0, seed=0, black_mode='DIAG'):
    """Solve the grid

    wiz             Wizium instance
    max_black       Max number of black cases to add (0 if not allowed)
    heuristic_level Heuristic level (0 if deactivated)
    seed            Random Number Generator seed (0: take at random)
    """
# ============================================================================

    if not seed: seed = random.randint(1, 1000000)

    # Configure the solver
    wiz.solver_start (seed=seed, black_mode=black_mode, max_black=max_black, heuristic_level=heuristic_level)
    tstart = time.time ()

    # Solve with steps of 500ms max, in order to draw the grid content evolution
    while True:
        status = wiz.solver_step (max_time_ms=500)

        draw (wiz)
        print (status)

        if status.fillRate == 100:
            print ("SUCCESS !")
            break
        if status.fillRate == 0:
            print ("FAILED !")
            break

    # Ensure to release grid content
    wiz.solver_stop ()

    tend = time.time ()
    print ("Compute time: {:.01f}s".format (tend-tstart))

def example_1():
    # Create a Wizium instance
    wiz = Wizium (os.path.join (os.getcwd (), PATH))
    # Load the dictionary
    load_dictionary (wiz, DICO_PATH)

    set_grid_1 (wiz)
    solve (wiz, max_black=0, heuristic_level=2)


def winnie_puzzle(filename):
     # Create a Wizium instance
    wiz = Wizium (os.path.join (os.getcwd (), PATH))
    load_dictionary(wiz, DICO_PATH)
    # set_grid_5(wiz)
    print("about to solve")
    size = 8
    wiz.grid_set_size(size,size)
    solve(wiz, max_black=9, heuristic_level=2, black_mode="DIAG")
    write_out(wiz,filename)

# ============================================================================
"""Main"""
# ============================================================================

filename = sys.argv[1]
winnie_puzzle(filename)