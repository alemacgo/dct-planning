;;; Auto-generated PDDL file from prenex formula

(define (domain unsat)

	(:constants
		zero
		max
	)

	(:predicates
		(begin_so-forall_t )
		(coin_t ?x0)
		(holds_and_3 ?x0 ?x1)
		(holds_and_6 ?x0 ?x1)
		(holds_exists_9 )
		(holds_forall_8 ?x0 ?x1)
		(holds_or_7 ?x0 ?x1)
		(holds_soforall_t )
		(iterate_t )
		(n ?x0 ?x1)
		(not_t ?x0)
		(p ?x0 ?x1)
		(suc ?x0 ?x1)
		(t ?x0)
		(begin)
		(holds_goal)
	)

	(:action zero_plus_one_t
		:parameters	(?x0)
		:precondition	(and (coin_t ?x0) (not_t ?x0) (iterate_t) )
		:effect			(and (not (coin_t ?x0)) (not (not_t ?x0)) (t ?x0) (proof) )
	)
	(:action one_plus_one_0_t
		:parameters	( ?iv0 ?iv1)
		:precondition	(and  (iterate_t) (coin_t  ?iv0) (t  ?iv0) (suc ?iv1 ?iv0) )
		:effect			(and (not (coin_t  ?iv0)) (not (t  ?iv0)) (not_t  ?iv0) (coin_t  ?iv1) )
	)
	(:action one_plus_one_final_t
		:precondition	(and (iterate_t) (coin_t  max) (t  max))
		:effect	(and (not (iterate_t) ) (not (coin_t  max)) (not (t  max)) (not_t  max) (holds_soforall_t) )
	)
	(:action change_for_coin_t
		:precondition	(and (iterate_t) (holds_exists_9 ))
		:effect	(and (not (proof)) (not (holds_exists_9 ))(coin_t zero) )
	)
	(:action init_so-forall_t
		:precondition	(and (iterate_t) (begin_so-forall_t))
		:effect	(and (not (begin_so-forall_t)) (proof) )
	)
	(:action establish_exists_9
		:parameters	( ?y)
		:precondition	 (and (holds_forall_8 max ?y) (proof))
		:effect		(and (holds_exists_9 ) (not (holds_forall_8 max ?y)))
	)
	(:action establish_forall_8_base
		:parameters	(?y)
		:precondition	 (and (holds_or_7 zero ?y) (proof))
		:effect		(and (holds_forall_8 zero ?y)  (not (holds_or_7 zero ?y)))
	)
	(:action establish_forall_8_inductive
		:parameters	(?y ?iv0 ?iv1)
		:precondition	(and (holds_forall_8 ?iv0 ?y) (suc ?iv0 ?iv1) (holds_or_7 ?iv1 ?y) (proof))
		:effect		(and  (not (holds_forall_8 ?iv0 ?y))  (not (holds_or_7 ?iv1 ?y)) (holds_forall_8 ?iv1 ?y))
	)
	(:action establish_or_7_0
		:parameters	(?x ?y)
		:precondition	 (and (holds_and_3 ?x ?y) (proof))
		:effect		(and (holds_or_7 ?x ?y) (not (holds_and_3 ?x ?y)))
	)
	(:action establish_or_7_1
		:parameters	(?x ?y)
		:precondition	 (and (holds_and_6 ?x ?y) (proof))
		:effect		(and (holds_or_7 ?x ?y) (not (holds_and_6 ?x ?y)))
	)
	(:action establish_and_3
		:parameters	(?x ?y)
		:precondition	(and (p ?x ?y) (not_t ?x) (proof))
		:effect		(and (holds_and_3 ?x ?y) )
	)
	(:action establish_and_6
		:parameters	(?x ?y)
		:precondition	(and (n ?x ?y) (t ?x) (proof))
		:effect		(and (holds_and_6 ?x ?y) )
	)
	(:action begin-proof
		:precondition	(begin)
		:effect		 (and (iterate_t) (begin_so-forall_t)  (not (begin)))
	)
	(:action prove-goal
		:precondition	 (and (holds_so-forall_t))
		:effect		(holds_goal)
	)
)