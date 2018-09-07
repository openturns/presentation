#                                               -*- Autoconf -*-
#
#  ot_check_r_package.m4
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
#  @date:   $LastChangedDate: 2008-10-31 16:07:46 +0100 (Fri, 31 Oct 2008) $
#  Id:      $Id: ot_check_r_package.m4 996 2008-10-31 15:07:46Z dutka $
#
#
#  This file is intended to be include in the configure.in file
#  of Open TURNS project to check whether R has a given package
#
# OT_CHECK_R_PACKAGE( R_PACKAGE_NAME )
# ------------------------------------
#
AC_DEFUN([OT_CHECK_R_PACKAGE], [dnl
  AC_REQUIRE([OT_CHECK_R])
  _OT_CHECK_R_PACKAGE([$1])
  
  r_package_name=$1
  AC_CACHE_CHECK([whether R has package ${r_package_name}], [ot_cv_check_r_package_${r_package_name}],
                 [eval "ot_cv_check_r_package_${r_package_name}=no"
                  cmd1="echo 'library(${r_package_name})' | ${r_prog_path} --no-save --silent --no-readline"
                  if eval "$cmd1" >/dev/null 2>&1 
                  then
                     cmd2="ot_cv_check_r_package_${r_package_name}=yes"
                     eval "$cmd2"
                  fi
                 ])

  res=0
  eval "test \"\${ot_cv_check_r_package_${r_package_name}}\" = yes" && res=1

  AC_DEFINE_UNQUOTED(AS_TR_CPP(HAVE_R_PACKAGE_$r_package_name), [$res])
])


# _OT_CHECK_R_PACKAGE( R_PACKAGE_NAME )
# -------------------------------------
#
m4_define([_OT_CHECK_R_PACKAGE],[dnl
  AH_TEMPLATE(AS_TR_CPP(HAVE_R_PACKAGE_[]$1),
              [Define to 1 if R has package ]$1[.])
])
