//                                               -*- C++ -*-
/**
 *  @file  t_IntegralUserDefined_std.cxx
 *  @brief The test file of class t_IntegralUserDefined_std for standard methods
 *
 *  (C) Copyright 2011 EDF-EADS-Phimeca
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
 *  @date:   $LastChangedDate$
 *  Id:      $Id$
 */
#include <iostream>
#include <sstream>
#include <OT.hxx>
#include <OTtestcode.hxx>
#include <OStream.hxx>
#include <Collection.hxx>
#include <NumericalPoint.hxx>
#include <NumericalSample.hxx>

#include "IntegralUserDefined.hxx"
#include "IntegralUserDefinedFactory.hxx"

using namespace OT::Test;
using namespace OT::Base::Common;
using namespace OT::Base::Type;
using namespace OT::Uncertainty::Distribution;
using namespace IntegralCompoundPoisson;


class TestObject : public IntegralUserDefinedFactory
{
public:
  explicit TestObject() : IntegralUserDefinedFactory() {}
  explicit TestObject(const OT::String & name) : IntegralUserDefinedFactory() {setName(name);}
  virtual ~TestObject() {}
};


int main(int argc, char *argv[])
{
  TESTPREAMBLE;
  OStream fullprint(std::cout);
  setRandomGenerator();

  try {
    // Test basic functionnalities
    checkClassWithClassName<TestObject>();

    // Test some extra functionnalities
    checkNameFeature<TestObject>();

    // Instanciate one distribution object
    UnsignedLongCollection support;
    support.add(1);
    support.add(2);
    support.add(3);
    support.add(4);
    Collection<NumericalScalar> weightsCollection;
    weightsCollection.add(0.1);
    weightsCollection.add(0.2);
    weightsCollection.add(0.3);
    weightsCollection.add(0.8);
    NumericalPoint weights(weightsCollection);

    IntegralUserDefined distribution(support, weights);
    fullprint << "d=" << distribution << std::endl;

    // Test for sampling
    UnsignedLong size(10000);
    IntegralUserDefined::NumericalSample oneSample = distribution.getNumericalSample( size );
    IntegralUserDefined * d2(IntegralUserDefinedFactory().buildImplementation(oneSample));
    fullprint << "d2=" << *d2 << std::endl;

  }
  catch (TestFailed & ex) {
    std::cerr << ex << std::endl;
    return ExitCode::Error;
  }


  return ExitCode::Success;
}
