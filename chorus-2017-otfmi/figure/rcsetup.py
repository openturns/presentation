# -*- coding: utf-8 -*-
from graph import color as co
co.set_color_cycle(co.list_sgd_b)

# The default page size in a beamer presentation is 12.8cm x 9.6cm
# (a 4:3 aspect ratio) with a font size of 11pt.

_font_size = 9.0
rcParams["font.size"] = _font_size
rcParams["axes.labelsize"] = _font_size
rcParams["axes.linewidth"] = 1. / 2.
rcParams["lines.linewidth"] = 1. / 1.5
rcParams["patch.linewidth"] = 1. / 1.5
rcParams["axes.titlesize"] = _font_size
rcParams["legend.fontsize"] = _font_size
rcParams["xtick.labelsize"] = _font_size
rcParams["ytick.labelsize"] = _font_size

rcParams["savefig.bbox"] = "tight"
# rcParams["figure.figsize"] = [5.04, 3.025]
rcParams["figure.figsize"] = [6.16, 3.697]
rcParams["font.family"] = ["sans-serif"]

rcParams["text.usetex"] = False
rcParams["text.latex.unicode"] = False

rcParams["text.latex.preamble"] = [
    # "\usepackage[utf8]{inputenc}",
    # "\usepackage[T1]{fontenc}",
    "\usepackage{lmodern}",
    "\usepackage{amsmath}", "\usepackage{amsfonts}",
    "\usepackage{amssymb}", "\usepackage{amsthm}",
    "\usepackage{siunitx}"]
