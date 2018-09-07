//                                               -*- C++ -*-
/**
 *  @file  UniformSphericalRandomVector.cxx
 *  @brief UniformSphericalRandomVector is some UniformSphericalRandomVector type to illustrate how to add some classes in Open TURNS
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
 *  @author: $LastChangedBy: dutka $
 *  @date:   $LastChangedDate: 2008-10-31 11:52:04 +0100 (Fri, 31 Oct 2008) $
 *  Id:      $Id: UniformSphericalRandomVector.cxx 995 2008-10-31 10:52:04Z dutka $
 */
#include "UniformSphericalRandomVector.hxx"
#include "DistFunc.hxx"

namespace OpenTURNS {

  namespace Uncertainty {

    namespace Model {
  
      CLASSNAMEINIT(UniformSphericalRandomVector);

    	typedef Uncertainty::Distribution::DistFunc		   DistFunc;

      /* Default constructor */
      UniformSphericalRandomVector::UniformSphericalRandomVector(const UnsignedLong dimension)
        : RandomVectorImplementation(),
	dimension_(dimension)
      {
        // Nothing to do
      }

      /* String converter */
      String UniformSphericalRandomVector::str() const
      {
        return OSS() << "class=" << UniformSphericalRandomVector::GetClassName()
      	  		 << " dimension=" << dimension_;
      }
  
      /* Get one realization of the distribution */
      UniformSphericalRandomVector::NumericalPoint UniformSphericalRandomVector::getRealization() const
      {
        NumericalPoint X(dimension_);
        NumericalScalar R(1);
        do
      	  {
      	  for (UnsignedLong i = 0; i < dimension_; ++i)
      	    { 
      	      X[i] = DistFunc::rNormal();
      	    }
      	  R=X.norm();
      	  }
        while (R==0);
        NumericalPoint value(X * (1./R));
	return value;
      }
      
      /* Dimension accessor */
      UnsignedLong UniformSphericalRandomVector::getDimension() const
      {
        return dimension_;
      }
      
      
    } /* namespace Model */
  } /* namespace Uncertainty */
} /* namespace OpenTURNS */

  
  

  

  

  
  

  

  
  

  


  
  
