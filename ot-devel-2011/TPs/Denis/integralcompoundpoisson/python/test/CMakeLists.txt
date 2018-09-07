#                                               -*- cmake -*-
#
#  CMakeLists.txt
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
#  @author: $LastChangedBy: dutka $
#  @date:   $LastChangedDate: 2010-02-04 16:44:49 +0100 (Thu, 04 Feb 2010) $
#  Id:      $Id: Makefile.am 1473 2010-02-04 15:44:49Z dutka $
#

cmake_minimum_required ( VERSION 2.8 )

#include ( CTest )

set ( NEW_PATH "$ENV{PATH}:${EXAMPLE_PATH}" )

set ( PYINSTALLCHECK_ENVIRONMENT "OPENTURNS_WRAPPER_PATH=${WRAPPER_PATH}"
                                 "OPENTURNS_CONFIG_PATH=${SYSCONFIG_PATH}/openturns"
				 "OPENTURNS_NUMERICALSAMPLE_PATH=${SAMPLE_PATH}"
				 "PATH=${NEW_PATH}"
				 "PYTHONPATH=${PYTHON_MODULE_PATH}"
    )

# This macro compiles on the fly and run the corresponding post-installation test
# It can have two optional arguments PRE and POST followed by some shell command to be run
# before or after the test if needed
# PRE and POST options cn be repeated many times: the arguments will be run one after the other
# in the order of appearence. If one fails, the whole command fails.
set ( PYINSTALLCHECK_TO_BE_RUN )
macro ( ot_pyinstallcheck_test TESTNAME )
  set ( TESTNAME_TGT t_${TESTNAME} )
  set ( TESTNAME_SRC ${TESTNAME_TGT}.py )
  set ( TESTNAME_OUT ${TESTNAME_TGT}.expout )
  get_source_file_property ( OUTFILE_LOC ${TESTNAME_OUT} LOCATION )
  #add_executable ( ${TESTNAME_TGT} EXCLUDE_FROM_ALL ${TESTNAME_SRC} )
  #target_link_libraries ( ${TESTNAME_TGT} OT )
  get_source_file_property ( TESTNAME_LOC ${TESTNAME_SRC} LOCATION )

  set ( _CMD )
  set ( _PRE )
  set ( _POST )
  set ( _IGNOREOUT OFF )
  foreach ( _ARG ${ARGN} )
    string ( TOUPPER ${_ARG} ARG )
    if ( ${ARG} MATCHES PRE )
      set ( _CMD PRE )
    elseif ( ${ARG} MATCHES POST )
      set ( _CMD POST )
    elseif ( ${ARG} MATCHES IGNOREOUT )
      set ( _IGNOREOUT ON )
    else ( ${ARG} MATCHES PRE )
      if ( ${_CMD} MATCHES PRE )
	set ( _PRE "${_PRE} ${_ARG} && " )
      elseif ( ${_CMD} MATCHES POST )
	set ( _POST "${_POST} && ${_ARG}" )
      endif  ( ${_CMD} MATCHES PRE )
      set ( _CMD )
    endif ( ${ARG} MATCHES PRE )
  endforeach ( _ARG )

  if (_IGNOREOUT)
    set ( COMMAND "( ${PYTHON_EXECUTABLE} ${TESTNAME_LOC} > /dev/null )" )
  else (_IGNOREOUT)
    set ( COMMAND "( ${PYTHON_EXECUTABLE} ${TESTNAME_LOC} > ${CMAKE_CURRENT_BINARY_DIR}/${TESTNAME_TGT}.out ) && diff -u ${OUTFILE_LOC} ${CMAKE_CURRENT_BINARY_DIR}/${TESTNAME_TGT}.out" )
  endif (_IGNOREOUT)

  if (_PRE OR _POST)
    add_test ( pyinstallcheck_${TESTNAME} "sh" "-c" "${_PRE}${COMMAND}${_POST}" )
  else (_PRE OR _POST)
    add_test ( pyinstallcheck_${TESTNAME} "sh" "-c" "${COMMAND}" )
  endif (_PRE OR _POST)
  set_tests_properties ( pyinstallcheck_${TESTNAME} PROPERTIES ENVIRONMENT "${PYINSTALLCHECK_ENVIRONMENT}" )
  list ( APPEND PYINSTALLCHECK_TO_BE_RUN ${TESTNAME_SRC} )
endmacro ( ot_pyinstallcheck_test )


## Python post-installation tests

ot_pyinstallcheck_test ( ComparisonOperator_std )

add_custom_target ( pyinstallcheck COMMAND ${CMAKE_CTEST_COMMAND} -R "^pyinstallcheck_"
                    DEPENDS ${PYINSTALLCHECK_TO_BE_RUN}
		    COMMENT "Run Python post-installation tests"  )

