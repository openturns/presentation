#                                               -*- Autoconf -*-
#
#  ot_check_win32.m4
#
#  (C) Copyright 2005-2010 EDF-EADS-Phimeca
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
#  @date:   $LastChangedDate: 2009-01-20 09:35:13 +0100 (mar, 20 jan 2009) $
#  Id:      $Id: ot_check_r.m4 1072 2009-01-20 08:35:13Z souchaud $
#
#
#  This file is intended to be include in the configure.in file
#  of Open TURNS project to check whether the target is a win32 platform.
#
# OT_CHECK_WIN32
# -------------------------------------------------------
#

AC_DEFUN([OT_CHECK_WIN32],
[
  win32=0

  case $host in
  *-*-cygwin* | *-*-mingw* | *-*-pw32*)
    AC_MSG_NOTICE([Win32 target detected])
    win32=1
    ;;
  esac

  # Propagate windows flag into Makefiles
  AM_CONDITIONAL([WIN32], [test x$win32 = x1])

  # Propagate test into atlocal
  AC_SUBST(win32)

  
  temporary_directory="/tmp"
  if test x$win32 = x1
  then
    temporary_directory="C:\\OpenTURNS\\tmp"
  fi
  # Propagate test into atlocal
  AC_SUBST(temporary_directory)


  # prefix for windows target
  win32_prefix="c:/openturns"

  # Propagate test into atlocal
  AC_SUBST(win32_prefix)

])



