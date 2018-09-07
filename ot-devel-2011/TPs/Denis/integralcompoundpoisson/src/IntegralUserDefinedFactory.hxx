//                                               -*- C++ -*-
/**
 *  @file  IntegralUserDefinedFactory.hxx
 *  @brief IntegralUserDefinedFactory is some integralcompoundpoisson type to illustrate how to add some classes in Open TURNS
 *
 *  (C) Copyright 2005-2007 EDF-EADS-Phimeca
 *
 *  This library is free software; you can redistribute it and/or
 *  modify it under the terms of the GNU Lesser General Public
 *  License as published by the Free Software Foundation; either
 *  version 2.1 of the License.
 *
 *  This library is distributed in the hope that it will be useful
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 *  Lesser General Public License for more details.
 *
 *  You should have received a copy of the GNU Lesser General Public
 *  License along with this library; if not, write to the Free Software
 *  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307 USA
 *
 *  @author: $LastChangedBy$
 *  @date:   $LastChangedDate: 2008-10-31 11:52:04 +0100 (Fri, 31 Oct 2008) $
 *  Id:      $Id: IntegralUserDefinedFactory.hxx 995 2008-10-31 10:52:04Z dutka $
 */
#ifndef INTEGRALCOMPOUNDPOISSON_INTEGRALUSERDEFINEDFACTORY_HXX
#define INTEGRALCOMPOUNDPOISSON_INTEGRALUSERDEFINEDFACTORY_HXX

#include <TypedInterfaceObject.hxx>
#include <StorageManager.hxx>
#include <DistributionImplementationFactory.hxx>

#include "IntegralUserDefined.hxx"


namespace IntegralCompoundPoisson {

  /**
   * @class IntegralUserDefinedFactory
   *
   * IntegralUserDefinedFactory is some integralcompoundpoisson type to illustrate how to add some classes in Open TURNS
   */
  class IntegralUserDefinedFactory
    : public OpenTURNS::Uncertainty::Model::DistributionImplementationFactory
  {
    CLASSNAME;

  public:
    typedef OpenTURNS::Uncertainty::Model::DistributionImplementationFactory  DistributionImplementationFactory; // required by SWIG
    typedef OpenTURNS::Base::Common::StorageManager      StorageManager;

    /** Default constructor */
    IntegralUserDefinedFactory();

    /** Virtual constructor */
    virtual IntegralUserDefinedFactory * clone() const;

    /* Here is the interface that all derived class must implement */
    using DistributionImplementationFactory::buildImplementation;

    IntegralUserDefined * buildImplementation(const NumericalSample & sample) const /* throw(InvalidArgumentException, InternalException) */;
    IntegralUserDefined * buildImplementation(const NumericalPointCollection & parameters) const /* throw(InvalidArgumentException, InternalException) */;
    IntegralUserDefined * buildImplementation() const /* throw(InvalidArgumentException, InternalException) */;

  private:

  }; /* class IntegralUserDefinedFactory */

} /* Namespace IntegralUserDefinedFactory */

#endif /* INTEGRALCOMPOUNDPOISSON_INTEGRALUSERDEFINEDFACTORY_HXX */
