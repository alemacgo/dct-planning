;;; Auto-generated PDDL file from prenex formula

(define (domain qbf)

	(:constants
		zero
		max
	)

	(:predicates
		(begin_so-forall_t )
		(coin_t ?x0)
		(e ?x0)
		(guess_r )
		(holds_and_15 ?x0)
		(holds_and_19 ?x0)
		(holds_and_21 ?x0 ?x1)
		(holds_and_4 ?x0)
		(holds_and_7 ?x0)
		(holds_and_9 ?x0 ?x1)
		(holds_exists_23 ?x0)
		(holds_forall_24 ?x0)
		(holds_or_20 ?x0)
		(holds_or_22 ?x0 ?x1)
		(holds_or_8 ?x0)
		(holds_so-exists_r )
		(holds_so-forall_t )
		(iterate_t )
		(n ?x0 ?x1)
		(not_e ?x0)
		(not_r ?x0)
		(not_t ?x0)
		(p ?x0 ?x1)
		(r ?x0)
		(so-forall_max_t ?x0)
		(so-forall_suc_t ?x0 ?x1)
		(so-forall_zero_t ?x0)
		(suc ?x0 ?x1)
		(t ?x0)
		(begin)
		(holds_goal)
	)

	(:action zero_plus_one_t
		:parameters	(?x0)
		:precondition	(and (coin_t ?x0) (not_t ?x0) (iterate_t)  )
		:effect			(and (not (coin_t ?x0)) (not (not_t ?x0)) (t ?x0) (guess_r) )
	)
	(:action one_plus_one_0_t
		:parameters	( ?iv0 ?iv1)
		:precondition	(and  (iterate_t) (coin_t  ?iv0) (t  ?iv0)  (so-forall_suc_t ?iv0 ?iv1) )
		:effect			(and (not (coin_t  ?iv0)) (not (t  ?iv0)) (not_t  ?iv0) (coin_t  ?iv1) )
	)
	(:action one_plus_one_final_t
		:parameters ( ?ivmax)
		:precondition	(and (iterate_t) (coin_t  ?ivmax) (t  ?ivmax)  (so-forall_max_t ?ivmax))
		:effect	(and (not (iterate_t) ) (not (coin_t  ?ivmax)) (not (t  ?ivmax)) (not_t  ?ivmax) (holds_so-forall_t) )
	)
	(:action change_for_coin_t
		:parameters ( ?ivzero)
		:precondition	(and (iterate_t) (holds_so-exists_r) (so-forall_zero_t ?ivzero))
		:effect	(and(not (holds_so-exists_r))(coin_t ?ivzero) )
	)
	(:action init_so-forall_t
		:precondition	(and (iterate_t) (begin_so-forall_t))
		:effect	(and (not (begin_so-forall_t)) (guess_r) )
	)
	(:action set_true_r
		:parameters	(?x0)
		:precondition	(and (not_r ?x0) (guess_r) )
		:effect			(and (r ?x0) (not (not_r ?x0)) )
	)
	(:action set_false_r
		:parameters	(?x0)
		:precondition	(and (r ?x0)  (guess_r) )
		:effect		(and (not_r ?x0) (not (r ?x0))   )
	)
	(:action end_guess_r
		:precondition	 (guess_r) 
		:effect		(and (proof_atom_level)(not (guess_r) ))
	)
	(:action establish_soexist_r
		:precondition	(and (holds_forall_24  max))
		:effect	(and(not (holds_forall_24  max)) (holds_so-exists_r)) 
	)
	(:action establish_forall_24_base
		:parameters	()
		:precondition	 (and (holds_exists_23 zero)  (proof_operator_level))
		:effect		(and (holds_forall_24 zero)  (not (holds_exists_23 zero)))
	)
	(:action establish_forall_24_inductive
		:parameters	( ?iv0 ?iv1)
		:precondition	(and (holds_forall_24 ?iv0) (suc ?iv0 ?iv1) (holds_exists_23 ?iv1)  (proof_operator_level))
		:effect		(and  (not (holds_forall_24 ?iv0))  (not (holds_exists_23 ?iv1)) (holds_forall_24 ?iv1))
	)
	(:action establish_exists_23
		:parameters	(?c ?x)
		:precondition	 (and (holds_or_22 ?c ?x)  (proof_operator_level))
		:effect		(and (holds_exists_23 ?c) (not (holds_or_22 ?c ?x))))
	(:action establish_or_22_0
		:parameters	(?c ?x)
		:precondition	 (and (holds_and_9 ?c ?x)  (proof_operator_level))
		:effect		(and (holds_or_22 ?c ?x) (not (holds_and_9 ?c ?x)))
	)
	(:action establish_or_22_1
		:parameters	(?c ?x)
		:precondition	 (and (holds_and_21 ?c ?x)  (proof_operator_level))
		:effect		(and (holds_or_22 ?c ?x) (not (holds_and_21 ?c ?x)))
	)
	(:action establish_and_9
		:parameters	(?c ?x)
		:precondition	(and (p ?x ?c) (holds_or_8 ?x)  (proof_operator_level))
		:effect		(and (holds_and_9 ?c ?x)  (not (holds_or_8 ?x)))
	)
	(:action establish_or_8_0
		:parameters	(?x)
		:precondition	 (and (holds_and_4 ?x)  (proof_operator_level))
		:effect		(and (holds_or_8 ?x) (not (holds_and_4 ?x)))
	)
	(:action establish_or_8_1
		:parameters	(?x)
		:precondition	 (and (holds_and_7 ?x)  (proof_operator_level))
		:effect		(and (holds_or_8 ?x) (not (holds_and_7 ?x)))
	)
	(:action establish_and_4
		:parameters	(?x)
		:precondition	(and (not_e ?x) (t ?x)  (proof_atom_level))
		:effect		(and (holds_and_4 ?x) )
	)
	(:action establish_and_7
		:parameters	(?x)
		:precondition	(and (e ?x) (r ?x)  (proof_atom_level))
		:effect		(and (holds_and_7 ?x) )
	)
	(:action establish_and_21
		:parameters	(?c ?x)
		:precondition	(and (n ?x ?c) (holds_or_20 ?x)  (proof_operator_level))
		:effect		(and (holds_and_21 ?c ?x)  (not (holds_or_20 ?x)))
	)
	(:action establish_or_20_0
		:parameters	(?x)
		:precondition	 (and (holds_and_15 ?x)  (proof_operator_level))
		:effect		(and (holds_or_20 ?x) (not (holds_and_15 ?x)))
	)
	(:action establish_or_20_1
		:parameters	(?x)
		:precondition	 (and (holds_and_19 ?x)  (proof_operator_level))
		:effect		(and (holds_or_20 ?x) (not (holds_and_19 ?x)))
	)
	(:action establish_and_15
		:parameters	(?x)
		:precondition	(and (not_e ?x) (not_t ?x)  (proof_atom_level))
		:effect		(and (holds_and_15 ?x) )
	)
	(:action establish_and_19
		:parameters	(?x)
		:precondition	(and (e ?x) (not_r ?x)  (proof_atom_level))
		:effect		(and (holds_and_19 ?x) )
	)
	(:action begin-proof
		:precondition	(begin)
		:effect		 (and (iterate_t) (begin_so-forall_t)  (not (begin)))
	)
	(:action finish-atom-proof
		:precondition	(proof_atom_level)
		:effect		 (and (proof_operator_level))
	)
	(:action prove-goal
		:precondition	 (and (holds_so-forall_t))
		:effect		(holds_goal)
	)
)