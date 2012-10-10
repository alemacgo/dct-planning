(define (problem p)
	(:domain unsat)
	(:objects zero
	 		obj1
			obj2
			max 
	)
	(:init
		(begin)
        (care_t zero)
        (care_t obj1)
        (dont_care_t obj2)
        (dont_care_t max)
		(suc zero obj1)
		(suc obj1 obj2)
		(suc obj2 max)
        (so-forall_suc_t zero obj1)
        (so-forall_max_t obj1)
        (so-forall_zero_t zero)
        (not_t zero)
		(not_t obj1)
		(not_t obj2)
		(not_t max)
        (P zero zero)
		(P obj1 zero)
		(P zero obj1)
		(N obj1 obj1)
		(N zero obj2)
		(P obj1 obj2)
		(N zero max)
        (N obj1 max)
        (M obj2 zero)
		(M obj2 obj1)
		(M obj2 obj2)
		(M obj2 max)
        (M max zero)
		(M max obj1)
		(M max obj2)
		(M max max)
	)
	(:goal (holds_goal)
	)
)
