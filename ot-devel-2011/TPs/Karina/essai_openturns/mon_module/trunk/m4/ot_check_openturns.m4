#                                               -*- Autoconf -*-
#
#  ot_check_openturns.m4
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
#  @date:   $LastChangedDate: 2008-09-22 11:34:11 +0200 (Mon, 22 Sep 2008) $
#  Id:      $Id: ot_check_openturns.m4 941 2008-09-22 09:34:11Z dutka $
#  serial   0.11.0
#
#
# This file is intended to be include in configure.in file
# of any project that embed Open TURNS. It allows the correct
# detection of Open TURNS by the embedding project without
# it knowing its intrinsics.
#
# OT_CHECK_OPENTURNS( [OPENTURNS_INSTALL_PATH = /usr] )
# -----------------------------------------------------
#
AC_DEFUN([OT_CHECK_OPENTURNS],
[
  AC_ARG_WITH([openturns],
              AC_HELP_STRING([--with-openturns=<path>],
                             [add Open TURNS support. <Path> should point to a actual install path of Open TURNS library and headers. If ommitted, assume that Open TURNS is installed in /usr, ie <path>=/usr. Default is to support Open TURNS.]),
              [], [withval=yes])

  WITH_OPENTURNS=0

  # saving values for compilation variables
  saved_CPPFLAGS=$CPPFLAGS
  saved_LDFLAGS=$LDFLAGS
  saved_LIBS=$LIBS

  openturns_default_path=m4_default([$1], /usr)
  if ! test x${withval} = xno
  then
    AC_CACHE_CHECK([for Open TURNS config script],  [ot_cv_openturns_config_script], [])
    AC_CACHE_CHECK([for Open TURNS module script],  [ot_cv_openturns_module_script], [])
    AC_CACHE_CHECK([for Open TURNS install path],  [ot_cv_openturns_install_path], [])
    AC_CACHE_CHECK([for Open TURNS include flags], [ot_cv_openturns_cppflags], [])
    AC_CACHE_CHECK([for Open TURNS library flags], [ot_cv_openturns_ldflags],  [])
    AC_CACHE_CHECK([for Open TURNS libraries],     [ot_cv_openturns_libs],     [])
    AC_CACHE_CHECK([for Open TURNS wrapper include flags], [ot_cv_openturns_wrapper_cppflags], [])
    AC_CACHE_CHECK([for Open TURNS wrapper library flags], [ot_cv_openturns_wrapper_ldflags],  [])
    AC_CACHE_CHECK([for Open TURNS wrapper library],       [ot_cv_openturns_wrapper_libs],     [])
    AC_CACHE_CHECK([for Open TURNS wrapper DTD path],      [ot_cv_openturns_wrapper_dtd_path], [])

    if test -z "$ot_cv_openturns_config_script" || test -z "$ot_cv_openturns_module_script" || test -z "$ot_cv_openturns_install_path" || test -z "$ot_cv_openturns_cppflags" || test -z "$ot_cv_openturns_ldflags" || test -z "$ot_cv_openturns_libs" || test -z "$ot_cv_openturns_wrapper_cppflags" || test -z "$ot_cv_openturns_wrapper_ldflags" || test -z "$ot_cv_openturns_wrapper_libs"
    then
      # we're trying to find the correct Open TURNS installation path
      openturns_install_path=$openturns_default_path
      test x${withval} = xyes || openturns_install_path=$withval

      # ask for Open TURNS support
      AC_PATH_PROGS([OPENTURNS_CONFIG_SCRIPT], [openturns-config], [false], [$openturns_install_path/bin])
      AC_PATH_PROGS([OPENTURNS_MODULE_SCRIPT], [openturns-module], [false], [$openturns_install_path/bin])

      if ! test x${OPENTURNS_CONFIG_SCRIPT} = xfalse
      then
        openturns_config_script=$OPENTURNS_CONFIG_SCRIPT
        openturns_module_script=$OPENTURNS_MODULE_SCRIPT
	openturns_install_path=`$OPENTURNS_CONFIG_SCRIPT --prefix`
        openturns_cppflags=`$OPENTURNS_CONFIG_SCRIPT --cppflags`
        openturns_ldflags=`$OPENTURNS_CONFIG_SCRIPT --ldflags`
        openturns_libs=`$OPENTURNS_CONFIG_SCRIPT --libs`
        openturns_wrapper_cppflags=`$OPENTURNS_CONFIG_SCRIPT --cppflags`
        openturns_wrapper_ldflags=`$OPENTURNS_CONFIG_SCRIPT --ldflags`
        openturns_wrapper_libs=`$OPENTURNS_CONFIG_SCRIPT --libs`
        openturns_wrapper_dtd_path=`$OPENTURNS_CONFIG_SCRIPT --wrapperdir`

      else
        AC_MSG_NOTICE([checking whether Open TURNS library and headers are here and working])

        AC_MSG_CHECKING([Open TURNS install path])
        test -d ${openturns_install_path} || AC_MSG_ERROR([$openturns_install_path: incorrect path])
        AC_MSG_RESULT([$openturns_install_path])

        AC_LANG_PUSH(C++)
        # we test the header file presence and usability
        openturns_cppflags="-I$openturns_install_path/include/openturns"
        CPPFLAGS="${CPPFLAGS} ${openturns_cppflags}"
        AC_CHECK_HEADER([OT.hxx],
                        [openturns_header_found=yes],
                        [openturns_header_found=no],
                        [])
        test x${openturns_header_found} = xno && AC_MSG_ERROR([Open TURNS include file NOT FOUND])

        # we test the library file presence and usability
        openturns_ldflags="-L$openturns_install_path/lib/openturns"
        openturns_libs="-lOT"
        LDFLAGS="${LDFLAGS} ${openturns_ldflags}"
        AC_CHECK_LIB([OT],
                     [openturns_library_ok],
                     [openturns_lib_found=yes],
                     [openturns_lib_found=no],
                     [])
        test x${openturns_lib_found} = xno && AC_MSG_ERROR([Open TURNS library NOT FOUND])
        AC_LANG_POP(C++)

        AC_LANG_PUSH(C)
        # we test the wrapper header file presence and usability
        openturns_wrapper_cppflags="-I$openturns_install_path/include/openturns"
        CPPFLAGS="${CPPFLAGS} ${openturns_wrapper_cppflags}"
        AC_CHECK_HEADER([WrapperCommon.h],
                        [openturns_wrapper_header_found=yes],
                        [openturns_wrapper_header_found=no],
                        [])
        test x${openturns_wrapper_header_found} = xno && AC_MSG_ERROR([Open TURNS wrapper include file NOT FOUND])

        openturns_wrapper_ldflags=
        openturns_wrapper_libs=
        AC_LANG_POP(C)

        # we look for the file wrapper.dtd to set its path
        for ot_dir in $openturns_install_path/share/openturns/wrappers
        do
          if test -f $ot_dir/wrapper.dtd
          then
            openturns_wrapper_dtd_path=$ot_dir
            break
          fi
        done
      fi

      # We write the values into the cache file
      OT_SET_OPENTURNS_CACHE_VALUES
    fi

    # we reset the values of Open TURNS flags from the cached values
    OPENTURNS_CONFIG_SCRIPT=$ot_cv_openturns_config_script
    OPENTURNS_MODULE_SCRIPT=$ot_cv_openturns_module_script
    AC_SUBST(OPENTURNS_CONFIG_SCRIPT)
    AC_SUBST(OPENTURNS_MODULE_SCRIPT)
    OPENTURNS_INSTALL_PATH=$ot_cv_openturns_install_path
    AC_SUBST(OPENTURNS_INSTALL_PATH)

    OPENTURNS_CPPFLAGS=$ot_cv_openturns_cppflags
    OPENTURNS_LDFLAGS=$ot_cv_openturns_ldflags
    OPENTURNS_LIBS=$ot_cv_openturns_libs
    AC_SUBST(OPENTURNS_CPPFLAGS)
    AC_SUBST(OPENTURNS_LDFLAGS)
    AC_SUBST(OPENTURNS_LIBS)

    OPENTURNS_WRAPPER_CPPFLAGS=$ot_cv_openturns_wrapper_cppflags
    OPENTURNS_WRAPPER_LDFLAGS=$ot_cv_openturns_wrapper_ldflags
    OPENTURNS_WRAPPER_LIBS=$ot_cv_openturns_wrapper_libs
    AC_SUBST(OPENTURNS_WRAPPER_CPPFLAGS)
    AC_SUBST(OPENTURNS_WRAPPER_LDFLAGS)
    AC_SUBST(OPENTURNS_WRAPPER_LIBS)

    OPENTURNS_WRAPPER_DTD_PATH=$ot_cv_openturns_wrapper_dtd_path
    AC_SUBST(OPENTURNS_WRAPPER_DTD_PATH)

    # after all tests are successful, we support Open TURNS
    WITH_OPENTURNS=1
    AC_MSG_NOTICE([Open TURNS support is OK])

  else
    # no Open TURNS support
    AC_MSG_NOTICE([No Open TURNS support])
  fi

  # Propagate test into Makefiles
  AM_CONDITIONAL(WITH_OPENTURNS, test $WITH_OPENTURNS = 1)

  # restoring saved values
  CPPFLAGS=$saved_CPPFLAGS
  LDFLAGS=$saved_LDFLAGS
  LIBS=$saved_LIBS

])

# OT_SET_OPENTURNS_CACHE_VALUES
# ------------------------------
#
AC_DEFUN([OT_SET_OPENTURNS_CACHE_VALUES],
[
  AC_CACHE_CHECK([for Open TURNS config script],  [ot_cv_openturns_config_script], [ot_cv_openturns_config_script=$openturns_config_script])
  AC_CACHE_CHECK([for Open TURNS module script],  [ot_cv_openturns_module_script], [ot_cv_openturns_module_script=$openturns_module_script])
  AC_CACHE_CHECK([for Open TURNS install path],  [ot_cv_openturns_install_path], [ot_cv_openturns_install_path=$openturns_install_path])
  AC_CACHE_CHECK([for Open TURNS include flags], [ot_cv_openturns_cppflags], [ot_cv_openturns_cppflags=$openturns_cppflags])
  AC_CACHE_CHECK([for Open TURNS library flags], [ot_cv_openturns_ldflags],  [ot_cv_openturns_ldflags=$openturns_ldflags])
  AC_CACHE_CHECK([for Open TURNS libraries],     [ot_cv_openturns_libs],     [ot_cv_openturns_libs=$openturns_libs])

  AC_CACHE_CHECK([for Open TURNS wrapper include flags], [ot_cv_openturns_wrapper_cppflags], [ot_cv_openturns_wrapper_cppflags=$openturns_wrapper_cppflags])
  AC_CACHE_CHECK([for Open TURNS wrapper library flags], [ot_cv_openturns_wrapper_ldflags],  [ot_cv_openturns_wrapper_ldflags=$openturns_wrapper_ldflags])
  AC_CACHE_CHECK([for Open TURNS wrapper library],       [ot_cv_openturns_wrapper_libs],     [ot_cv_openturns_wrapper_libs=$openturns_wrapper_libs])

  AC_CACHE_CHECK([for Open TURNS wrapper DTD path],      [ot_cv_openturns_wrapper_dtd_path], [ot_cv_openturns_wrapper_dtd_path=$openturns_wrapper_dtd_path])

])
