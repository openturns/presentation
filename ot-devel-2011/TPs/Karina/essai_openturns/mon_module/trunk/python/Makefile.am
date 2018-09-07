#                                               -*- Makefile -*-
#
#  Makefile.am
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
#  @date:   $LastChangedDate: 2009-01-16 13:58:07 +0100 (Fri, 16 Jan 2009) $
#  Id:      $Id: Makefile.am 1068 2009-01-16 12:58:07Z dutka $
#
include $(top_srcdir)/config/common.am

AM_CPPFLAGS += -I$(top_srcdir)/src
AM_CPPFLAGS += $(OPENTURNS_CPPFLAGS)
AM_CPPFLAGS += -DSWIG_TYPE_TABLE=openturns

BUILT_SOURCES             =
pkgpython_PYTHON          =
pkgpyexec_LTLIBRARIES     =
MAINTAINERCLEANFILES      = $(BUILT_SOURCES) UniformSphericalRandomVector.py
EXTRA_DIST                = UniformSphericalRandomVector.pth

python_DATA = UniformSphericalRandomVector.pth

## Python module : UniformSphericalRandomVector

BUILT_SOURCES            +=  UniformSphericalRandomVector_wrap.cpp
pkgpython_PYTHON         +=  UniformSphericalRandomVector.py
pkgpyexec_LTLIBRARIES    += _UniformSphericalRandomVector.la
EXTRA_DIST               += $(OPENTURNS_SWIG_SRC)

_UniformSphericalRandomVector_la_LDFLAGS      = -module -no-undefined
#_UniformSphericalRandomVector_la_LDFLAGS     += $(OPENTURNS_LDFLAGS)
_UniformSphericalRandomVector_la_LIBADD       = ../src/libOTUniformSphericalRandomVector.la
#_UniformSphericalRandomVector_la_LIBADD      += $(OPENTURNS_LIBS)
_UniformSphericalRandomVector_la_CPPFLAGS     = $(SWIG_PYTHON_CPPFLAGS)
_UniformSphericalRandomVector_la_CPPFLAGS    += $(PYTHON_CPPFLAGS)
_UniformSphericalRandomVector_la_CPPFLAGS    += $(AM_CPPFLAGS)
_UniformSphericalRandomVector_la_CXXFLAGS     = $(AM_CXXFLAGS)
_UniformSphericalRandomVector_la_SOURCES      = UniformSphericalRandomVector_wrap.cpp $(OPENTURNS_SWIG_SRC)

pkgswig_DATA = $(OPENTURNS_SWIG_SRC)

OPENTURNS_SWIG_SRC   = \
	UniformSphericalRandomVector.i

OPENTURNS_WRAPPER_DEPEND =
# OPENTURNS_WRAPPER_DEPEND = \
# 	UniformSphericalRandomVector.hxx

UniformSphericalRandomVector.py : UniformSphericalRandomVector_wrap.cpp
UniformSphericalRandomVector_wrap.cpp : $(OPENTURNS_SWIG_SRC) $(OPENTURNS_WRAPPER_DEPEND)
	@echo "*** INFO: This may take a while. Be patient..."
	(rm -f UniformSphericalRandomVector.py UniformSphericalRandomVector_wrap.cpp && \
	$(SWIG) $(SWIG_PYTHON_OPT) $(AM_CPPFLAGS) -I$(otswigdir) $(SWIGFLAGS) -o $@.tmp $< && \
	mv $@.tmp $@)

