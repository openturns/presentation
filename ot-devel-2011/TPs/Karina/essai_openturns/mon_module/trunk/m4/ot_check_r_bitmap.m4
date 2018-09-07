#                                               -*- Autoconf -*-
#
#  ot_check_r_bitmap.m4
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
#  Id:      $Id: ot_check_r_bitmap.m4 996 2008-10-31 15:07:46Z dutka $
#
#
#  This file is intended to be include in the configure.in file
#  of Open TURNS project to check whether R can create bitmap
#
# OT_CHECK_R_BITMAP
# ------------------------------------
#
AC_DEFUN([OT_CHECK_R_BITMAP], [dnl
  AC_REQUIRE([OT_CHECK_R])

  
  AC_CACHE_CHECK([whether R can create bitmap], [ot_cv_check_r_bitmap],
                 [eval "ot_cv_check_r_bitmap=no"
                  cmd1="echo 'bitmap("test")' | ${r_prog_path} --no-save --silent --no-readline"
                  if eval "$cmd1" >/dev/null 2>&1 
                  then
                     cmd2="ot_cv_check_r_bitmap=yes"
                     eval "$cmd2"
                  fi
                 ])

  res=0
  eval "test \"\${ot_cv_check_r_bitmap\" = yes" && res=1
  if test $res = 0; then
    AC_MESSAGE_NOTICE([R cannot create bitmap. Check ghostscript (gs) installation and R configuration.])
  fi

  AC_DEFINE_UNQUOTED(HAVE_R_BITMAP, [$res])
])
