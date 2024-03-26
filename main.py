"""
Faculty Of Computers & Artificial Intelligence - Cairo University
Authors:
Khaled Waleed Al-Shaer 20210127
Omar Kouta 2022______ TODO

Reasoning and Knowledge Representation - Assignment 1

CNF Converter for First Order Logic
"""

"""
Documentation for Usage

- Every sentence is a list
- Every sentence consists of an operator and operands (also called literals)
- For example A ^ (B or C) => ["and", "A", ["or", "B", "C"]]

Available operators or quantifiers with Examples ("A" or any constant like it can be altered by another sentence)
["not", "A"]
["or", "A", "B"]
["and", "A", "B"]
["implies", "A", "B"]
["iff", "A", "B"]

"""

def isConstant(expression):
    if expression[0] in ["and", "or", "not", "implies", "iff", "exist", "all"]:
        return False
    return True


def remove_biconditional(expression):
    # A <--> B == ["iff", "A", "B"]
    if expression[0] == "iff":
        literal1 = expression[1]
        literal2 = expression[2]
        expression[0] = "and"
        expression[1] = ["implies", literal1, literal2]
        expression[2] = ["implies", literal2, literal1]

    for literal in expression:
        if len(literal) > 1:
            remove_biconditional(literal)


def remove_imply(expression):
    # A --> B [implies, A, B] == [or, [not, A], B]
    if expression[0] == "implies":
        literal1 = expression[1]

        expression[0] = "or"
        expression[1] = ["not", literal1]

    for literal in expression:
        if len(literal) > 1:
            remove_imply(literal)


def eliminate_implication(expression):
    remove_biconditional(expression)
    remove_imply(expression)


def deMorgan(expression):  # [not, [not, P]] == [and, [not, literal1], [not, literal2]]
    if expression[0] == "not":
        literal = expression[1]

        if literal[0] == "not":
            del expression[:]
            # check if variable, then append
            if (len(literal[1]) == 1):
                expression.append(literal[1])
            # if operator or list
            else:
                for lit in literal[1]:
                    expression.append(lit)

                # recursive on inner lists
                if (len(expression) > 1):
                    deMorgan(expression)


        elif literal[0] == "or":
            del expression[:]
            expression.append("and")
            for lit in literal:
                if lit == "or":
                    continue
                else:
                    expression.append(["not", lit])


        elif literal[0] == "and":
            del expression[:]
            expression.append("or")
            for lit in literal:
                if lit == "and":
                    continue
                else:
                    expression.append(["not", lit])


        elif literal[0] == "exist":  # [not, [exist, P]] == [all, [not, P]]
            del expression[:]
            expression.append("all")
            for lit in literal:
                if lit == "exist":
                    continue
                else:
                    expression.append(["not", lit])


        elif literal[0] == "all":  # [not, [all, P]] == [exist, [not, P]]
            del expression[:]
            expression.append("exist")
            for lit in literal:
                if lit == "all":
                    continue
                else:
                    expression.append(["not", lit])

    for literal in expression:
        if len(literal) > 1:
            deMorgan(literal)


def move_negation_inward(expression):
    # De Morgan Law
    deMorgan(expression)


def standardize_variable_names(expression):
    independent_var = {}
    def search_for_indepenedent_variables(expression):





def move_quantifiers_left():
    pass


def skolemize():
    # remove existential quantifiers and replace it by skolem constant or skolem function
    pass


def remove_universal():
    pass


def convert_to_conjuctive_form():
    # use distribution law to distribute AND over OR
    pass


def make_clauses():
    # rename variable names again
    standardize_variable_names()
    # put clauses in set
    pass


def unification():
    # an inner step in resolution can be used if needed
    pass


def convert_to_cnf(expression):
    # IDEA : return a set or a list of clauses
    eliminate_implication(expression)
    move_negation_inward(expression)
    standardize_variable_names()
    move_quantifiers_left()

    # TODO: Khaled's Work
    skolemize()
    remove_universal()
    convert_to_conjuctive_form()
    make_clauses()
    pass


# TODO: Khaled's Work
def apply_resolution():
    convert_to_cnf()

    # use unification if needed
    unification()

    # resolution
    pass


print(deMorgan(["all", ["not", ["exist", "A"]]]))
