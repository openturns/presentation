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
#  @date:   $LastChangedDate: 2008-12-18 14:14:36 +0100 (Thu, 18 Dec 2008) $
#  Id:      $Id: Makefile.am 1046 2008-12-18 13:14:36Z dutka $
#
include $(top_srcdir)/config/common.am

pkginclude_HEADERS = \
	UniformSphericalRandomVector.hxx

pkglib_LTLIBRARIES         = libOTUniformSphericalRandomVector.la
libOTUniformSphericalRandomVector_la_CXXFLAGS  = $(AM_CXXFLAGS)
libOTUniformSphericalRandomVector_la_CXXFLAGS += $(OPENTURNS_CPPFLAGS)
libOTUniformSphericalRandomVector_la_LDFLAGS   = -no-undefined
libOTUniformSphericalRandomVector_la_LDFLAGS  += $(OPENTURNS_LDFLAGS)
libOTUniformSphericalRandomVector_la_LIBADD    = $(OPENTURNS_LIBS)
libOTUniformSphericalRandomVector_la_SOURCES   = \
	UniformSphericalRandomVector.cxx
