;;; Auto-generated PDDL file from prenex formula

(define (domain hamiltonian)

	(:constants
		zero
		max
	)

	(:predicates
		(e ?x0 ?x1)
		(f ?x0 ?x1)
		(free_domain_f ?x0)
		(free_range_f ?x0)
		(gt ?x0 ?x1)
		(holds_and_4 ?x0 ?x1 ?x2)
		(holds_and_7 ?x0 ?x1 ?x2)
		(holds_and_9 ?x0 ?x1)
		(holds_exists_10 ?x0)
		(holds_exists_5 ?x0 ?x1)
		(holds_exists_8 ?x0 ?x1)
		(holds_forall_13 ?x0)
		(holds_or_12 ?x0)
		(not_f ?x0 ?x1)
		(suc ?x0 ?x1)
		(guess)
		(proof)
		(holds_goal)
	)

	(:action set_true_15
		:parameters	(?x0 ?x1)
		:precondition	(and (not_f ?x0 ?x1)
		(free_domain_f ?x0)
		(free_range_f ?x1) (guess))
		:effect			(and (f ?x0 ?x1)
		(not (not_f ?x0 ?x1) ) (not (free_domain_f ?x0) )
		(not (free_range_f ?x1)))
	)
	(:action establish_forall_13_base
		:parameters	()
		:precondition	 (and (holds_or_12 zero) (proof))
		:effect		(holds_forall_13 zero)
	)
	(:action establish_forall_13_inductive
		:parameters	( ?iv0 ?iv1)
		:precondition	(and (holds_forall_13 ?iv0) (suc ?iv0 ?iv1) (holds_or_12 ?iv1) (proof))
		:effect		(holds_forall_13 ?iv1)
	)
	(:action establish_or_12_0
		:parameters	(?x)
		:precondition	 (and (or (gt ?x max) (= ?x max)) (proof))
		:effect		(holds_or_12 ?x)
	)
	(:action establish_or_12_1
		:parameters	(?x)
		:precondition	 (and (holds_exists_10 ?x) (proof))
		:effect		(holds_or_12 ?x)
	)
	(:action establish_exists_10
		:parameters	(?x ?y1)
		:precondition	 (and (holds_and_9 ?y1 ?x) (proof))
		:effect		(holds_exists_10 ?x)
	)
	(:action establish_and_9
		:parameters	(?y1 ?x)
		:precondition	(and (f ?x ?y1) (holds_exists_8 ?y1 ?x) (proof))
		:effect		(holds_and_9 ?y1 ?x)
	)
	(:action establish_exists_8
		:parameters	(?y1 ?x ?y2)
		:precondition	 (and (holds_and_7 ?y2 ?y1 ?x) (proof))
		:effect		(holds_exists_8 ?y1 ?x)
	)
	(:action establish_and_7
		:parameters	(?y2 ?y1 ?x)
		:precondition	(and (holds_exists_5 ?y2 ?x) (e ?y1 ?y2) (proof))
		:effect		(holds_and_7 ?y2 ?y1 ?x)
	)
	(:action establish_exists_5
		:parameters	(?y2 ?x ?x2)
		:precondition	 (and (holds_and_4 ?y2 ?x2 ?x) (proof))
		:effect		(holds_exists_5 ?y2 ?x)
	)
	(:action establish_and_4
		:parameters	(?y2 ?x2 ?x)
		:precondition	(and (suc ?x ?x2) (f ?x2 ?y2) (proof))
		:effect		(holds_and_4 ?y2 ?x2 ?x)
	)
	(:action begin-proof
		:precondition	(guess)
		:effect		(and (proof) (not (guess)))
	)
	(:action prove-goal
		:precondition	 (and (holds_forall_13  max) (proof))
		:effect		(holds_goal)
	)
)