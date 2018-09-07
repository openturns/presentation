// SWIG file IntegralCompoundPoisson.i
// Author : $LastChangedBy$
// Date : $LastChangedDate: 2008-10-15 17:56:07 +0200 (Wed, 15 Oct 2008) $
// Id : $Id: IntegralCompoundPoisson.i 972 2008-10-15 15:56:07Z dutka $

%{
#include "IntegralCompoundPoisson.hxx"
%}

%include IntegralCompoundPoisson.hxx


namespace IntegralCompoundPoisson { %extend IntegralCompoundPoisson { IntegralCompoundPoisson(const IntegralCompoundPoisson & other) { return new IntegralCompoundPoisson::IntegralCompoundPoisson(other); } } }
