#                                               -*- Makefile -*-
#
#  Makefile.am
#
#  (C) Copyright 2011 EDF-EADS-Phimeca
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
#
include $(top_srcdir)/config/common.am
include $(top_srcdir)/config/test.am


AM_CPPFLAGS += -I$(top_srcdir)/test -I$(top_srcdir)/src
AM_CPPFLAGS += $(OPENTURNS_CPPFLAGS)
AM_LDFLAGS = $(OPENTURNS_LDFLAGS) $(OPENTURNS_LIBS) ../src/libOTIntegralCompoundPoisson.la

CHECK_TESTS += $(srcdir)/t_IntegralUserDefined_std.at
CHECK_TESTS += $(srcdir)/t_IntegralUserDefinedFactory_std.at
CHECK_TESTS += $(srcdir)/t_IntegralCompoundPoisson_std.at

OUTFILES = $(srcdir)/t_IntegralUserDefined_std.expout
OUTFILES = $(srcdir)/t_IntegralUserDefined_stdFactory.expout
OUTFILES = $(srcdir)/t_IntegralCompoundPoisson_std.expout

CHECK_PROGS += t_IntegralUserDefined_std
CHECK_PROGS += t_IntegralUserDefinedFactory_std
CHECK_PROGS += t_IntegralCompoundPoisson_std

t_IntegralUserDefined_std_SOURCES = t_IntegralUserDefined_std.cxx
t_IntegralUserDefinedFactory_std_SOURCES = t_IntegralUserDefinedFactory_std.cxx
t_IntegralCompoundPoisson_std_SOURCES = t_IntegralCompoundPoisson_std.cxx

noinst_PROGRAMS = $(CHECK_PROGS) $(INSTALLCHECK_PROGS)

CHECK_TESTS_ENVIRONMENT = OPENTURNS_WRAPPER_PATH=$(builddir) OPENTURNS_CONFIG_PATH=$(etcbuilddir)
INSTALLCHECK_TESTS_ENVIRONMENT = AUTOTEST_PATH=$(examplesdir) OPENTURNS_WRAPPER_PATH=$(wrappersdir) OPENTURNS_CONFIG_PATH=$(etcinstalldir) OPENTURNS_NUMERICALSAMPLE_PATH=$(samplesdir)


