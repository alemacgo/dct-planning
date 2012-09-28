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
		(itarate_t )
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
		:precondition	(and (coin_t ?x0) (not_t ?x0) (itarate_t) )
		:effect			(and (not (coin_t ?x0)) (not (not_t ?x0)) (t ?x0) (proof) )
	)
	(:action one_plus_one_0_t
		:parameters	( ?iv0 ?iv1)
		:precondition	(and  (itarate_t) (coin_t  ?iv0) (t  ?iv0) (suc ?iv1 ?iv0) )
		:effect			(and (not (coin_t  ?iv0)) (not (t  ?iv0)) (not_t  ?iv0) (coin_t  ?iv1) )
	)
	(:action one_plus_one_final_t
		:precondition	(and (itarate_t) ( max) (t  max))
		:effect	(and (not (itarate_t) ) (not (itarate_t) ) (not (coin_t  max)) (not (t  max)) (not_t  max) (holds_soforall_t) )
	)
	(:action change_for_coin_t
		:precondition	(and (itarate_t) (holds_exists_9 ))
		:effect	(and (not (proof)) (not (holds_exists_9 ))(coin_t zero) )
	)
	(:action init_so-forall_t
		:precondition	(and (itarate_t) (begin_so-forall_t))
		:effect	(and (not (begin_so-forall_t)) (proof) )
	)
	(:action establish_exists_9
		:parameters	( ?y)
		:precondition	 (and (holds_forall_8 ?y max) (proof))
		:effect		(and (holds_exists_9 ) (not (holds_forall_8 ?y max))))
	(:action establish_forall_8_base
		:parameters	(?y)
		:precondition	 (and (holds_or_7 ?y zero) (proof))
		:effect		(and (holds_forall_8 ?y zero) )
	)
	(:action establish_forall_8_inductive
		:parameters	(?y ?iv0 ?iv1)
		:precondition	(and (holds_forall_8 ?y ?iv0) (suc ?iv0 ?iv1) (holds_or_7 ?y ?iv1) (proof))
		:effect		(and  (not (holds_forall_8 ?y ?iv0))  (not (holds_or_7 ?y ?iv1)) (holds_forall_8 ?y ?iv1))
	)
	(:action establish_or_7_0
		:parameters	(?y ?x)
		:precondition	 (and (holds_and_3 ?y ?x) (proof))
		:effect		(and (holds_or_7 ?y ?x) (not (holds_and_3 ?y ?x)))
	)
	(:action establish_or_7_1
		:parameters	(?y ?x)
		:precondition	 (and (holds_and_6 ?y ?x) (proof))
		:effect		(and (holds_or_7 ?y ?x) (not (holds_and_6 ?y ?x)))
	)
	(:action establish_and_3
		:parameters	(?y ?x)
		:precondition	(and (p ?x ?y) (not_t ?x) (proof))
		:effect		(and (holds_and_3 ?y ?x) )
	)
	(:action establish_and_6
		:parameters	(?y ?x)
		:precondition	(and (n ?x ?y) (t ?x) (proof))
		:effect		(and (holds_and_6 ?y ?x) )
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