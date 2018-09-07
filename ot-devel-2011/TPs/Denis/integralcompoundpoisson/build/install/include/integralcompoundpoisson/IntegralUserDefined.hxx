//                                               -*- C++ -*-
/**
 *  @file  IntegralCompoundPoisson.hxx
 *  @brief The IntegralCompoundPoisson distribution
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
#ifndef INTEGRALCOMPOUNDPOISSON_INTEGRALUSERDEFINED_HXX
#define INTEGRALCOMPOUNDPOISSON_INTEGRALUSERDEFINED_HXX

#include <Collection.hxx>
#include <OTtypes.hxx>

#include "UserDefined.hxx"

namespace IntegralCompoundPoisson {

      typedef OpenTURNS::Uncertainty::Distribution::UserDefined  UserDefined;
      typedef OpenTURNS::NumericalScalar                         NumericalScalar;
      typedef OpenTURNS::UnsignedLong                            UnsignedLong;
      typedef OpenTURNS::Bool                                    Bool;
      typedef OpenTURNS::String                                  String;
      typedef OpenTURNS::Base::Type::Collection<UnsignedLong>    UnsignedLongCollection;

      /**
       * @class IntegralUserDefined
       *
       * The IntegralUserDefined distribution.
       */
      class IntegralUserDefined
        : public OpenTURNS::Uncertainty::Distribution::UserDefined
      {
        CLASSNAME;
      public:

        typedef OpenTURNS::Base::Common::InvalidArgumentException           InvalidArgumentException;
        typedef OpenTURNS::Base::Type::PersistentCollection<UnsignedLong>   UnsignedLongPersistentCollection;
        typedef OpenTURNS::Base::Type::Interval                             Interval;
        typedef UserDefined::NumericalPoint                          NumericalPoint;
        typedef UserDefined::NumericalSample                         NumericalSample;
        typedef UserDefined::NumericalPointWithDescriptionCollection NumericalPointWithDescriptionCollection;
        typedef UserDefined::NotDefinedException                     NotDefinedException;
        typedef UserDefined::StorageManager                          StorageManager;

        /** Default constructor */
        IntegralUserDefined();

        /** Parameters constructor */
        explicit IntegralUserDefined(const UnsignedLongCollection & support,
                   const NumericalPoint & weights)
          /* throw (InvalidArgumentException) */;


        /** Comparison operator */
        Bool operator ==(const IntegralUserDefined & other) const;

        /** String converter */
	String __repr__() const;

        /** Tell if the distribution is integer valued */
        Bool isIntegral() const;

        /* Interface inherited from Distribution */

        /** Virtual constructor */
        IntegralUserDefined * clone() const;

        /* Interface specific to IntegralUserDefined */

        /** support accessor */
        UnsignedLongCollection getIntegralSupport() const;

        /** Get the support of a distribution that intersect a given interval */
        NumericalSample getSupport(const Interval & interval) const;

        /** weights accessor */
        NumericalPoint getWeights() const;

        /** normalizedWeights accessor */
        NumericalPoint getNormalizedWeights() const;

        /** Method save() stores the object through the StorageManager */
        void save(StorageManager::Advocate & adv) const;

        /** Method load() reloads the object from the StorageManager */
        void load(StorageManager::Advocate & adv);

      protected:

      private:

        /** Supports and weights collection accessor */
        void setSupportWeightsCollection(const UnsignedLongCollection & support, const NumericalPoint & weights)
          /* throw (InvalidArgumentException) */;

        /** The main parameter set of the distribution */
        UnsignedLongPersistentCollection support_;
        NumericalPoint weights_;
        NumericalPoint normalizedWeights_;

      }; /* class IntegralUserDefined */


} /* namespace IntegralCompoundPoisson */

#endif /* INTEGRALCOMPOUNDPOISSON_INTEGRALUSERDEFINED_HXX */
