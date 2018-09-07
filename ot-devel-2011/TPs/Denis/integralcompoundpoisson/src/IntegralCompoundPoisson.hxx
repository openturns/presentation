//                                               -*- C++ -*-
/**
 *  @file  IntegralCompoundPoisson.hxx
 *  @brief IntegralCompoundPoisson is some integralcompoundpoisson type to illustrate how to add some classes in Open TURNS
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
 *  Id:      $Id: IntegralCompoundPoisson.hxx 995 2008-10-31 10:52:04Z dutka $
 */
#ifndef INTEGRALCOMPOUNDPOISSON_INTEGRALCOMPOUNDPOISSON_HXX
#define INTEGRALCOMPOUNDPOISSON_INTEGRALCOMPOUNDPOISSON_HXX

#include <DiscreteDistribution.hxx>
#include <Poisson.hxx>
#include <UniVariatePolynomial.hxx>
#include <Collection.hxx>
#include <Graph.hxx>
#include <StorageManager.hxx>

#include "IntegralUserDefined.hxx"

namespace IntegralCompoundPoisson {

  /**
   * @class IntegralCompoundPoisson
   *
   * IntegralCompoundPoisson is some integralcompoundpoisson type to illustrate how to add some classes in Open TURNS
   */
  class IntegralCompoundPoisson
    : public OpenTURNS::Uncertainty::Model::DiscreteDistribution
  {
    CLASSNAME;

  public:
    typedef OpenTURNS::String           String;
    typedef OpenTURNS::Bool             Bool;
    typedef OpenTURNS::Uncertainty::Model::DiscreteDistribution DiscreteDistribution;
    typedef OpenTURNS::Base::Common::StorageManager             StorageManager;
    typedef OpenTURNS::Base::Func::UniVariatePolynomial         UniVariatePolynomial;
    typedef UniVariatePolynomial::Coefficients           Coefficients;
    typedef UniVariatePolynomial::NumericalComplexCollection  NumericalComplexCollection;
    typedef OpenTURNS::Uncertainty::Distribution::Poisson       Poisson;
    typedef DiscreteDistribution::CovarianceMatrix       CovarianceMatrix;
    typedef DiscreteDistribution::NumericalSample        NumericalSample;
    typedef DiscreteDistribution::NumericalPoint         NumericalPoint;
    typedef DiscreteDistribution::Graph                  Graph;


    /** Default constructor */
    IntegralCompoundPoisson();

    /** Parameters constructor */
    IntegralCompoundPoisson(const IntegralUserDefined & atomDistribution,
            const NumericalScalar theta, 
            const UnsignedLong log2cache = 10)
      /* throw (InvalidArgumentException) */;

    /** Comparison operator */
    Bool operator ==(const IntegralCompoundPoisson & other) const;

    /** String converter */
    OpenTURNS::String __repr__() const;

    /* Interface inherited from Distribution */

    /** Virtual constructor */
    virtual IntegralCompoundPoisson * clone() const;

    /** Get one realization of the distribution */
    using DiscreteDistribution::getRealization;
    NumericalPoint getRealization() const;
 
    /** Get the quantile of the sample */
    using DiscreteDistribution::computeQuantile;
    NumericalPoint computeQuantile(const NumericalScalar prob, Bool tail = false) const;

    /** Get the PDF of the distribution */
    using DiscreteDistribution::computePDF;
    NumericalScalar computePDF(const NumericalPoint & point) const;

    /** Get the CDF of the distribution */
    using DiscreteDistribution::computeCDF;
    NumericalScalar computeCDF(const NumericalPoint & point, const Bool tail = false) const;

    /** Get a numerical sample whose elements follow the distribution */
    using DiscreteDistribution::getNumericalSample;
    NumericalSample getNumericalSample(const UnsignedLong size) const;

    using DiscreteDistribution::getSupport;
    NumericalSample getSupport(const Interval & interval) const;

    /** Get the mean of the distribution */
    NumericalPoint getMean() const;

    /** Get the standard deviation of the distribution */
    NumericalPoint getStandardDeviation() const;

    /** Get the covariance of the distribution */
    CovarianceMatrix getCovariance() const;

    using DiscreteDistribution::drawPDF;
    Graph drawPDF(const NumericalScalar xMin,
                  const NumericalScalar xMax,
                  const UnsignedLong pointNumber = DefaultPointNumber) const;

    using DiscreteDistribution::drawCDF;
    Graph drawCDF(const NumericalScalar xMin,
                  const NumericalScalar xMax,
                  const UnsignedLong pointNumber = DefaultPointNumber) const;

  private:

    void fillComputationCache() const;

    /** The Lambda of the Poisson distribution */
    NumericalScalar theta_;

    /** The Poisson distribution */
    Poisson poisson_;

    /** The atom distribution */
    IntegralUserDefined atomDistribution_;

    UniVariatePolynomial q_;
    mutable NumericalPoint pdfCache_;
    mutable NumericalPoint cdfCache_;
    mutable UnsignedLong m_;

  }; /* class IntegralCompoundPoisson */

} /* Namespace IntegralCompoundPoisson */

#endif /* INTEGRALCOMPOUNDPOISSON_INTEGRALCOMPOUNDPOISSON_HXX */
