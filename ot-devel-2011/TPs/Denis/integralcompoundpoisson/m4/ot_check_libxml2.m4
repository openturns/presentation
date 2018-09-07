#                                               -*- Autoconf -*-
#
#  ot_check_libxml2.m4
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
#  @author: $LastChangedBy: dutka $
#  @date:   $LastChangedDate: 2008-06-26 13:50:17 +0200 (Thu, 26 Jun 2008) $
#  Id:      $Id: ot_check_libxml2.m4 862 2008-06-26 11:50:17Z dutka $
#
#
#  This file is intended to be include in the configure.in file
#  of Open TURNS project to check whether reguler expressions are 
#  available on the platform.
#
# OT_CHECK_LIBXML2([ DIR = /usr ])
# --------------------------------
#
AC_DEFUN([OT_CHECK_LIBXML2],
[
 AC_ARG_WITH([libxml2],
  AC_HELP_STRING([--with-libxml2@<:@=DIR@:>@], [add XML support. @<:@]m4_default([$1], /usr)[@:>@]),
                 [], [withval=yes])

  WITH_LIBXML2=0

  # saving values for compilation variables
  saved_CPPFLAGS=$CPPFLAGS
  saved_LDFLAGS=$LDFLAGS
  saved_LIBS=$LIBS

  libxml2_default_path=m4_default([$1], /usr)
  if ! test x${withval} = xno
  then
    # we're trying to find the correct Libxml2 installation path
    libxml2_install_path=$libxml2_default_path
    test x${withval} = xyes || libxml2_install_path=$withval

    AC_MSG_CHECKING([libxml2 install path])
    test -d ${libxml2_install_path} || AC_MSG_ERROR([$libxml2_install_path: incorrect path])
    AC_MSG_RESULT([$libxml2_install_path])



    # we test the header file presence and usability
    libxml2_include_path=$libxml2_install_path/include/libxml2
    LIBXML2_CPPFLAGS="-I${libxml2_include_path}"
    CPPFLAGS="${CPPFLAGS} ${LIBXML2_CPPFLAGS}"
    AC_LANG_PUSH(C)
    AC_CHECK_HEADERS([libxml/parser.h],
                     [libxml2_header_found=yes],
                     [libxml2_header_found=no],
                     [])
    AC_LANG_POP(C)
    test x${libxml2_header_found} = xno && AC_MSG_ERROR([Libxml2 include file NOT FOUND])
    AC_SUBST(LIBXML2_CPPFLAGS)

    # we test the library file presence and usability
    libxml2_lib_path=$libxml2_install_path/lib
    libxml2_lib_name=xml2
    LIBXML2_LDFLAGS="-L${libxml2_lib_path}"
    LIBXML2_LIBS="-l${libxml2_lib_name}"
    LDFLAGS="${LDFLAGS} ${LIBXML2_LDFLAGS}"
    LIBS="${LIBS} ${LIBXML2_LIBS}"
    AC_SEARCH_LIBS([xmlParseDoc], [$libxml2_lib_name], [libxml2_lib_found=yes], [libxml2_lib_found=no])
    test x${libxml2_lib_found} = xno && AC_MSG_ERROR([Libxml2 library NOT FOUND])
    AC_SUBST(LIBXML2_LDFLAGS)
    AC_SUBST(LIBXML2_LIBS)



    # after all tests are successful, we support Libxml2
    WITH_LIBXML2=1
    AC_MSG_NOTICE([Libxml2 support is OK])

    # Propagate test into source files
    AC_DEFINE(HAVE_LIBXML2, 1, [Support for regular expression library])

  else
    # no Libxml2 support
    AC_MSG_NOTICE([No Libxml2 support])
  fi

  # Propagate test into atlocal
  AC_SUBST(WITH_LIBXML2)

  # Propagate test into Makefiles...
  AM_CONDITIONAL(WITH_LIBXML2, test $WITH_LIBXML2 = 1)

  # restoring saved values
  CPPFLAGS=$saved_CPPFLAGS
  LDFLAGS=$saved_LDFLAGS
  LIBS=$saved_LIBS

])
