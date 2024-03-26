def eliminate_implication():
    pass


def move_negation_inward():
    # De Morgan Law
    # remove double nots
    pass


def standardize_variable_names():
    pass


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


def convert_to_cnf():
    # IDEA : return a set or a list of clauses
    eliminate_implication()
    move_negation_inward()
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
