"""
Faculty Of Computers & Artificial Intelligence - Cairo University
Authors:
Khaled Waleed Al-Shaer 20210127
Omar Kouta 20220528

Reasoning and Knowledge Representation - Assignment 1

CNF Converter for First Order Logic
"""
import copy

operations = ["IF", "AND", "OR", "NOT", "IMPLIES"]
quantifiers = ["FORALL", "EXISTS"]


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


def parse_tree(args):
    stack = []
    for i in range(len(args)):
        current_index = i

        element = args[current_index]
        element_type = element[0]
        element_value = element[1]

        if element_type == "open_bracket":
            continue
        elif element_type == "close_bracket":  # final destination
            picked = []
            while True:
                parent = stack.pop()

                parent_type = parent.get_element_type()
                parent_value = parent.get_element_value()

                if parent_type == "op" or parent_type == "quant" or parent_type == "function" or parent_type == "predicate":
                    children = parent.get_child_nodes()
                    children_nums = len(children)

                    if children_nums < 1:
                        break

                picked.append(parent)

            parent.set_child_nodes(picked)

            stack.append(parent)

        else:
            node = Node(element_type, element_value)
            stack.append(node)

    assert (len(stack) == 1)

    return stack.pop()


def parser(statements):
    global prev_arg, arg_type
    characters = statements
    args = []

    arg_list = characters.replace('(', ' ( ').replace(')', ' ) ').split()
    for i in range(len(arg_list)):
        arg = arg_list[i]
        if i - 1 >= 0:
            prev_arg = arg_list[i - 1]
        if i + 1 < len(arg_list):
            next_arg = arg_list[i + 1]

        if arg == "(":
            arg_type = "open_bracket"
        elif arg == ")":
            arg_type = "close_bracket"
        elif prev_arg == "(":
            if arg in operations:
                arg_type = "op"
            elif arg in quantifiers:
                arg_type = "quant"
            else:
                arg_type = "function"
        elif prev_arg in quantifiers:
            arg_type = "variable"  # quantifier counter
        elif arg.isalnum():  # alpha-number
            arg_type = "symbol"

        arg_tuple = (arg_type, arg)
        args.append(arg_tuple)

    return parse_tree(args)


def correct(tree):
    return True


def remove_conditionals(tree):
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
    current_node = tree
    parent_value = tree.get_value()

    if len(current_node.get_children()) == 0:
        return tree

    if parent_value == "NOT":
        child = current_node.get_children()[0]  # it must have only 1 child
        child_value = child.get_value()

        if child_value == "NOT":
            current_node.set_node(child.get_children()[0].get_type(),
                                  child.get_children()[0].get_value())

        if len(current_node.get_children()[0].get_children()[0]) == 2:
            current_node.get_children()[1] = \
                current_node.get_children()[0].get_children()[0].get_children()[1]

        current_node.get_children()[0] = \
            current_node.get_children()[0].get_children()[0].get_children()[0]

        double_not(current_node)

    if len(current_node.get_children()) == 2:
        double_not(current_node.get_children()[1])

    double_not(current_node.get_children()[0])

    return tree


def standardize(tree):
    return True


def all_left(tree):
    def prenex_check(tree):
        parent_type = tree.get_type()

        children = tree.get_children()

        if len(children) != 2:
            return True

        left_child = children[1]
        left_child_type = left_child.get_type()

        right_child = children[0]
        right_child_type = right_child.get_type()

        if parent_type != "quant" and (left_child_type == "quant" or right_child_type == "quant"):
            return False
        else:
            return prenex_check(left_child) and prenex_check(right_child)

    def prenex_convert(tree):
        parent = tree
        parent_type = parent.get_type()

        children = parent.get_children()

        if len(children) != 2:
            return tree

        left_child = children[1]
        left_child_type = left_child.get_type()
        left_child_value = left_child.get_value()
        left_child_children = left_child.get_children()

        right_child = children[0]
        right_child_type = right_child.get_type()
        right_child_value = right_child.get_value()
        right_child_children = right_child.get_children()

        if parent_type == "op" and left_child_type == "quant":
            left_child_left = left_child_children[1]
            left_child_left_type = left_child_left.get_type()
            left_child_left_value = left_child_left.get_value()

            temp_type = parent.get_type()
            temp_value = parent.get_value()

            parent.set_node(left_child_type, left_child_value)
            left_child.set_node(temp_type, temp_value)

            temp = Node(left_child_left_type, left_child_left_value)
            left_child.get_children()[1] = left_child.get_children()[0]
            left_child.get_children()[0] = parent.get_children()[0]
            parent.get_children()[0] = parent.get_children()[1]
            parent.get_children()[1] = temp

        elif parent_type == "op" and right_child_type == "quant":
            right_child_left = right_child_children[1]
            right_child_left_type = right_child_left.get_type()
            right_child_left_value = right_child_left.get_value()

            temp_type = parent.get_type()
            temp_value = parent.get_value()

            parent.set_node(right_child_type, right_child_value)
            right_child.set_node(temp_type, temp_value)

            temp = Node(right_child_left_type, right_child_left_value)
            right_child.get_children()[1] = parent.get_children()[1]
            parent.get_children()[1] = temp

        prenex_convert(left_child)
        prenex_convert(right_child)

        return tree



    is_good = prenex_check(tree)
    if is_good:
        return tree
    else:
        tree = prenex_convert(tree)
        return all_left(tree)


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
