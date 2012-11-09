;;; Auto-generated PDDL file from prenex formula

(define (domain coloring)

	(:constants
		zero
		max
	)

	(:predicates
		(b ?x0)
		(g ?x0)
		(holds_and_11 ?x0 ?x1)
		(holds_and_24 ?x0)
		(holds_and_32 ?x0)
		(holds_and_40 ?x0)
		(holds_and_43 ?x0)
		(holds_forall_14 ?x0 ?x1)
		(holds_forall_44 ?x0)
		(holds_or_13 ?x0 ?x1)
		(holds_or_18 ?x0)
		(holds_or_26 ?x0)
		(holds_or_3 ?x0 ?x1)
		(holds_or_34 ?x0)
		(holds_or_42 ?x0)
		(holds_or_6 ?x0 ?x1)
		(holds_or_9 ?x0 ?x1)
		(not_b ?x0)
		(not_e ?x0 ?x1)
		(not_g ?x0)
		(not_r ?x0)
		(r ?x0)
		(suc ?x0 ?x1)
		(guess)
		(proof)
		(holds_goal)
	)

	(:action set_true_48
		:parameters	(?x0)
		:precondition	(and (not_r ?x0) (guess))
		:effect		(and (r ?x0) (not (not_r ?x0)))
	)
	(:action set_true_47
		:parameters	(?x0)
		:precondition	(and (not_g ?x0) (guess))
		:effect		(and (g ?x0) (not (not_g ?x0)))
	)
	(:action set_true_46
		:parameters	(?x0)
		:precondition	(and (not_b ?x0) (guess))
		:effect		(and (b ?x0) (not (not_b ?x0)))
	)
	(:action establish_forall_44_base
		:parameters	()
		:precondition	 (and (holds_and_43 zero) (proof))
		:effect		(holds_forall_44 zero)
	)
	(:action establish_forall_44_inductive
		:parameters	( ?iv0 ?iv1)
		:precondition	(and (holds_forall_44 ?iv0) (suc ?iv0 ?iv1) (holds_and_43 ?iv1) (proof))
		:effect		(holds_forall_44 ?iv1)
	)
	(:action establish_and_43
		:parameters	(?x)
		:precondition	(and (holds_forall_14 ?x max) (holds_or_18 ?x) (holds_or_26 ?x) (holds_or_34 ?x) (holds_or_42 ?x) (proof))
		:effect		(holds_and_43 ?x)
	)
	(:action establish_forall_14_base
		:parameters	(?x)
		:precondition	 (and (holds_or_13 zero ?x) (proof))
		:effect		(holds_forall_14 ?x zero)
	)
	(:action establish_forall_14_inductive
		:parameters	(?x ?iv0 ?iv1)
		:precondition	(and (holds_forall_14 ?x ?iv0) (suc ?iv0 ?iv1) (holds_or_13 ?iv1 ?x) (proof))
		:effect		(holds_forall_14 ?x ?iv1)
	)
	(:action establish_or_13_0
		:parameters	(?y ?x)
		:precondition	 (and (not_e ?x ?y) (proof))
		:effect		(holds_or_13 ?y ?x)
	)
	(:action establish_or_13_1
		:parameters	(?y ?x)
		:precondition	 (and (holds_and_11 ?y ?x) (proof))
		:effect		(holds_or_13 ?y ?x)
	)
	(:action establish_and_11
		:parameters	(?y ?x)
		:precondition	(and (holds_or_3 ?y ?x) (holds_or_6 ?y ?x) (holds_or_9 ?y ?x) (proof))
		:effect		(holds_and_11 ?y ?x)
	)
	(:action establish_or_3_0
		:parameters	(?y ?x)
		:precondition	 (and (not_r ?x) (proof))
		:effect		(holds_or_3 ?y ?x)
	)
	(:action establish_or_3_1
		:parameters	(?y ?x)
		:precondition	 (and (not_r ?y) (proof))
		:effect		(holds_or_3 ?y ?x)
	)
	(:action establish_or_6_0
		:parameters	(?y ?x)
		:precondition	 (and (not_g ?x) (proof))
		:effect		(holds_or_6 ?y ?x)
	)
	(:action establish_or_6_1
		:parameters	(?y ?x)
		:precondition	 (and (not_g ?y) (proof))
		:effect		(holds_or_6 ?y ?x)
	)
	(:action establish_or_9_0
		:parameters	(?y ?x)
		:precondition	 (and (not_b ?x) (proof))
		:effect		(holds_or_9 ?y ?x)
	)
	(:action establish_or_9_1
		:parameters	(?y ?x)
		:precondition	 (and (not_b ?y) (proof))
		:effect		(holds_or_9 ?y ?x)
	)
	(:action establish_or_18_0
		:parameters	(?x)
		:precondition	 (and (r ?x) (proof))
		:effect		(holds_or_18 ?x)
	)
	(:action establish_or_18_1
		:parameters	(?x)
		:precondition	 (and (g ?x) (proof))
		:effect		(holds_or_18 ?x)
	)
	(:action establish_or_18_2
		:parameters	(?x)
		:precondition	 (and (b ?x) (proof))
		:effect		(holds_or_18 ?x)
	)
	(:action establish_or_26_0
		:parameters	(?x)
		:precondition	 (and (not_r ?x) (proof))
		:effect		(holds_or_26 ?x)
	)
	(:action establish_or_26_1
		:parameters	(?x)
		:precondition	 (and (holds_and_24 ?x) (proof))
		:effect		(holds_or_26 ?x)
	)
	(:action establish_and_24
		:parameters	(?x)
		:precondition	(and (not_g ?x) (not_b ?x) (proof))
		:effect		(holds_and_24 ?x)
	)
	(:action establish_or_34_0
		:parameters	(?x)
		:precondition	 (and (not_g ?x) (proof))
		:effect		(holds_or_34 ?x)
	)
	(:action establish_or_34_1
		:parameters	(?x)
		:precondition	 (and (holds_and_32 ?x) (proof))
		:effect		(holds_or_34 ?x)
	)
	(:action establish_and_32
		:parameters	(?x)
		:precondition	(and (not_r ?x) (not_b ?x) (proof))
		:effect		(holds_and_32 ?x)
	)
	(:action establish_or_42_0
		:parameters	(?x)
		:precondition	 (and (not_b ?x) (proof))
		:effect		(holds_or_42 ?x)
	)
	(:action establish_or_42_1
		:parameters	(?x)
		:precondition	 (and (holds_and_40 ?x) (proof))
		:effect		(holds_or_42 ?x)
	)
	(:action establish_and_40
		:parameters	(?x)
		:precondition	(and (not_r ?x) (not_g ?x) (proof))
		:effect		(holds_and_40 ?x)
	)
	(:action begin-proof
		:precondition	(guess)
		:effect		(and (proof) (not (guess)))
	)
	(:action prove-goal
		:precondition	 (and (holds_forall_44  max) (proof))
		:effect		(holds_goal)
	)
)