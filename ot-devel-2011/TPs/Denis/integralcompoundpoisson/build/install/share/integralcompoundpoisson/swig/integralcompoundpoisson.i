// SWIG file openturnsintegralcompoundpoisson.i
// Author : $LastChangedBy$
// Date : $LastChangedDate: 2008-08-28 17:36:47 +0200 (Thu, 28 Aug 2008) $
// Id : $Id: openturnsintegralcompoundpoisson.i 916 2008-08-28 15:36:47Z dutka $

%module(docstring="Open TURNS IntegralCompoundPoisson module is an example on how to include new classes in Open TURNS") integralcompoundpoisson
%feature("autodoc","1");

%pythoncode %{
# Override the default SWIG function
def _swig_repr(self):
  return self.str()
%}

%{
#include "OTconfig.hxx"
#include "OTCommon.hxx"
#include "OTType.hxx"
#include "OTStat.hxx"
#include "OTGraph.hxx"
#include "PythonWrappingFunctions.hxx"
%}

// Prerequisites needed
%include typemaps.i
%include exception.i

%import base.i
%import uncertainty.i

// The new classes
%include IntegralUserDefined.i
%include IntegralUserDefinedFactory.i
%include IntegralCompoundPoisson.i
