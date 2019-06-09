This is a set of scripts for generating a list of properties which fail to conform due to setbacks. Setback computations are based on the *minimal* setback dimension, since determining front vs. side vs. back is difficult even for a human and impossible for an automated script.

 - Using zone and building height from the city's Buildings GIS dataset, compute the *minimal* setback dimension (usually the side yard setback, though C-1A has a weird setback setup that might mean that isn't true, and BA-2 has a smaller front setback requirement than side setback.)
 - Using the parcel property line, buffer in by the setback amount in all directions. 
 - Find buildings which overlap with the parcel *by 85% of the building area*, then intersect them with the shrunk boundary line.

Flaws with this approach:

 - In general, there can be significant variance in setback dimensions: e.g. C-zoned properties have a minimum rear setback of 20 feet; but this approach will typically apply a minimum of only 7.5 feet (the side yard setback) instead. This will undercount setback non-conformance.
 - In zones like IB-2, or many of the BA zones, which have at least one dimension with no minimum setback, this will produce no setback information, despite these properties potentially having setback problems. This will undercount setback non-conformance.
 - In places where a parcel line splits a building in half -- e.g. 12-14 Laurel St. -- neither parcel holds 80% of the building, and so no building is identified which can be affected by setbacks. This will undercount setback non-conformance.
 - Setbacks do not take into account the *length* of a property along the line at all -- instead simply using the height. Many setbacks are based on height + length, and would likely be 2x larger using that approach, but it is impractical to implement this in an automated way, so setbacks are conservative.
 - Some properties have a building which is overlapping the parcel boundary by 20%-30%, e.g. garages or outbuildings. These buildings will not be considered in setbacks because they do not overlap by 85%.

I applied this approach to the 12696 properties that are included in the dataset used.

Using this approach, I identified 1590 parcels where no setback could be computed (due to being in a zoning district with no published setback requirements, or in a district with at least one dimension with a minimum setback dimension of 0). 

Of the remaining 11106 properties, 9115 parcels fail to conform to setback requirements -- 71% of Cambridge, and 82% of the parcels where setbacks can be computed.
