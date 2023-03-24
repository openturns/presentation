# -*- coding: utf-8 -*-

from openturns.coupling_tools import get_line_col

Y = get_line_col("get_line_col.txt", skip_line=6, skip_col=4)

print("Y:", Y)
