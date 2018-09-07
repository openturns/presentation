//                                               -*- C++ -*-
/**
 *  @file  t_IntegralCompoundPoisson_std.cxx
 *  @brief The test file of class IntegralCompoundPoisson for standard methods
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

#include "IntegralCompoundPoisson.hxx"
#include "IntegralUserDefinedFactory.hxx"

using namespace OT;
using namespace OT::Test;
using namespace OT::Base::Common;
using namespace OT::Base::Stat;
using namespace OT::Base::Type;
using namespace OT::Base::Graph;

class TestObject : public IntegralCompoundPoisson::IntegralCompoundPoisson
{
public:
  explicit TestObject() : IntegralCompoundPoisson::IntegralCompoundPoisson() {}
  explicit TestObject(const OT::String & name) : IntegralCompoundPoisson::IntegralCompoundPoisson() {setName(name);}
  virtual ~TestObject() {}
};


int main(int argc, char *argv[])
{
  TESTPREAMBLE;
  OStream fullprint(std::cout);
  setRandomGenerator();
  Bool drawFlag = true;

  try {
    // Test basic functionnalities
    checkClassWithClassName<TestObject>();

    // Test some extra functionnalities
    checkNameFeature<TestObject>();

    // Instanciate one distribution object
    // First, build the atom distribution
    IntegralCompoundPoisson::UnsignedLongCollection support;
    support.add(1);
    support.add(2);
    support.add(4);
    support.add(7);
    Collection<NumericalScalar> weightsCollection;
    weightsCollection.add(0.1);
    weightsCollection.add(0.2);
    weightsCollection.add(0.3);
    weightsCollection.add(0.4);
    NumericalPoint weights(weightsCollection);
    IntegralCompoundPoisson::IntegralUserDefined d(support, weights);
    // Second, build Poisson's theta
    const NumericalScalar theta(20.0);
    // Build the CompoundPoisson distribution
    IntegralCompoundPoisson::IntegralCompoundPoisson ICP(d, theta);
    NumericalSample ICPSample = ICP.getNumericalSample(100000);
    IntegralCompoundPoisson::IntegralUserDefined * userDefined(IntegralCompoundPoisson::IntegralUserDefinedFactory().buildImplementation(ICPSample));
    for (UnsignedLong i = 1; i < 181; ++i)
      {
        const NumericalPoint npi(1, i);
        const NumericalScalar udPDF(userDefined->computePDF(npi));
        const NumericalScalar icpPDF(ICP.computePDF(npi));
        const NumericalScalar udCDF(userDefined->computeCDF(npi));
        const NumericalScalar icpCDF(ICP.computeCDF(npi));
        const NumericalScalar udCDFc(userDefined->computeCDF(npi, true));
        const NumericalScalar icpCDFc(ICP.computeCDF(npi, true));
        fullprint << "error rel % (PDF, CDF, CDF c)=" << std::endl;
        NumericalPoint res1(3, 0.0);
        res1[0] = udPDF / icpPDF - 1.0;
        res1[1] = udCDF / icpCDF - 1.0;
        res1[2] = udCDFc / icpCDFc - 1.0;
        res1 *= 100;
        fullprint << res1 << std::endl;
        fullprint << "error abs (PDF, CDF, CDF c)=" << std::endl;
        NumericalPoint res2(3, 0.0);
        res2[0] = fabs(udPDF - icpPDF);
        res2[1] = fabs(udCDF - icpCDF);
        res2[2] = fabs(udCDFc - icpCDFc);
        fullprint << res2 << std::endl;
      }

    if (drawFlag)
      {
        NumericalScalar xMin(-10.0);
        NumericalScalar xMax(200.0);
        Graph::Format format(GraphImplementation::PNG);
        Graph g(ICP.drawPDF(xMin, xMax));
        Drawable drawable(userDefined->drawPDF(xMin, xMax, 10 * int(xMax - xMin + 1)).getDrawable(0));
        drawable.setColor("blue");
        drawable.setLineStyle("dotted");
        g.addDrawable(drawable);
        g.draw("ICPPDF", 1280, 1024, format);
        // ViewImage(g.getBitmap());

        g = ICP.drawCDF(xMin, xMax);
        drawable = userDefined->drawCDF(xMin, xMax, 10 * int(xMax - xMin + 1)).getDrawable(0);
        drawable.setColor("blue");
        drawable.setLineStyle("dotted");
        g.addDrawable(drawable);
        g.draw("ICPCDF", 1280, 1024, format);
        // ViewImage(g.getBitmap());
      }

  }
  catch (TestFailed & ex) {
    std::cerr << ex << std::endl;
    return ExitCode::Error;
  }


  return ExitCode::Success;
}
