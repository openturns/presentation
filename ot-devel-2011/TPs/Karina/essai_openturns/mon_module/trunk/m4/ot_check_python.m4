#                                               -*- Autoconf -*-
#
#  ot_check_python.m4
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
#  @date:   $LastChangedDate: 2007-09-25 12:38:48 +0200 (Tue, 25 Sep 2007) $
#  Id:      $Id: ot_check_python.m4 541 2007-09-25 10:38:48Z dutka $
#
#
#  This file is intended to be include in the configure.in file
#  of Open TURNS project to check whether Python is available on the
#  build platform.
#
# OT_CHECK_PYTHON
# ---------------
#
AC_DEFUN([OT_CHECK_PYTHON],
[#ac_save_CPPFLAGS="$CPPFLAGS"
AM_PATH_PYTHON

AC_SUBST([PYTHON_PREFIX],
         [`${PYTHON} -c "import sys; print sys.prefix"`] )

AC_SUBST([python_includedir],
         [`${PYTHON} -c "import sys; print sys.prefix + \"/include/python\" + str(sys.version_info[[0]]) + \".\" + str(sys.version_info[[1]])"`] )

AC_SUBST([python_libdir],
         [`${PYTHON} -c "import sys; print sys.prefix + \"/lib/python\" + str(sys.version_info[[0]]) + \".\" + str(sys.version_info[[1]]) + \"/m4\""`] )

AC_SUBST([python_version],
         [`${PYTHON} -c "import sys; print str(sys.version_info[[0]]) + \".\" + str(sys.version_info[[1]])"`] )

WITH_PYTHON=0
test -n "${PYTHON}" && WITH_PYTHON=1

# Propagate test into Makefiles
AM_CONDITIONAL(WITH_PYTHON, test $WITH_PYTHON = 1)
])
