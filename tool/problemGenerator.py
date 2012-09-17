#! /usr/bin/env python
from sys import argv
from instance_predicates import *

problem_path = argv[1]
fluents_string = argv[2]
quantified_relations_string = argv[3]
domain_name = argv[4]

fluents = {}
quantified_relations = {}

number_of_objects = 0
facts = []

def parse_fluents():
    for fluent in fluents_string[1:-1].split(','):
        fluents[fluent.split(':')[0].lstrip()] = \
            int(fluent.split(':')[1])

def parse_quantified_relations():
    for qr in quantified_relations_string[1:-1].split(','):
        quantified_relations[qr.split(':')[0].lstrip()[1:]] = \
            qr.split(':')[1].lstrip()

def parse_input_file(infile):
    lines = infile.readlines()
    try:
        global number_of_objects
        number_of_objects = int(lines[0])
    except Error:
        raise SystemExit("""The first line on the problem description should
                specify how many objects there are""")
    for line in lines[1:]:
        facts.append('(' + line.rstrip()[2:].lower())

try:
    instance_file = open(problem_path, "r")
    #instance_filename = problem_path.rpartition('.')[0].rpartition('/')[2]

    pddl_file = open(problem_path.rpartition('.')[0] + '.pddl', 'w')
    parse_fluents()
    parse_quantified_relations()
    print quantified_relations
    parse_input_file(instance_file)

    pddl_file.write("(define (problem a)\n")
    pddl_file.write("\t(:domain " + domain_name + ")\n")
    pddl_file.write("\t(:objects\n\t\t")

    objects = "\n\t\t".join(generate_obj(number_of_objects)) + "\n\t)"
    pddl_file.write(objects)

    pddl_file.write("\n\t(:init\n\t\t(guess)\n\t\t")

    for fluent in fluents:
        if fluent == 'suc':
            pddl_file.write("\n\t\t".join(generate_suc(number_of_objects)) + "\n\t\t")
        elif fluent == 'gt':
            pddl_file.write("\n\t\t".join(generate_gt(number_of_objects)) + "\n\t\t")
        elif fluent == 'geq':
            pddl_file.write("\n\t\t".join(generate_geq(number_of_objects)) + "\n\t\t")
        elif fluent == 'lt':
            pddl_file.write("\n\t\t".join(generate_lt(number_of_objects)) + "\n\t\t")
        elif fluent == 'leq':
            pddl_file.write("\n\t\t".join(generate_leq(number_of_objects)) + "\n\t\t")
        elif quantified_relations.has_key(fluent):
            if quantified_relations[fluent] == 'inj':
                pddl_file.write("\n\t\t".join(generate_free_rel_2arity(number_of_objects, fluent)) + "\n\t\t")
                pddl_file.write("\n\t\t".join(generate_free_domain(number_of_objects, fluent)) + "\n\t\t")
                pddl_file.write("\n\t\t".join(generate_free_range(number_of_objects, fluent)) + "\n\t\t")
            elif quantified_relations[fluent] == 'func':
                pddl_file.write("\n\t\t".join(generate_free_rel_2arity(number_of_objects, fluent)) + "\n\t\t")
                pddl_file.write("\n\t\t".join(generate_free_domain(number_of_objects, fluent)) + "\n\t\t")
            elif quantified_relations[fluent] == '1':
                pddl_file.write("\n\t\t".join(generate_free_rel_1arity(number_of_objects, fluent)) + "\n\t\t")
            elif quantified_relations[fluent] == '2':
                pddl_file.write("\n\t\t".join(generate_free_rel_1arity(number_of_objects, fluent)) + "\n\t\t")
            # work on the other cases
            else:
                raise SystemExit("""Not a supported arity for automatic
                        translation of the instance""")
        else:
            pass
        
    pddl_file.write("\n\t\t".join(facts) + "\n\t\t")
    pddl_file.write("\n\t)\n\t(:goal (holds_goal)\n\t)\n)")

except IOError:
    raise SystemExit("""The problem file was not found, or the output file could
            not be written""")
