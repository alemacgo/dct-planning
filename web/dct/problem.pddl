(define (problem a)
	(:domain problem)
	(:objects
		obj1
		obj2
	)
	(:init
		(guess)
		(suc zero obj1)
		(suc obj1 obj2)
		(suc obj2 max)
		(not_t zero)
		(not_t obj1)
		(not_t obj2)
		(not_t max)
		(p zero zero)
		(n zero obj1)
		(n zero obj2)
		(p obj2 zero)
		(n obj1 zero)
		(n obj2 obj1)
		(p obj1 obj2)
		(p zero max)
		
	)
	(:goal (holds_goal)
	)
)