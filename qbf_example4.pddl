(define (problem p)
	(:domain qbf)
	(:objects 			obj1 
			obj2 
			obj3 
			obj4 
			obj5 
			obj6 
			obj7 
			obj8 
			obj9 
			obj10 
			obj11 
			obj12 
			obj13 
			obj14 
			obj15 
			obj16 
			obj17 
			obj18 

	)
	(:init
		(begin)
		(suc zero obj1)
		(suc obj1 obj2)
		(suc obj2 obj3)
		(suc obj3 obj4)
		(suc obj4 obj5)
		(suc obj5 obj6)
		(suc obj6 obj7)
		(suc obj7 obj8)
		(suc obj8 obj9)
		(suc obj9 obj10)
		(suc obj10 obj11)
		(suc obj11 obj12)
		(suc obj12 obj13)
		(suc obj13 obj14)
		(suc obj14 obj15)
		(suc obj15 obj16)
		(suc obj16 obj17)
		(suc obj17 obj18)
		(suc obj18 max)
		(so-forall_suc_t zero obj1)
		(so-forall_suc_t obj1 obj2)
		(so-forall_zero_t zero)
		(so-forall_max_t obj2)
		(not_t zero)
		(not_t obj1)
		(not_t obj2)
		(not_e zero)
		(not_e obj1)
		(not_e obj2)
		(not_r obj3)
		(not_r obj4)
		(e obj3)
		(e obj4)
		(N zero zero)
		(N obj4 zero)
		(N obj3 zero)
		(P zero obj1)
		(P obj4 obj1)
		(N obj3 obj1)
		(P zero obj2)
		(N obj3 obj2)
		(N obj4 obj2)
		(P obj2 obj3)
		(P obj4 obj3)
		(P obj3 obj3)
		(N obj1 obj4)
		(N obj3 obj4)
		(P obj4 obj4)
		(P obj1 obj5)
		(P obj4 obj5)
		(N obj3 obj5)
		(P obj1 obj6)
		(N obj3 obj6)
		(N obj4 obj6)
		(P obj2 obj7)
		(P obj3 obj7)
		(P obj4 obj7)
		(N obj1 obj8)
		(P obj4 obj8)
		(N obj3 obj8)
		(N obj2 obj9)
		(P obj3 obj9)
		(P obj4 obj9)
		(N obj2 obj10)
		(N obj3 obj10)
		(N obj4 obj10)
		(N zero obj11)
		(N obj3 obj11)
		(P obj4 obj11)
		(N obj1 obj12)
		(P obj3 obj12)
		(P obj4 obj12)
		(N obj1 obj13)
		(N obj3 obj13)
		(N obj4 obj13)
		(N obj1 obj14)
		(N obj4 obj14)
		(P obj3 obj14)
		(N zero obj15)
		(P obj3 obj15)
		(P obj4 obj15)
		(N obj2 obj16)
		(P obj3 obj16)
		(N obj4 obj16)
		(N zero obj17)
		(N obj4 obj17)
		(P obj3 obj17)
		(N zero obj18)
		(N obj3 obj18)
		(N obj4 obj18)
		(N obj1 max)
		(P obj3 max)
		(N obj4 max)
	)
	(:goal (holds_goal)
	)
)