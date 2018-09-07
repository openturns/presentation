//                                               -*- C++ -*-
/**
 *  @file  IntegralUserDefined.cxx
 *  @brief The IntegralUserDefined distribution
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
#include <PersistentObjectFactory.hxx>
#include <UserDefinedPair.hxx>

#include "IntegralUserDefined.hxx"

namespace IntegralCompoundPoisson {

      CLASSNAMEINIT(IntegralUserDefined);

      static OpenTURNS::Base::Common::Factory<IntegralUserDefined> RegisteredFactory("IntegralUserDefined");

      typedef OpenTURNS::Uncertainty::Distribution::UserDefinedPair UserDefinedPair;

      /* Default constructor */
      IntegralUserDefined::IntegralUserDefined()
        : UserDefined(),
          support_(UnsignedLongCollection(1)),
          weights_(NumericalPoint(1, 1.0)),
          normalizedWeights_(NumericalPoint(1, 1.0))
      {
      }

      /* Parameters constructor */
      IntegralUserDefined::IntegralUserDefined(const UnsignedLongCollection & support,
                             const NumericalPoint & weights)
        /* throw (InvalidArgumentException) */
        : UserDefined(),
          support_(support),
          weights_(weights),
          normalizedWeights_(NumericalPoint(1, 1.0))
      {
        setSupportWeightsCollection(support, weights);
      }

      /* Comparison operator */
      Bool IntegralUserDefined::operator ==(const IntegralUserDefined & other) const {
        Bool sameObject = false;

        if (this != &other) { // Other is NOT me, so I have to realize the comparison
          // sameObject = ...
          // TODO: Write IntegralUserDefined::operator ==(...)
          sameObject = (support_ == other.support_) && (weights_ == other.weights_);
        } else sameObject = true;

        return sameObject;
      }

      /* String converter */
      String IntegralUserDefined::__repr__() const {
        OpenTURNS::OSS oss;
        oss << "class=" << IntegralUserDefined::GetClassName()
            << " name=" << getName()
            << " dimension=" << getDimension()
            << " support=" << support_
            << " weights=" << weights_;
        return oss;
      }

      /* Virtual constructor */
      IntegralUserDefined * IntegralUserDefined::clone() const
      {
        return new IntegralUserDefined(*this);
      }

      /** Tell if the distribution is integer valued */
      Bool IntegralUserDefined::isIntegral() const
      {
        return true;
      }

      /* support accessor */
      /** Supports and weights collection accessor */
      void IntegralUserDefined::setSupportWeightsCollection(const UnsignedLongCollection & support,
          const NumericalPoint & weights)
      {
        const UnsignedLong supportSize(support.getSize());
        const UnsignedLong weightSize(weights.getSize());
        // Check arguments
        if (supportSize == 0 || weightSize == 0) throw InvalidArgumentException(HERE) << "Error: cannot build an IntegralUserDefined distribution based on an empty sample.";
        if (supportSize != weightSize) throw InvalidArgumentException(HERE) << "Error: cannot build an IntegralUserDefined distribution if support and weights have a different size.";
        for (UnsignedLong i = 0; i < supportSize; ++i)
          {
            if (support[i] < 0) throw InvalidArgumentException(HERE) << "Error: cannot build an IntegralUserDefined distribution if support contains negative integers";
          }
        for (UnsignedLong i = 0; i < weightSize; ++i)
          {
            if (weights[i] < 0 || weights[i] > 1.0) throw InvalidArgumentException(HERE) << "Error: cannot build an IntegralUserDefined distribution if weights are not in [0, 1]";
          }
        NumericalScalar sumWeights(0.);
        for (UnsignedLong i = 0; i < weightSize; ++i) sumWeights += weights[i];
        if (sumWeights == 0.0) throw InvalidArgumentException(HERE) << "Error: cannot build an IntegralUserDefined distribution if all weights are null";

        weights_ = NumericalPoint(weightSize, 0.0);
        for (UnsignedLong i = 0; i < weightSize; ++i) weights_[i] = weights[i];

        normalizedWeights_ = weights_ * (1.0 / sumWeights);

        support_ = UnsignedLongCollection(supportSize);
        for (UnsignedLong i = 0; i < supportSize; ++i) support_[i] = support[i];

        NumericalSample sample(supportSize, 1);
        for (UnsignedLong i = 0; i < supportSize; ++i) sample[i] = NumericalPoint(1, support_[i]);

        UserDefinedPairCollection collection(supportSize);
        for (UnsignedLong i = 0; i < supportSize; ++i)
          {
            collection[i] = UserDefinedPair(sample[i], normalizedWeights_[i]);
          }
        // We set the dimension of the UserDefined distribution
        // This call set also the range
        setPairCollection( collection );
        setName("IntegralUserDefined");
      }

      /* support accessor */
      UnsignedLongCollection IntegralUserDefined::getIntegralSupport() const
      {
        return support_;
      }

      /** Get the support of a distribution that intersect a given interval */
      IntegralUserDefined::NumericalSample IntegralUserDefined::getSupport(const Interval & interval) const
      {
        const NumericalPoint lower(interval.getLowerBound());
        const NumericalPoint upper(interval.getUpperBound());
        const UnsignedLong supportSize(support_.getSize());
        UnsignedLong count(0);
        for (UnsignedLong i = 0; i < supportSize; ++i)
          {
            if (support_[i] >= lower[0] && support_[i] <= upper[0]) count++;
          }
        NumericalSample sample(count, 1);
        count = 0;
        for (UnsignedLong i = 0; i < supportSize; ++i)
          {
            if (support_[i] >= lower[0] && support_[i] <= upper[0])
              {
                sample[count] = NumericalPoint(1, support_[i]);
                count++;
              }
          }
        return sample;
      }


      /* weights accessor */
      IntegralUserDefined::NumericalPoint IntegralUserDefined::getWeights() const
      {
        return weights_;
      }

      /* normalizedWeights accessor */
      IntegralUserDefined::NumericalPoint IntegralUserDefined::getNormalizedWeights() const
      {
        return normalizedWeights_;
      }

      /* Method save() stores the object through the StorageManager */
      void IntegralUserDefined::save(StorageManager::Advocate & adv) const
      {
        UserDefined::save(adv);
        adv.saveAttribute( "support_", support_ );
        adv.saveAttribute( "weights_", weights_ );
        adv.saveAttribute( "normalizedWeights_", normalizedWeights_ );
      }

      /* Method load() reloads the object from the StorageManager */
      void IntegralUserDefined::load(StorageManager::Advocate & adv)
      {
        UserDefined::load(adv);
        adv.loadAttribute( "support_", support_ );
        adv.loadAttribute( "weights_", weights_ );
        adv.loadAttribute( "normalizedWeights_", normalizedWeights_ );
        computeRange();
      }

} /* namespace IntegralCompoundPoisson */
