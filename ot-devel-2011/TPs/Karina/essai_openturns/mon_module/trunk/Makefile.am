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

# When rebuilding, tell aclocal where to find additional macros
ACLOCAL_AMFLAGS = -I m4

SUBDIRS      = config m4 src python test
DIST_SUBDIRS = config m4 src python test

dist_doc_DATA = \
	README \
	INSTALL \
	TODO \
	NEWS \
	AUTHORS \
	ChangeLog \
	COPYING


MAINTAINERCLEANFILES = \
	Makefile.in \
	aclocal.m4 \
	configure \
	config-h.in \
	stamp-h.in \
	config.cache \
	config.h.in \
	config.log \
	config.status

DISTCLEANFILES = summary
CLEANFILES     = Doxygen.log FLAGS

EXTRA_DIST = Doxyfile CONF

$(ac_aux_dir)/package.m4: $(top_srcdir)/configure.ac

all-local:
	: > FLAGS
	echo "swigflags: -I$(pkgswigdir)" >> FLAGS
	echo "cppflags: -I$(pkgincludedir)" >> FLAGS
	echo "ldflags: -L$(pkglibdir)" >> FLAGS
	echo "libs: -lOTmon_module_0" >> FLAGS

if WITH_DOXYGEN
if WITH_DOT
html-am : Doxyfile
	@DOXYGEN@ $(builddir)/Doxyfile
endif
endif
