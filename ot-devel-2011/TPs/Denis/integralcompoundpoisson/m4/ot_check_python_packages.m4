#                                               -*- Autoconf -*-
#
#  ot_check_python_packages.m4
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
#  Id:      $Id: ot_check_python_packages.m4 862 2008-06-26 11:50:17Z dutka $
#
#
#  This file is intended to be include in the configure.in file
#  of Open TURNS project to check whether R has a given package
#
# OT_CHECK_PYTHON_PACKAGES( PYTHON_PACKAGE_NAME )
# -----------------------------------------------
#
AC_DEFUN([OT_CHECK_PYTHON_PACKAGES], [dnl
  AC_REQUIRE([OT_CHECK_PYTHON])
  _OT_CHECK_PYTHON_PACKAGES([$1])
  for python_package_name in $1
  do
    AC_CACHE_CHECK([whether Python has package ${python_package_name}], [ot_cv_check_python_package_${python_package_name}],
                   [eval "ot_cv_check_python_package_${python_package_name}=no"
                    cmd1="echo 'from ${python_package_name} import *' | ${PYTHON}"
		    pkg=`echo ${python_package_name} | tr "[a-z]" "[A-Z]"`
		    cmd3="WITH_PYTHON_${pkg}=0"
                    if eval "$cmd1" >/dev/null 2>&1 
                    then
                       cmd2="ot_cv_check_python_package_${python_package_name}=yes"
                       eval "$cmd2"
		       cmd3="WITH_PYTHON_${pkg}=1"
                    fi
		    eval "$cmd3"
                   ])

    res=0
    eval "test \"\${ot_cv_check_python_package_${python_package_name}}\" = yes" && res=1

    AC_DEFINE_UNQUOTED(AS_TR_CPP(HAVE_PYTHON_PACKAGE_$python_package_name), [$res])
  done
])


# _OT_CHECK_PYTHON_PACKAGES( PYTHON_PACKAGE_NAME )
# ------------------------------------------------
#
m4_define([_OT_CHECK_PYTHON_PACKAGES],[dnl
  AC_FOREACH([OT_Package], [$1], 
  [AH_TEMPLATE(AS_TR_CPP(HAVE_PYTHON_PACKAGE_[]OT_Package),
               [Define to 1 if Python has package ]OT_Package[.])
  ])
])
