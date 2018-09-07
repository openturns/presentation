// SWIG file IntegralUserDefined.i
// Author : $LastChangedBy$
// Date : $LastChangedDate: 2008-10-15 17:56:07 +0200 (Wed, 15 Oct 2008) $
// Id : $Id: IntegralCompoundPoisson.i 972 2008-10-15 15:56:07Z dutka $

%{
#include "IntegralUserDefined.hxx"
%}

// %template(UnsignedLongCollection_) OpenTURNS::Base::Type::Collection<OpenTURNS::NumericalScalar>;
// %template(UnsignedLongCollection) OpenTURNS::Base::Type::PersistentCollection<OpenTURNS::NumericalScalar>;

%include IntegralUserDefined.hxx

namespace IntegralCompoundPoisson { %extend IntegralUserDefined { IntegralUserDefined(const IntegralUserDefined & other) { return new IntegralCompoundPoisson::IntegralUserDefined(other); } } }
