"""
Faculty Of Computers & Artificial Intelligence - Cairo University
Authors:
Khaled Waleed Al-Shaer 20210127
Omar Kouta 20220528

Reasoning and Knowledge Representation - Assignment 1

CNF Converter for First Order Logic
"""
import copy


class Node:
    def __init__(self, type, value):  # Constructor
        self.set_node(type, value)
        self.children = []

    def set_node(self, type, value):
        self.type = type
        self.value = value

    def add_child(self, node):
        self.children.append(node)

    def set_children(self, children):
        self.children = children

    def get_children(self):
        return self.children

    def get_type(self):
        return self.type

    def get_value(self):
        return self.value

    def get_text(self):
        return "[" + self.get_type() + "] " + self.get_value()

    def __str__(self, level=0):
        text = "--" * level + self.get_text() + "\n"
        for child_node in self.children:
            text += child_node.__str__(level + 1)
        return text


def parser(statements):
    arguments = []

    return True


def correct(tree):
    return True


def remove_conditionals(tree):
    tree = Node("NOT", "x") # TODO: remove this, this is only for IDE help
    parent_type = tree.get_type()
    parent_value = tree.get_value()

    children = tree.get_children()

    if parent_type == "op" and parent_value == "IMPLIES":
        tree.set_node("op", "OR")

        child = children[-1]

        new_node = Node("op", "NOT")
        new_node.add_child(child)

        children[-1] = new_node

        tree.set_children(children)

    children = tree.get_children()
    for i in range(len(children)):
        remove_conditionals(children[i])

    return tree


def deMorgan(tree):
    parent = tree
    parent_type = tree.get_type()
    parent_value = tree.get_value()

    children = tree.get_children()

    if parent_type == "op" and parent_value == "Not":
        child = children[0]

        child_type = child.get_type()
        child_value = child.get_value()

        new_type = new_value = ""

        # Reversing the Operator / Quantifier
        if child_type == "op":
            new_type = "op"
            if child_value == "AND":
                new_value = "OR"
            elif child_value == "OR":
                new_value = "AND"

        elif child_type == "quant":
            new_type = "quant"
            if child_value == "FORALL":
                new_value = "EXISTS"
            elif child_value == "EXISTS":
                new_value = "FORALL"

        if new_type != "" and new_value != "":
            tree.set_node(new_type, new_value)

            grandsons = child.get_children()

            new_children = []

            for grandson in grandsons:
                grandson_type = grandson.get_type()

                if grandson_type == "variable":
                    new_children.append(grandson)
                else:
                    new_node = Node(parent_type, parent_value)
                    new_node.add_child(grandson)

                    new_children.append(new_node)

            tree.set_children(new_children)

    children = tree.get_children()
    for i in range(len(children)):
        deMorgan(children[i])

    return tree


def double_not(tree):
    return True


def standardize(tree):
    return True


def all_left(tree):
    return True


def skolemize(tree):
    return True


def drop_universal(tree):
    return True


def fix_symbols(tree):
    return True


def CNF(tree):
    return True


def clausal_from_ands(tree):
    return True


def resolution(clauses):
    return True


def determine_if_true(statement):
    clauses = []
    for i in range(0, len(statement)):  # for all statements within a list of statement
        tree = parser(statement[i])
        tree = correct(tree)  # TODO: We DON"T UNDERSTAND WHAT THIS DOES
        tree = remove_conditionals(tree)
        tree = deMorgan(tree)
        tree = double_not(tree)
        tree = standardize(tree)
        tree = all_left(tree)
        tree = skolemize(tree)
        tree = drop_universal(tree)
        tree = fix_symbols(tree)
        tree = CNF(tree)

        # TODO: Understand this
        predicates = clausal_from_ands(tree)
        clauses.append(predicates)
    return resolution(clauses)


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
