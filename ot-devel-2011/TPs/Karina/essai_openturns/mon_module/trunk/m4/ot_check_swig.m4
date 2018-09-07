#                                               -*- Autoconf -*-
#
#  ot_check_swig.m4
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
#  @author: $LastChangedBy: dutka $
#  @date:   $LastChangedDate: 2009-02-03 18:25:52 +0100 (mar, 03 fév 2009) $
#  Id:      $Id: ot_check_swig.m4 1102 2009-02-03 17:25:52Z dutka $
#
#
#  This file is intended to be include in the configure.in file
#  of Open TURNS project to check whether R is available on the
#  build platform.
#
# OT_CHECK_SWIG( version, path = /usr )
# -------------------------------------
#
AC_DEFUN([OT_CHECK_SWIG],
[
  AC_ARG_WITH([swig],
    AC_HELP_STRING([--with-swig@<:@=DIR@:>@], [set SWIG installation directory. @<:@]m4_default([$2], /usr)[@:>@]),
    [], [withval=no])


  AC_ARG_VAR([SWIGFLAGS],[The list of flags that should be passed to SWIG.])

  WITH_SWIG=0

  SWIG='noswig() { echo "error: SWIG not available. Check configuration." ; return 1 ; } ; noswig'

  swig_default_path=m4_default([$2], /usr)
  if test ! x${withval} = xno
  then
    # we're trying to find the correct SWIG installation path
    swig_install_path=$swig_default_path
    if test ! x${withval} = xyes
    then
      swig_install_path=$withval
      PATH="${swig_install_path}/bin:${PATH}"
    fi

    AC_PROG_SWIG(m4_default([$1], 1.3.35))
    if test $ac_prog_swig_res = "ok" 
    then
      SWIG_ENABLE_CXX
      #SWIG_MULTI_MODULE_SUPPORT
      SWIG_PYTHON

      #test -n "${SWIG}" && WITH_SWIG=1
      eval "${SWIG} -help >/dev/null 2>&1" && WITH_SWIG=1
    fi
  fi

  AC_SUBST(SWIG)

  # Propagate test into Makefiles
  AM_CONDITIONAL(WITH_SWIG, test $WITH_SWIG = 1)
])

# _OT_SWIG_VERSION
# ----------------
#
AC_DEFUN([_OT_SWIG_VERSION],
[
  AC_REQUIRE([AC_PROG_AWK])
  AC_MSG_CHECKING([Swig version])
  ot_swig_version="undefined"
  if ${SWIG} -version >conftest.swigversion 2>&1; then
    ot_swig_version=`grep Version conftest.swigversion | cut -d " " -f 3`
  fi
  AC_MSG_RESULT([$ot_swig_version])
])
