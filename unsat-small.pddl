(define (problem p)
	(:domain unsat)
	(:objects zero 
			max 
	)
	(:init
		(begin)
		(suc zero max)
		(not_t zero)
		(not_t max)
        (P zero zero)
        (N zero max)
        (M max zero)
        (M max max)
	)
	(:goal (holds_goal)
	)
)
