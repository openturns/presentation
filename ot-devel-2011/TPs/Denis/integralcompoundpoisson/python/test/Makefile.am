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
#  @author: $LastChangedBy$
#  @date:   $LastChangedDate$
#  Id:      $Id$
#
include $(top_srcdir)/config/common.am
include $(top_srcdir)/config/test.am


wrappersdir   = $(pkglibdir)/wrappers
samplesdir    = $(pkgdatadir)/examples
examplesdir   = $(pkgdatadir)/examples
etcbuilddir   = $(abs_top_builddir)/etc
etcinstalldir = $(prefix)/etc/openturns
INSTALLCHECK_TESTS_ENVIRONMENT = AUTOTEST_PATH=$(examplesdir) OPENTURNS_WRAPPER_PATH=$(wrappersdir) OPENTURNS_CONFIG_PATH=$(etcinstalldir) PYTHONPATH=$(pyexecdir) OPENTURNS_NUMERICALSAMPLE_PATH=$(samplesdir) OPENTURNS_PYTHON_SILENT=1
if WIN32
# set OPENTURNS_HOME for windows checktest under linux environment
INSTALLCHECK_TESTS_ENVIRONMENT += OPENTURNS_HOME=$(prefix)
endif



####################

#### Python test files

PYTHONINSTALLCHECK_TESTS = $(srcdir)/t_IntegralCompoundPoisson_validation.py

#### Out files

OUTFILES = $(srcdir)/t_IntegralCompoundPoisson_validation.expout

#### Python test sources

PYTHONINSTALLCHECK_PROGS = t_IntegralCompoundPoisson_validation.py

# We declare Python scripts with PYTHON primary (not SCRIPTS) in order
# to have them compiled at installation, but because Python scripts don't
# have the execute flag (chmod +x), we cheat it by forcing the system to
# use the SCRIPTS primary installation shell (SCRIPTS primary gives the
# execute flag but doen't compile the Python scripts !)
examples_PYTHON           = $(PYTHONINSTALLCHECK_PROGS)
# Install the test scripts in order to check openturns on windows.
if WIN32
examples_SCRIPTS          = $(PYTHONINSTALLCHECKTESTSUITE)
endif

EXTRA_DIST += CMakeLists.txt
