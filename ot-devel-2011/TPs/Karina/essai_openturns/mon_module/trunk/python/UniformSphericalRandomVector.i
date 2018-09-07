// SWIG file openturnsUniformSphericalRandomVector.i
// Author : $LastChangedBy: dutka $
// Date : $LastChangedDate: 2008-08-28 17:36:47 +0200 (Thu, 28 Aug 2008) $
// Id : $Id: openturnsUniformSphericalRandomVector.i 916 2008-08-28 15:36:47Z dutka $

%module(docstring="Open TURNS UniformSphericalRandomVector module is an example on how to include new classes in Open TURNS") UniformSphericalRandomVector
%feature("autodoc","1");

%pythoncode %{
# Override the default SWIG function
def _swig_repr(self):
  return self.str()
%}

// Prerequisites needed
%include typemaps.i
%include exception.i

%import base_all.i
%import uncertainty_all.i

// The new classes
%{
#include "UniformSphericalRandomVector.hxx"
%}

%include UniformSphericalRandomVector.hxx
namespace OpenTURNS { namespace Uncertainty { namespace Model { %extend UniformSphericalRandomVector { UniformSphericalRandomVector(const UniformSphericalRandomVector & other) { return new OpenTURNS::Uncertainty::Model::UniformSphericalRandomVector(other); } } }}}
