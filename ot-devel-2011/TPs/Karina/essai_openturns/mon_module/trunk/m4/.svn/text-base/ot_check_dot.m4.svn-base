#                                               -*- Autoconf -*-
#
#  ot_check_dot.m4
#
#  (C) Copyright 2005-2007 EDF-EADS-Phimeca
#
#  This library is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 2.1 of the License.
#
#  This library is distributed in the hope that it will be useful
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public
#  License along with this library; if not, write to the Free Software
#  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307 USA
#
#  @author: $LastChangedBy$
#  @date:   $LastChangedDate: 2008-06-26 13:50:17 +0200 (Thu, 26 Jun 2008) $
#  Id:      $Id: ot_check_dot.m4 862 2008-06-26 11:50:17Z dutka $
#
#
#  This file is intended to be include in the configure.in file
#  of Open TURNS project to check whether Dot is available on the
#  build platform.
#
# OT_CHECK_DOT
# ------------
#
AC_DEFUN([OT_CHECK_DOT],
[
  WITH_DOT=0
  AC_ARG_VAR([DOT], [path for dot tool])
  AC_PATH_PROG([DOT], [dot])
  test x$DOT = x || WITH_DOT=1

  # Propagate test into atlocal
  AC_SUBST(WITH_DOT)

  # Propagate test into Makefiles
  AM_CONDITIONAL(WITH_DOT, test $WITH_DOT = 1)
])
