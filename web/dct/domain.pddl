;;; Auto-generated PDDL file from prenex formula

(define (domain problem)

	(:constants
		zero
		max
	)

	(:predicates
		(holds_and_2 ?x0 ?x1)
		(holds_and_6 ?x0 ?x1)
		(holds_exists_8 ?x0)
		(holds_forall_9 ?x0)
		(holds_or_7 ?x0 ?x1)
		(n ?x0 ?x1)
		(not_t ?x0)
		(p ?x0 ?x1)
		(suc ?x0 ?x1)
		(t ?x0)
		(guess)
		(proof)
		(holds_goal)
	)

	(:action set_true_11
		:parameters	(?x0)
		:precondition	(and (not_t ?x0) (guess))
		:effect		(and (t ?x0) (not (not_t ?x0)))
	)
	(:action establish_forall_9_base
		:parameters	()
		:precondition	 (and (holds_exists_8 zero) (proof))
		:effect		(holds_forall_9 zero)
	)
	(:action establish_forall_9_inductive
		:parameters	( ?iv0 ?iv1)
		:precondition	(and (holds_forall_9 ?iv0) (suc ?iv0 ?iv1) (holds_exists_8 ?iv1) (proof))
		:effect		(holds_forall_9 ?iv1)
	)
	(:action establish_exists_8
		:parameters	(?y ?x)
		:precondition	 (and (holds_or_7 ?y ?x) (proof))
		:effect		(holds_exists_8 ?y)
	)
	(:action establish_or_7_0
		:parameters	(?y ?x)
		:precondition	 (and (holds_and_2 ?y ?x) (proof))
		:effect		(holds_or_7 ?y ?x)
	)
	(:action establish_or_7_1
		:parameters	(?y ?x)
		:precondition	 (and (holds_and_6 ?y ?x) (proof))
		:effect		(holds_or_7 ?y ?x)
	)
	(:action establish_and_2
		:parameters	(?y ?x)
		:precondition	(and (p ?x ?y) (t ?x) (proof))
		:effect		(holds_and_2 ?y ?x)
	)
	(:action establish_and_6
		:parameters	(?y ?x)
		:precondition	(and (n ?x ?y) (not_t ?x) (proof))
		:effect		(holds_and_6 ?y ?x)
	)
	(:action begin-proof
		:precondition	(guess)
		:effect		(and (proof) (not (guess)))
	)
	(:action prove-goal
		:precondition	 (and (holds_forall_9  max) (proof))
		:effect		(holds_goal)
	)
)