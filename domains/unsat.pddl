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
		(holds_exists_10 )
		(holds_forall_9 ?x0 ?x1)
		(holds_or_8 ?x0 ?x1)
		(holds_soforall_t )
		(iterate_t )
		(m ?x0 ?x1)
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
		:precondition	(and  (iterate_t) (coin_t  ?iv0) (t  ?iv0) (suc ?iv0 ?iv1) )
		:effect			(and (not (coin_t  ?iv0)) (not (t  ?iv0)) (not_t  ?iv0) (coin_t  ?iv1) )
	)
	(:action one_plus_one_final_t
		:precondition	(and (iterate_t) (coin_t  max) (t  max))
		:effect	(and (not (iterate_t) ) (not (coin_t  max)) (not (t  max)) (not_t  max) (holds_soforall_t) )
	)
	(:action change_for_coin_t
		:precondition	(and (iterate_t) (holds_exists_10 ))
		:effect	(and (not (proof)) (not (holds_exists_10 ))(coin_t zero) )
	)
	(:action init_so-forall_t
		:precondition	(and (iterate_t) (begin_so-forall_t))
		:effect	(and (not (begin_so-forall_t)) (proof) )
	)
	(:action establish_exists_10
		:parameters	( ?y)
		:precondition	 (and (holds_forall_9 ?y max) (proof))
		:effect		(and (holds_exists_10 ) (not (holds_forall_9 ?y max))))
	(:action establish_forall_9_base
		:parameters	(?y)
		:precondition	 (and (holds_or_8 ?y zero) (proof))
		:effect		(and (holds_forall_9 ?y zero)  (not (holds_or_8 ?y zero)))
	)
	(:action establish_forall_9_inductive
		:parameters	(?y ?iv0 ?iv1)
		:precondition	(and (holds_forall_9 ?y ?iv0) (suc ?iv0 ?iv1) (holds_or_8 ?y ?iv1) (proof))
		:effect		(and  (not (holds_forall_9 ?y ?iv0))  (not (holds_or_8 ?y ?iv1)) (holds_forall_9 ?y ?iv1))
	)
	(:action establish_or_8_0
		:parameters	(?y ?x)
		:precondition	 (and (holds_and_3 ?y ?x) (proof))
		:effect		(and (holds_or_8 ?y ?x) (not (holds_and_3 ?y ?x)))
	)
	(:action establish_or_8_1
		:parameters	(?y ?x)
		:precondition	 (and (holds_and_6 ?y ?x) (proof))
		:effect		(and (holds_or_8 ?y ?x) (not (holds_and_6 ?y ?x)))
	)
	(:action establish_or_8_2
		:parameters	(?y ?x)
		:precondition	 (and (m ?x ?y) (proof))
		:effect		(and (holds_or_8 ?y ?x))
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