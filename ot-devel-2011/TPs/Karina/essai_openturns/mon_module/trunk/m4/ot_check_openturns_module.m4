#                                               -*- Autoconf -*-
#
#  ot_check_openturns_module.m4
#
#  (C) Copyright 2009 EDF-EADS-Phimeca
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
# OT_CHECK_OPENTURNS_MODULES( OPENTURNS_MODULE_NAME )
# ---------------------------------------------------
#
AC_DEFUN([OT_CHECK_OPENTURNS_MODULES],
[
  AC_REQUIRE([OT_CHECK_OPENTURNS])
  _OT_CHECK_OPENTURNS_MODULES([$1])
  for ot_module_name in $1
  do
    AC_CACHE_CHECK([whether OpenTURNS has module ${ot_module_name}], [ot_cv_check_ot_module_${ot_module_name}],
                   [eval "ot_cv_check_ot_module_${ot_module_name}=no"
                    if $OPENTURNS_MODULE_SCRIPT --silent --module=${ot_module_name} >/dev/null 2>&1 
                    then
                       cmd2="ot_cv_check_ot_module_${ot_module_name}=yes"
                       eval "$cmd2"
                    fi
                   ])

    res=0
    if eval "test \"\${ot_cv_check_ot_module_${ot_module_name}}\" = yes"
    then
      res=1
      OPENTURNS_MODULES="$OPENTURNS_MODULES ${ot_module_name}"
      MOD_SWIGFLAGS="`$OPENTURNS_MODULE_SCRIPT --silent --module=${ot_module_name} --swigflags --cppflags` $MOD_SWIGFLAGS"
      MOD_CPPFLAGS="`$OPENTURNS_MODULE_SCRIPT --silent --module=${ot_module_name} --cppflags` $MOD_CPPFLAGS"
      MOD_LDFLAGS="`$OPENTURNS_MODULE_SCRIPT --silent --module=${ot_module_name} --ldflags` $MOD_LDFLAGS"
      MOD_LIBS="`$OPENTURNS_MODULE_SCRIPT --silent --module=${ot_module_name} --libs` $MOD_LIBS"
    fi

    AC_SUBST(OPENTURNS_MODULES)
    AC_DEFINE_UNQUOTED(AS_TR_CPP(HAVE_OT_MODULE_$ot_module_name), [$res])
  done
])


# _OT_CHECK_OPENTURNS_MODULES( OT_MODULE_NAME )
# ---------------------------------------------
#
m4_define([_OT_CHECK_OPENTURNS_MODULES],[dnl
  AC_FOREACH([OT_Module], [$1], 
  [AH_TEMPLATE(AS_TR_CPP(HAVE_OT_MODULE_[]OT_Module),
               [Define to 1 if OpenTURNS has module ]OT_Module[.])
  ])
])

