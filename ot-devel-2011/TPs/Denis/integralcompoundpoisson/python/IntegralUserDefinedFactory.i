// SWIG file IntegralUserDefinedFactory.i
// Author : $LastChangedBy$
// Date : $LastChangedDate: 2008-10-15 17:56:07 +0200 (Wed, 15 Oct 2008) $
// Id : $Id: IntegralUserDefinedFactory.i 972 2008-10-15 15:56:07Z dutka $

%{
#include "IntegralUserDefinedFactory.hxx"
%}

%include IntegralUserDefinedFactory.hxx

namespace IntegralCompoundPoisson
{
  %extend IntegralUserDefinedFactory
  {
    IntegralUserDefinedFactory(const IntegralUserDefinedFactory & other) { return new IntegralCompoundPoisson::IntegralUserDefinedFactory(other); }
  }
}
