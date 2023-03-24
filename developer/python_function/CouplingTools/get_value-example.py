# -*- coding: utf-8 -*-
# Copyright (C) - 2013 - Michael Baudin - EDF R&D

from openturns.coupling_tools import get_value

filename = "results.txt"
# 1. search token, the value right after the token
# is returned:
Y = get_value(filename, token="Y1=")  # 11.11
print("(1) Y:", Y)

# 2. skip lines and columns (useful for array search):
Y = get_value(filename, skip_line=1, skip_col=2)  # 9
print("(2) Y:", Y)

# 3. skip lines and columns backward (be careful:
# if there is an empty line at the end of the file,
# it is taken into account. i.e. this last empty line
# will be reached using skip\_line=-1):
Y = get_value(filename, skip_line=-2, skip_col=-2)  # 201
print("(3) Y:", Y)

# 4. search the 3rd appearance of the token:
Y = get_value(filename, token="Y1=", skip_token=2)  # 33.33
print("(4) Y:", Y)

# 5. search the 2nd appearance of the token from the end
# of the file:
Y = get_value(filename, token="Y1=", skip_token=-2)  # 22.22
print("(5) Y:", Y)

# 6. search a token and then skip lines and columns from
# this token:
Y = get_value(filename, token="Y1=", skip_line=5, skip_col=-2)  # 101
print("(6) Y:", Y)

# 7. search the 2nd token and then skip lines and columns
# from this token:
Y = get_value(filename, token="Y1=", skip_token=1, skip_line=5, skip_col=1)  # 300
print("(7) Y:", Y)
