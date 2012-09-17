;;; Auto-generated PDDL file from prenex formula

(define (domain kcolorability)

	(:constants
		zero
		max
	)

	(:predicates
		(f ?x0 ?x1)
		(free_domain_f ?x0)
		(holds_and_13 ?x0)
		(holds_and_2 ?x0 ?x1)
		(holds_exists_3 ?x0)
		(holds_forall_12 ?x0 ?x1)
		(holds_forall_14 ?x0)
		(holds_forall_9 ?x0 ?x1 ?x2)
		(holds_or_11 ?x0 ?x1)
		(holds_or_7 ?x0 ?x1 ?x2)
		(k ?x0)
		(not_e ?x0 ?x1)
		(not_f ?x0 ?x1)
		(suc ?x0 ?x1)
		(choosing_true_values)
		(building_proof)
		(holds_goal)
	)

	(:action set_true_16
		:parameters	(?x0 ?x1)
		:precondition	(and (not_f ?x0 ?x1) (free_domain_f ?x0) (choosing_true_values))
		:effect		(and (f ?x0 ?x1) (not (not_f ?x0 ?x1)) (not (free_domain_f ?x0)))
	)
	(:action establish_forall_14_base
		:parameters	()
		:precondition	 (and (holds_and_13 zero) (building_proof))
		:effect		(holds_forall_14 zero)
	)
	(:action establish_forall_14_inductive
		:parameters	( ?iv0 ?iv1)
		:precondition	(and (holds_forall_14 ?iv0) (suc ?iv0 ?iv1) (holds_and_13 ?iv1) (building_proof))
		:effect		(holds_forall_14 ?iv1)
	)
	(:action establish_and_13
		:parameters	(?x)
		:precondition	(and (holds_exists_3 ?x) (holds_forall_12 ?x max) (building_proof))
		:effect		(holds_and_13 ?x)
	)
	(:action establish_exists_3
		:parameters	(?x ?y)
		:precondition	 (and (holds_and_2 ?y ?x) (building_proof))
		:effect		(holds_exists_3 ?x)
	)
	(:action establish_and_2
		:parameters	(?y ?x)
		:precondition	(and (f ?x ?y) (k ?y) (building_proof))
		:effect		(holds_and_2 ?y ?x)
	)
	(:action establish_forall_12_base
		:parameters	(?x)
		:precondition	 (and (holds_or_11 zero ?x) (building_proof))
		:effect		(holds_forall_12 ?x zero)
	)
	(:action establish_forall_12_inductive
		:parameters	(?x ?iv0 ?iv1)
		:precondition	(and (holds_forall_12 ?x ?iv0) (suc ?iv0 ?iv1) (holds_or_11 ?iv1 ?x) (building_proof))
		:effect		(holds_forall_12 ?x ?iv1)
	)
	(:action establish_or_11_0
		:parameters	(?y ?x)
		:precondition	 (and (not_e ?x ?y) (building_proof))
		:effect		(holds_or_11 ?y ?x)
	)
	(:action establish_or_11_1
		:parameters	(?y ?x)
		:precondition	 (and (holds_forall_9 ?y ?x max) (building_proof))
		:effect		(holds_or_11 ?y ?x)
	)
	(:action establish_forall_9_base
		:parameters	(?y ?x)
		:precondition	 (and (holds_or_7 zero ?y ?x) (building_proof))
		:effect		(holds_forall_9 ?y ?x zero)
	)
	(:action establish_forall_9_inductive
		:parameters	(?y ?x ?iv0 ?iv1)
		:precondition	(and (holds_forall_9 ?y ?x ?iv0) (suc ?iv0 ?iv1) (holds_or_7 ?iv1 ?y ?x) (building_proof))
		:effect		(holds_forall_9 ?y ?x ?iv1)
	)
	(:action establish_or_7_0
		:parameters	(?z ?y ?x)
		:precondition	 (and (not_f ?x ?z) (building_proof))
		:effect		(holds_or_7 ?z ?y ?x)
	)
	(:action establish_or_7_1
		:parameters	(?z ?y ?x)
		:precondition	 (and (not_f ?y ?z) (building_proof))
		:effect		(holds_or_7 ?z ?y ?x)
	)
	(:action move_on
		:precondition	(choosing_true_values)
		:effect		(and (building_proof) (not (choosing_true_values)))
	)
	(:action establish_goal
		:precondition	 (and (holds_forall_14  max) (building_proof))
		:effect		(holds_goal)
	)
)