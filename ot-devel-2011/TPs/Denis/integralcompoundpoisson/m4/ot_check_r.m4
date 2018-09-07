#                                               -*- Autoconf -*-
#
#  ot_check_r.m4
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
#  @date:   $LastChangedDate: 2008-10-31 16:07:46 +0100 (Fri, 31 Oct 2008) $
#  Id:      $Id: ot_check_r.m4 996 2008-10-31 15:07:46Z dutka $
#
#
#  This file is intended to be include in the configure.in file
#  of Open TURNS project to check whether R is available on the
#  build platform.
#
# OT_CHECK_R( [R_INSTALL_PATH = /usr], [R_NEW_NAME = R] )
# -------------------------------------------------------
#
AC_DEFUN([OT_CHECK_R],
[AC_ARG_WITH([R],
    AC_HELP_STRING([--with-R@<:@=DIR@:>@], [add R support. @<:@]m4_default([$1], /usr)[@:>@]),
    [], [withval=yes])

 AC_ARG_ENABLE([R-renaming],
    AC_HELP_STRING([--enable-R-renaming@<:@=NEWNAME@:>@], [change the name of R executable. @<:@]m4_default([$2], R)[@:>@]),
    [], [enableval=no])

  WITH_R=0

  # saving values for compilation variables
  saved_CPPFLAGS=$CPPFLAGS
  saved_LDFLAGS=$LDFLAGS
  saved_LIBS=$LIBS
  saved_PATH=$PATH

  # change the name of R executable
  r_default_name=m4_default([$2], R)
  r_name=${r_default_name}
  test ! x${enableval} = xno && r_name=${enableval}


  r_default_path=m4_default([$1], /usr)
  if test ! x${withval} = xno
  then
    # ask for R support
    AC_MSG_NOTICE([checking whether R is here and working])

    # we're trying to find the correct R installation path
    r_install_path=$r_default_path
    if test ! x${withval} = xyes
    then
      r_install_path=$withval
      PATH="${r_install_path}/bin:${PATH}"
    fi

    # check R program location
    AC_PATH_PROG([r_prog_path], [${r_name}], [no])
    test x${r_prog_path} = xno && AC_MSG_ERROR([${r_name} program NOT FOUND])

    # after all tests are successful, we support R
    WITH_R=1
    AC_MSG_NOTICE([R support is OK])

    # Propagate values into source files
    AC_DEFINE_UNQUOTED([R_EXECUTABLE_PATH], "${r_prog_path}", [The path to the R executable])

  else
    # no R support
    AC_MSG_NOTICE([No R support])
  fi

  # Propagate test into Makefiles
  AM_CONDITIONAL(WITH_R, test $WITH_R = 1)

  # restoring saved values
  CPPFLAGS=$saved_CPPFLAGS
  LDFLAGS=$saved_LDFLAGS
  LIBS=$saved_LIBS
  PATH=$saved_PATH

])
