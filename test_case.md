
Test case	/ Expected result
Single product fits:	A suitable box is accepted
Product fits after rotation:	Rotation is considered
Product exceeds box dimensions	:Box is rejected
Multiple products fit together:	Non-overlapping placement succeeds
Products individually fit but cannot fit together:	Packing attempt is rejected
Cheapest suitable box:	Lowest-cost feasible box is recommended
Insufficient weight capacity:	Box is excluded
Inactive box	:Box is excluded
Empty order:	Clear failure response
Nonexistent order ID	:API returns HTTP 404
No suitable box	:API returns HTTP 422