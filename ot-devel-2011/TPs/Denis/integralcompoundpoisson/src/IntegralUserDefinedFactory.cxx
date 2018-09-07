//                                               -*- C++ -*-
/**
 *  @file  IntegralUserDefinedFactory.cxx
 *  @brief IntegralUserDefinedFactory is some integralcompoundpoisson type to illustrate how to add some classes in Open TURNS
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
 *  @date:   $LastChangedDate: 2008-10-31 11:52:04 +0100 (Fri, 31 Oct 2008) $
 *  Id:      $Id: IntegralUserDefinedFactory.cxx 995 2008-10-31 10:52:04Z dutka $
 */
#include <PersistentObjectFactory.hxx>
#include <Collection.hxx>
#include <map>

#include "IntegralUserDefinedFactory.hxx"

namespace IntegralCompoundPoisson {

  CLASSNAMEINIT(IntegralUserDefinedFactory);

  typedef OpenTURNS::Base::Type::Collection<NumericalScalar>                NumericalScalarCollection;
  typedef OpenTURNS::Uncertainty::Model::DistributionImplementationFactory  DistributionImplementationFactory;

  /* Default constructor */
  IntegralUserDefinedFactory::IntegralUserDefinedFactory()
    : DistributionImplementationFactory()
  {
    // Nothing to do
  }

      /* Virtual constructor */
      IntegralUserDefinedFactory * IntegralUserDefinedFactory::clone() const
      { 
        return new IntegralUserDefinedFactory(*this);
      }

      /* Here is the interface that all derived class must implement */

      IntegralUserDefined * IntegralUserDefinedFactory::buildImplementation(const NumericalSample & sample) const /* throw(InvalidArgumentException, InternalException) */
      {
        const NumericalScalar sampleSize(sample.getSize());
        std::map<UnsignedLong, int> mapSamples;
        if (sampleSize == 0) throw InvalidArgumentException(HERE) << "Error: cannot build a IntegralUserDefined distribution from an empty sample";
        if (sample.getDimension() != 1) throw InvalidArgumentException(HERE) << "Error: can build a IntegralUserDefined distribution only from a sample of dimension 1, here dimension=" << sample.getDimension();
        for (UnsignedLong i = 0; i < sampleSize; ++i)
          {
            if (sample[i][0] < 0) throw InvalidArgumentException(HERE) << "Error: realizations must be nonnegative";
            UnsignedLong val(sample[i][0]);
            if (mapSamples.find(val) != mapSamples.end()) {
              int oldCount(mapSamples[val]);
              mapSamples[val] =  oldCount + 1;
            } else {
              mapSamples[val] = 0;
            }
          }

        UnsignedLong itemSize(mapSamples.size());
        UnsignedLongCollection support;
        NumericalScalarCollection weightsCollection;
        for(std::map<UnsignedLong, int>::const_iterator it = mapSamples.begin(); it != mapSamples.end(); ++it)
          {
            support.add(it->first);
            weightsCollection.add(it->second / (NumericalScalar) sampleSize);
          }
        NumericalPoint weights(weightsCollection);

        return IntegralUserDefined(support, weights).clone();
      }

      IntegralUserDefined * IntegralUserDefinedFactory::buildImplementation(const NumericalPointCollection & parameters) const /* throw(InvalidArgumentException, InternalException) */
      {
        try {
          IntegralUserDefined distribution;
          distribution.setParametersCollection(parameters);
          return distribution.clone();
        }
        catch (InvalidArgumentException & ex)
          {
            throw InternalException(HERE) << "Error: cannot build a IntegralUserDefined distribution from the given parameters";
          }
      }

      IntegralUserDefined * IntegralUserDefinedFactory::buildImplementation() const /* throw(InvalidArgumentException, InternalException) */
      {
        return IntegralUserDefined().clone();
      }

} /* Namespace IntegralUserDefinedFactory */
