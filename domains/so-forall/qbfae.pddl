;;; Auto-generated PDDL file from prenex formula

(define (domain qbfae)

	(:constants
		zero
		max
	)

	(:predicates
		(begin_so-forall_t )
		(coin_t ?x0)
		(guess_r )
		(holds_and_11 ?x0 ?x1)
		(holds_and_4 ?x0 ?x1)
		(holds_exists_13 ?x0)
		(holds_forall_14 ?x0)
		(holds_or_10 ?x0)
		(holds_or_12 ?x0 ?x1)
		(holds_or_3 ?x0)
		(holds_so-exists_r )
		(holds_so-forall_t )
		(iterate_t )
		(n ?x0 ?x1)
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
		(proof)
	)

	(:action establish_or_10_0
		:parameters	(?x)
		:precondition	 (and (not_t ?x)  (proof))
		:effect		(and (holds_or_10 ?x))
	)
	(:action establish_or_10_1
		:parameters	(?x)
		:precondition	 (and (not_r ?x)  (proof))
		:effect		(and (holds_or_10 ?x))
	)
	(:action establish_and_11
		:parameters	(?c ?x)
		:precondition	(and (n ?x ?c) (holds_or_10 ?x)  (proof))
		:effect		(and (holds_and_11 ?c ?x) )
	)
	(:action establish_or_3_0
		:parameters	(?x)
		:precondition	 (and (t ?x)  (proof))
		:effect		(and (holds_or_3 ?x))
	)
	(:action establish_or_3_1
		:parameters	(?x)
		:precondition	 (and (r ?x)  (proof))
		:effect		(and (holds_or_3 ?x))
	)
	(:action establish_and_4
		:parameters	(?c ?x)
		:precondition	(and (p ?x ?c) (holds_or_3 ?x)  (proof))
		:effect		(and (holds_and_4 ?c ?x) )
	)
	(:action establish_or_12_0
		:parameters	(?c ?x)
		:precondition	 (and (holds_and_4 ?c ?x)  (proof))
		:effect		(and (holds_or_12 ?c ?x))
	)
	(:action establish_or_12_1
		:parameters	(?c ?x)
		:precondition	 (and (holds_and_11 ?c ?x)  (proof))
		:effect		(and (holds_or_12 ?c ?x))
	)
	(:action establish_exists_13
		:parameters	(?c ?x)
		:precondition	 (and (holds_or_12 ?c ?x)  (proof))
		:effect		(and (holds_exists_13 ?c))
	)
	(:action establish_forall_14_base
		:parameters	()
		:precondition	 (and (holds_exists_13 zero)  (proof))
		:effect		(and (holds_forall_14 zero) )
	)
	(:action establish_forall_14_inductive
		:parameters	( ?iv0 ?iv1)
		:precondition	(and (holds_forall_14 ?iv0) (suc ?iv0 ?iv1) (holds_exists_13 ?iv1)  (proof))
		:effect		(and   (holds_forall_14 ?iv1))
	)
	(:action set_true_r
		:parameters	(?x0)
		:precondition	(and  (not_r ?x0) (guess_r) )
		:effect			(and (r ?x0) (not  (not_r ?x0)) )
	)
	(:action set_false_r
		:parameters	(?x0)
		:precondition	(and (r ?x0)  (guess_r) )
		:effect		(and  (not_r ?x0) (not (r ?x0))   )
	)
	(:action end_guess_r
		:precondition	 (guess_r) 
		:effect		(and (proof) (not (guess_r) ))
	)
	(:action dummy_guess_r
		:precondition	 (guess_r) 
		:effect	 (guess_r) )
	(:action establish_soexist_r
		:precondition	(and (holds_forall_14  max))
		:effect	(and (not (holds_forall_14  max)) (holds_so-exists_r)  (not (proof))
				(forall (?ivDel0 ?ivDel1) (not (holds_or_12 ?ivDel0 ?ivDel1)))
				(forall (?ivDel0 ?ivDel1) (not (holds_and_4 ?ivDel0 ?ivDel1)))
				(forall (?ivDel0) (not (holds_or_3 ?ivDel0)))
				(forall (?ivDel0) (not (holds_exists_13 ?ivDel0)))
				(forall (?ivDel0) (not (holds_forall_14 ?ivDel0)))
				(forall (?ivDel0) (not (holds_or_10 ?ivDel0)))
				(forall (?ivDel0 ?ivDel1) (not (holds_and_11 ?ivDel0 ?ivDel1))))
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
		:parameters (?ivmax0)
		:precondition	(and (iterate_t) (coin_t ?ivmax0) (t ?ivmax0) (so-forall_max_t ?ivmax0))
		:effect	(and (not (iterate_t) ) (not (coin_t  ?ivmax0)) (not (t ?ivmax0)) (not_t ?ivmax0) (holds_so-forall_t) )
	)
	(:action change_for_coin_t
		:parameters (?ivzero0)
		:precondition	(and (iterate_t) (holds_so-exists_r)(so-forall_zero_t ?ivzero0))
		:effect	(and (not (holds_so-exists_r)) (coin_t ?ivzero0) )
	)
	(:action init_so-forall_t
		:precondition	(and (iterate_t) (begin_so-forall_t))
		:effect	(and (not (begin_so-forall_t)) (guess_r) )
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