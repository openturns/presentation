#                                               -*- Autoconf -*-
#
#  ot_debug.m4
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
#  @date:   $LastChangedDate: 2008-12-05 12:54:09 +0100 (Fri, 05 Dec 2008) $
#  Id:      $Id: ot_debug.m4 1039 2008-12-05 11:54:09Z dutka $
#
#
#  This file is intended to be include in the configure.in file
#  of Open TURNS project to check whether debug statements should be included
#
# OT_DEBUG( level )
# -----------------
#
AC_DEFUN([OT_DEBUG],
[
  AC_ARG_ENABLE([debug],
                AC_HELP_STRING([--enable-debug@<:@=taglist@:>@], [Add debug information.
	                       Debugging can be specified as a comma separated tag list where tags can be: message, memory. Default is none.]),
			       [test x$enableval = xyes && enableval="message"], [enableval="message"])

  test x$enableval = xno && enableval="none"

  OT_CPPFLAGS=""
  OT_CFLAGS=""
  OT_FFLAGS=""
  OT_CXXFLAGS=""

  for flag in `echo $enableval| tr "," " "`
  do
    case $flag in
    message)
      OT_CPPFLAGS="$OT_CPPFLAGS -DDEBUG"
      OT_CFLAGS="$OT_CFLAGS -g"
      OT_FFLAGS="$OT_FFLAGS -g"
      OT_CXXFLAGS="$OT_CXXFLAGS -g"
      ;;

    memory)
      OT_CPPFLAGS="$OT_CPPFLAGS -DDEBUG_MEMORY"
      SWIGFLAGS="$SWIGFLAGS -DDEBUG_MEMORY"
      ;;

    none)
      ;;

    *)
      AC_MSG_ERROR([Debug option : invalid argument ($flag).])
      ;;
    esac
  done

  DEBUG_LEVEL=$enableval

  AC_SUBST(OT_CPPFLAGS)
  AC_SUBST(OT_CFLAGS)
  AC_SUBST(OT_FFLAGS)
  AC_SUBST(OT_CXXFLAGS)

  AC_MSG_NOTICE([Debug level is enableval])
])
