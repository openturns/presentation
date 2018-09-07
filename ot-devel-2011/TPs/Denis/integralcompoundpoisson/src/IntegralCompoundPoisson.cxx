//                                               -*- C++ -*-
/**
 *  @file  IntegralCompoundPoisson.cxx
 *  @brief IntegralCompoundPoisson is some integralcompoundpoisson type to illustrate how to add some classes in Open TURNS
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
 *  Id:      $Id: IntegralCompoundPoisson.cxx 995 2008-10-31 10:52:04Z dutka $
 */
#include <PersistentObjectFactory.hxx>
#include <Collection.hxx>
#include <DiscreteDistribution.hxx>
#include <Staircase.hxx>
#include <Curve.hxx>
#include <math.h>

#include "kissfft.hh"
#include "IntegralCompoundPoisson.hxx"

namespace IntegralCompoundPoisson {

  CLASSNAMEINIT(IntegralCompoundPoisson);

  static OpenTURNS::Base::Common::Factory<IntegralCompoundPoisson> RegisteredFactory("IntegralCompoundPoisson");

  typedef OpenTURNS::NumericalComplex                    NumericalComplex;
  typedef OpenTURNS::Uncertainty::Distribution::Poisson  Poisson;
  typedef OpenTURNS::Base::Func::UniVariatePolynomial    UniVariatePolynomial;
  typedef OpenTURNS::Base::Graph::Curve                  Curve;
  typedef OpenTURNS::Base::Graph::Staircase              Staircase;

  typedef kissfft<NumericalScalar> FFT;

  /* Default constructor */
  IntegralCompoundPoisson::IntegralCompoundPoisson()
    : DiscreteDistribution(),
      theta_(1.0),
      poisson_(),
      atomDistribution_(),
      q_(),
      pdfCache_(),
      cdfCache_(),
      m_(0)
  {
    // Nothing to do
  }

  /* Parameters constructor */
  IntegralCompoundPoisson::IntegralCompoundPoisson(const IntegralUserDefined & atomDistribution,
                                                   const NumericalScalar theta,
                                                   const UnsignedLong log2cache)
    : DiscreteDistribution(),
      theta_(theta),
      poisson_(Poisson(theta)),
      atomDistribution_(atomDistribution),
      q_(),
      pdfCache_(),
      cdfCache_(),
      m_(0)
  {
    // Get the information to build the generating function (GF) of the atom distribution as a sparse polynomial
    UnsignedLongCollection support(atomDistribution.getIntegralSupport());
    NumericalPoint coeffs(atomDistribution.getNormalizedWeights() * theta_);
    // Substract theta
    support.add(0);
    coeffs.add(-theta);
    // Build the Q polynomial
    UnsignedLong d(0);
    for (UnsignedLong i = 0, n = support.getSize(); i < n; ++i)
      {
        if (d < support[i]) d = support[i];
      }
    NumericalPoint fullCoefficients(d + 1, 0.0);
    for (UnsignedLong i = 0, n = support.getSize(); i < n; ++i)
      {
        fullCoefficients[support[i]] += coeffs[i];
      }
    q_ = UniVariatePolynomial(fullCoefficients);
    pdfCache_ = NumericalPoint(0);
    cdfCache_ = NumericalPoint(0);
    m_ = 1 << log2cache;
    fillComputationCache();
  }

  /* Comparison operator */
  OpenTURNS::Bool IntegralCompoundPoisson::operator ==(const IntegralCompoundPoisson & other) const
  {
    if (this == &other) return true;
    return (theta_ == other.theta_) && (atomDistribution_ == other.atomDistribution_);
  }

  OpenTURNS::String IntegralCompoundPoisson::__repr__() const
  {
    return OpenTURNS::OSS() << "class=" << IntegralCompoundPoisson::GetClassName()
                            << " name=" << getName()
                            << " dimension=" << getDimension();
  }

  /* Virtual constructor */
  IntegralCompoundPoisson * IntegralCompoundPoisson::clone() const
  {
    return new IntegralCompoundPoisson(*this);
  }

  /* Get one realization of the distribution */
  IntegralCompoundPoisson::NumericalPoint IntegralCompoundPoisson::getRealization() const
  {
    NumericalScalar realization(0.0);
    // Number of terms
    const UnsignedLong N(static_cast<UnsignedLong>(round(poisson_.getRealization()[0])));
    // Sum the atoms
    for (UnsignedLong i = 0; i < N; ++i) realization += atomDistribution_.getRealization()[0];
    return NumericalPoint(1, realization);
  }

  /** Get the quantile of the sample */
  IntegralCompoundPoisson::NumericalPoint IntegralCompoundPoisson::computeQuantile(const NumericalScalar prob,
										   Bool tail) const
  {
    if (prob < 0.0 || prob > 1.0) throw InvalidArgumentException(HERE) << "Error: In IntegralCompoundPoisson, prob must be in [0, 1]";
    UnsignedLong k(0);
    if (tail)
      {
        while (computeCDF(NumericalPoint(1, k), true) > prob) ++k;
      }
    else
      {
        while (computeCDF(NumericalPoint(1, k)) < prob) ++k;
      }
    return NumericalPoint(1, k);
  }

  /** Get the PDF of the distribution */
  NumericalScalar IntegralCompoundPoisson::computePDF(const NumericalPoint & point) const
  {
    NumericalScalar x(point[0]);
    // x must be a nonnegative integer
    if (x < 0) return 0.0;
    const UnsignedLong k(static_cast<UnsignedLong>(round(x)));
    if (x != k) return 0.0;
    const UnsignedLong cacheSize(pdfCache_.getSize());
    if (k < cacheSize) return pdfCache_[k];
    // If we arrive here, it is because i >= m so increase m and
    // update the caches
    while (m_ <= k) m_ << 1;
    fillComputationCache();
    return pdfCache_[k];
  }

  /** Get the CDF of the distribution */
  NumericalScalar IntegralCompoundPoisson::computeCDF(const NumericalPoint & point, const Bool tail) const
  {
    const NumericalScalar x(point[0]);
    // x must be a positive integer
    if (x <= 0) return (tail ? 1.0 : 0.0);
    const UnsignedLong k(static_cast<UnsignedLong>(round(x)));
    // If the value is already in the cache, return it
    UnsignedLong cacheSize(cdfCache_.getSize());
    if (k < cacheSize) return (tail ? 1.0 - cdfCache_[k] : cdfCache_[k]);
    // Compute all the values from the last stored in the cache to the needed one
    NumericalScalar lastCDF(0.0);
    if (cacheSize > 0) lastCDF = cdfCache_[cacheSize - 1];
    for (UnsignedLong i = cacheSize; i <= k; ++i)
      {
        lastCDF += computePDF((NumericalScalar) i);
        if (lastCDF > 1.0) lastCDF = 1.0;
        cdfCache_.add(lastCDF);
      }
    return (tail ? 1.0 - cdfCache_[k] : cdfCache_[k]);
  }

  IntegralCompoundPoisson::Graph IntegralCompoundPoisson::drawPDF(const NumericalScalar xMin,
                                                                  const NumericalScalar xMax,
                                                                  const UnsignedLong pointNumber) const
  {
    if (xMax <= xMin) throw InvalidArgumentException(HERE) << "Error: cannot draw a PDF with xMax >= xMin, here xmin=" << xMin << " and xmax=" << xMax;
    NumericalSample support(0, 1);
    NumericalPoint weights(0);
    for (NumericalScalar x(xMin); x <= xMax; x += 1.0)
      {
        support.add(NumericalPoint(1, x));
        weights.add(computePDF(x));
      }
    String title("IntegralCompoundPoisson PDF");
    Graph graph(title, "k", "pdf", true, "topright");
    NumericalPoint point(2);
    point[0] = xMin;
    point[1] = 0.0;
    NumericalSample data(0, 2);
    data.add(point);
    for (UnsignedLong i = 0, n = support.getSize(); i < n; ++i)
      {
        point[0] = support[i][0];
        data.add(point);
        point[1] = computePDF(point[0]);
        data.add(point);
        point[1] = 0.0;
        data.add(point);
      }
    point[0] = xMax;
    point[1] = 0.0;
    data.add(point);
    graph.addDrawable(Curve(data, "red", "solid", 2, title));
    return graph;
  }

  IntegralCompoundPoisson::Graph IntegralCompoundPoisson::drawCDF(const NumericalScalar xMin,
                                                                  const NumericalScalar xMax,
                                                                  const UnsignedLong pointNumber) const
  {
    if (xMax <= xMin) throw InvalidArgumentException(HERE) << "Error: cannot draw a PDF with xMax >= xMin, here xmin=" << xMin << " and xmax=" << xMax;
    NumericalSample support(0, 1);
    NumericalPoint weights(0);
    for (NumericalScalar x(xMin); x <= xMax; x += 1.0)
      {
        support.add(NumericalPoint(1, x));
        weights.add(computePDF(x));
      }
    UnsignedLong size(support.getSize());
    String title("IntegralCompoundPoisson CDF");
    Graph graph(title, "k", "pdf", true, "topleft");
    NumericalScalar lastX(xMin);
    NumericalSample data(size + 2, 2);
    data[0][0] = xMin;
    data[0][1] = computeCDF(xMin);
    for (UnsignedLong i = 0; i < size; ++i)
      {
        NumericalScalar x(support[i][0]);
        data[i + 1][0] = x;
        data[i + 1][1] = computeCDF(x);
      }
    data[size + 1][0] = xMax;
    data[size + 1][1] = computeCDF(xMax);
    Staircase s(data, "red", "solid", "s");
    s.setLineWidth(2);
    s.setLegendName(title);
    graph.addDrawable(s);
    return graph;
  }

  IntegralCompoundPoisson::NumericalSample IntegralCompoundPoisson::getSupport(const Interval & interval) const
  {
    const NumericalPoint lower(interval.getLowerBound());
    const NumericalPoint upper(interval.getUpperBound());
    UnsignedLongCollection support(atomDistribution_.getIntegralSupport());
    const UnsignedLong supportSize(support.getSize());
    UnsignedLong count(0);
    for (UnsignedLong i = 0; i < supportSize; ++i)
      {
        if (support[i] >= lower[0] && support[i] <= upper[0]) ++count;
      }
    NumericalSample sample(count, 1);
    count = 0;
    for (UnsignedLong i = 0; i < supportSize; ++i)
      {
        if (support[i] >= lower[0] && support[i] <= upper[0])
          {
            sample[count] = NumericalPoint(1, support[i]);
            count++;
          }
      }
    return sample;
  }

  void IntegralCompoundPoisson::fillComputationCache() const
  {
    NumericalScalar r(exp((-10.63 / m_) * M_LN10));
    NumericalComplexCollection GFCache(m_);
    NumericalPoint rPowerCache(m_);
    NumericalComplexCollection expCache(m_);
    // Initial value
    expCache[0] = 1.0;
    rPowerCache[0] = 1.0;
    NumericalComplex s(0.0, 2.0 * M_PI / NumericalScalar(m_));
    for (UnsignedLong i = 1; i < m_; ++i)
      {
        expCache[i] = exp(s * NumericalScalar(i));
        rPowerCache[i] = rPowerCache[i-1] * r;
      }

    // Poisson's inversion formula
    // p_n = 1/(mr^n)\sum_{k=0}^{m-1} G(r\exp(2i\pi k/m))\exp(-2i\pi n k / m)
    // FFT
    // X_k = \sum_{n=0}^{N-1}x_n\exp(-2i\pi kn/N), k=0..N-1
    for (UnsignedLong i = 0; i < m_; ++i)
      {
        GFCache[i] = exp(q_(r * expCache[i]));
      }

    UnsignedLong nfft(GFCache.getSize());
    NumericalComplexCollection X(nfft);
    FFT fft(nfft,false);
    fft.transform( &GFCache[0] , &X[0] );

    NumericalPoint candidate(m_);
    for (UnsignedLong i = 0; i < m_; ++i)
      {
        candidate[i] = X[i].real() / (((NumericalScalar) m_) * rPowerCache[i]);
        // Due to roundoff errors, the computed pdf can be slightly negative
        if (candidate[i] < 0.0) candidate[i] = 0.0;
      }
    pdfCache_ = candidate;
  }

  /* Get a numerical sample whose elements follow the distribution */
  IntegralCompoundPoisson::NumericalSample IntegralCompoundPoisson::getNumericalSample(const UnsignedLong size) const
  {
    NumericalSample sample(size, 1);
    for (UnsignedLong i = 0; i < size; ++i)
      {
        sample[i] = getRealization();
      }
    return sample;
  }

  /* Get the mean of the distribution */
  IntegralCompoundPoisson::NumericalPoint IntegralCompoundPoisson::getMean() const
  {
    return NumericalPoint(1, q_.derivative(1.0) * exp(q_(1.0)));
  }

  /* Get the standard deviation of the distribution */
  IntegralCompoundPoisson::NumericalPoint IntegralCompoundPoisson::getStandardDeviation() const
  {
    return NumericalPoint(1, sqrt(getCovariance()(0, 0)));
  }

  /* Get the covariance of the distribution */
  IntegralCompoundPoisson::CovarianceMatrix IntegralCompoundPoisson::getCovariance() const
  {
    CovarianceMatrix covariance(1);
    NumericalScalar q1(q_(1.0));
    UniVariatePolynomial qp(q_.derivate());
    NumericalScalar qp1(qp(1.0));
    NumericalScalar qs1(qp.derivative(1.0));
    NumericalScalar expQ1(exp(q1));
    covariance(0, 0) = (qs1 + qp1 * (1.0 + qp1 * (1 - expQ1))) * expQ1;
    return covariance;
  }

} /* Namespace IntegralCompoundPoisson */
