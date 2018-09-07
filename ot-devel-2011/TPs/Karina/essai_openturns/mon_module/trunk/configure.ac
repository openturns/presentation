#                                               -*- Autoconf -*-
#
#  configure.ac
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
#  @date:   $LastChangedDate: 2008-11-18 17:12:46 +0100 (Tue, 18 Nov 2008) $
#  Id:      $Id: configure.ac 1017 2008-11-18 16:12:46Z dutka $
#
#  Process this file with autoconf to produce a configure script.
#  Set minimal version of Autoconf for configure to work
#
AC_PREREQ([2.59])

# Initialize Autoconf
AC_INIT([OpenTURNS module 'UniformSphericalRandomVector'],
        [0.0.0],
        [bugs@openturns.org],
        [UniformSphericalRandomVector])

# Chooze our own configuration directory
AC_CONFIG_AUX_DIR([config])
AC_SUBST([ac_aux_dir])
AC_CONFIG_MACRO_DIR([m4])

# Initialize Automake
AM_INIT_AUTOMAKE([dist-bzip2 tar-ustar])

# Initialize Autotest
AC_CONFIG_TESTDIR([test])

# Chooze project source directory
AC_CONFIG_SRCDIR([src/UniformSphericalRandomVector.cxx])


# Propagate through source files the path of the installation directory
AC_DEFINE_UNQUOTED([INSTALL_PATH], "$prefix", [The path of installation])


# Detect debug option (Nota: change compilation flag value)
OT_DEBUG

# Proceed to required program detection
AC_LIBTOOL_DLOPEN # MUST be declared BEFORE AC_PROG_LIBTOOL
AC_PROG_LIBTOOL
AC_PROG_CXX
AC_PROG_CPP
AC_PROG_AWK
AC_PROG_INSTALL
AC_PROG_LN_S
AC_PROG_MAKE_SET

# Add some external flags to Libtool (ie, --silent)
LIBTOOL="${LIBTOOL} \$(LIBTOOL_FLAGS)"

# Check for typedefs, structures, and compiler characteristics
AC_HEADER_STDBOOL
# AC_C_CONST
AC_TYPE_SIZE_T
# AC_STRUCT_TM
AC_C_INLINE


# Proceed to required or optional program detection
# with our own macro files

# Check for Open TURNS library
OT_CHECK_OPENTURNS
#OT_CHECK_OPENTURNS_MODULES([extramod])

# Check for Python
OT_CHECK_PYTHON
#OT_CHECK_PYTHON_PACKAGES([qt rpy])

# Check for SWIG
SWIGFLAGS="`$OPENTURNS_CONFIG_SCRIPT --swigflags` $SWIGFLAGS"
OT_CHECK_SWIG([1.3.35])

# Check for Doxygen
OT_CHECK_DOXYGEN

# Check for Dot
OT_CHECK_DOT

SWIGFLAGS="$SWIGFLAGS $MOD_SWIGFLAGS"
CPPFLAGS="$CPPFLAGS $MOD_CPPFLAGS"
LDFLAGS="$LDFLAGS $MOD_LDFLAGS"
LIBS="$LIBS $MOD_LIBS"

# Propagate configuration into Makefile
AC_OUTPUT([Doxyfile
           Makefile
           CONF
           m4/Makefile
           config/Makefile
           src/Makefile
           python/Makefile
           test/Makefile
           test/atlocal
])

rc=0
#echo $OPENTURNS_MODULES | grep -q extramod && sum_ot_extramod=OK  || { sum_ot_extramod="no * (MANDATORY)"; rc=1; }
test "x$WITH_PYTHON" = x1             && sum_python=OK        || sum_python="no * (TUI not compiled)"
test "x$WITH_SWIG" = x1               && sum_swig=OK          || sum_swig="no * (only useful for developers)"
test "x$WITH_DOXYGEN" = x1            && sum_doxygen=OK       || sum_doxygen="no * (optional)"
test "x$WITH_DOT" = x1                && sum_dot=OK           || sum_dot="no * (optional)"


cat <<EOT

Summary:
========

EOT

# If you want to test for extra module 'extramod', remember to mention it in the summary
cat <<EOT > summary
(python)

 Debug level is ${DEBUG_LEVEL}

 Support for          is
 -----------------------------
  Python               ${sum_python}
  SWIG                 ${sum_swig}
  Doxygen              ${sum_doxygen}
  dot                  ${sum_dot}
EOT
cat summary

test $rc = 1 && exit $rc

cat <<EOT
Congratulations !
Now you can build Open TURNS as usual:
	make
	make check (optional but recommended)
	make install
	make installcheck (optional but recommended)

And if you find the output too verbose, try using the following options:
	make -s LIBTOOL_FLAGS=--silent

Have fun !
EOT
