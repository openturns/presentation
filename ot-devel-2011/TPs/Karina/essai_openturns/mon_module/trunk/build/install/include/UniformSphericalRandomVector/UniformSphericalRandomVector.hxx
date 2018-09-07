//                                               -*- C++ -*-
/**
 *  @file  UniformSphericalRandomVector.hxx
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
 *  Id:      $Id: UniformSphericalRandomVector.hxx 995 2008-10-31 10:52:04Z dutka $
 */
#ifndef OPENTURNS_UNIFORMSPHERICALRANDOMVECTOR_HXX
#define OPENTURNS_UNIFORMSPHERICALRANDOMVECTOR_HXX

#include "OT.hxx"
#include "NumericalPoint.hxx"
#include "RandomVectorImplementation.hxx"

namespace OpenTURNS {

  namespace Uncertainty {

    namespace Model {
  
      /**
       * @class UniformSphericalRandomVector
       *
       * UniformSphericalRandomVector is some UniformSphericalRandomVector type to illustrate how to add some classes in Open TURNS
       */
      class UniformSphericalRandomVector
    	: public RandomVectorImplementation
      {
    	CLASSNAME;
  
      public:
    	typedef Base::Type::NumericalPoint		   NumericalPoint;
  
    	/** Default constructor */
    	UniformSphericalRandomVector(const UnsignedLong dimension);
  
    	/** String converter */
    	String str() const;
    	
    	/* Get one realization of the distribution */
    	NumericalPoint getRealization() const;
	
    	/* Get one dimension of the distribution */
	UnsignedLong getDimension() const;
  
      private:
    	UnsignedLong dimension_;
      
      };
  
    } /* namespace Model */
  } /* namespace Uncertainty */
} /* namespace OpenTURNS */

#endif /* OPENTURNS_UNIFORMSPHERICALRANDOMVECTOR_HXX */
  

  
  

  
  

  

  

  
  

  

  
  

  


  
  
