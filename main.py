"""
Faculty Of Computers & Artificial Intelligence - Cairo University
Authors:
Khaled Waleed Al-Shaer 20210127
Omar Kouta 20220528

Reasoning and Knowledge Representation - Assignment 1

CNF Converter for First Order Logic
"""
import copy


def parser(statements):
    arguments = []

    return True

def remove_conditionals(tree):
    return True

def deMorgan():

def determine_if_true(statement):
    clauses = []
    for i in range(0, len(statement)): # for all statements within a list of statement
        tree = parser(statement[i])
        # tree = correct(tree) # TODO: We DON"T UNDERSTAND WHAT THIS DOES
        tree = remove_conditionals(tree)
        tree = deMorgan()



    return True  # TODO


def find_true_statements(statements):
    results = []
    for i in range(0, len(statements)):
        try:
            statements[i] = determine_if_true(statements[i])
            if statements[i]:
                results.append(i)
        except Exception:
            continue
    return results


statements = [["(FORALL x (IMPLIES (p x) (q x)))", "(p (f a))", "(NOT (q (f a)))"]]  # this is inconsistent

print(find_true_statements(statements))
