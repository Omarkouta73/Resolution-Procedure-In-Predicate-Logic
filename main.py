"""
Faculty Of Computers & Artificial Intelligence - Cairo University
Authors:
Khaled Waleed Al-Shaer 20210127
Omar Kouta 20220528

Reasoning and Knowledge Representation - Assignment 1

CNF Converter for First Order Logic
"""
import copy
import itertools
import random

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

                parent_type = parent.get_type()
                parent_value = parent.get_value()

                if parent_type == "op" or parent_type == "quant" or parent_type == "function" or parent_type == "predicate":
                    children = parent.get_children()
                    children_nums = len(children)

                    if children_nums < 1:
                        break

                picked.append(parent)

            parent.set_child_nodes(picked)

            stack.append(parent)

        else:
            node = Node(element_type, element_value)
            stack.append(node)

    while (len(stack) > 1):
        childs = []
        childs.append(stack.pop())
        childs.append(stack.pop())
        stack[-1].set_child_nodes(childs)

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
    S_type = tree.get_type()
    S_value = tree.get_value()

    children = tree.get_children()

    for i in range(len(children)):
        child = children[i]

        ch_type = child.get_type()
        ch_value = child.get_value()

        if (S_type == "function"):
            if (ch_type == "function"):
                S_type = "predicate"
                tree.set_node(S_type, S_value)

        if (S_type == "op" or S_type == "quant"):
            if (ch_type == "function"):
                ch_type = "predicate"
                child.set_node(ch_type, ch_value)

                children[i] = child

        if (S_type == "predicate"):
            if (ch_type == "symbol"):
                ch_type = "variable"
                child.set_node(ch_type, ch_value)

                children[i] = child

        correct(child)

    tree.set_child_nodes(children)

    return tree


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
    variable_names = {}
    S_type = tree.get_type()
    S_value = tree.get_value()

    children = tree.get_children()

    if S_type == "quant":
        child = children[-1]

        ch_type = child.get_type()
        ch_value = child.get_value()

        variable_names[ch_value] = ch_value + "_" + str(random.randint(0, 10000))

        child.set_node(ch_type, variable_names[ch_value])

        children[-1] = child

    elif S_type == "function" or S_type == "predicate":
        for i in range(len(children)):
            child = children[i]
            ch_type = child.get_type()
            ch_value = child.get_value()

            if ch_value in variable_names:
                child.set_node(ch_type, variable_names[ch_value])

            children[i] = child

    tree.set_child_nodes(children)
    for i in range(len(children)):
        standardize(children[i])

    return tree


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


universal_varList = []


def rename(tree, new_type, variable):
    global universal_varList

    parent = tree
    children = parent.children
    parent_value = parent.get_value()

    if parent_value == variable:
        parent.set_node(new_type, variable)
        if new_type != "symbol":
            for i in range(0, len(universal_varList)):
                parent.add_child(Node("variable", universal_varList[i]))

    else:
        for i in range(len(children)):
            tree = rename(children[i], new_type, variable)

    return tree


def skolemize(tree):
    global universal_varList
    parent = tree
    parent_type = parent.get_type()
    parent_value = parent.get_value()

    if parent_type != "quant":
        universal_varList = []
        return tree

    children = parent.get_children()

    left_child = children[1]
    left_child_value = left_child.get_value()

    right_child = children[0]
    right_child_type = right_child.get_type()
    right_child_value = right_child.get_value()

    right_child_children = right_child.get_children()

    # if len(right_child_children) == 2:
    #     right_child_left = right_child_children[1]

    # right_child_right = right_child_children[0]

    if parent_value == "FORALL":
        universal_varList.append(left_child_value)
    else:
        new_type = None
        if not universal_varList:  # handles the case where there's for all before exists
            new_type = "symbol"
        else:
            new_type = "function"

        rename(tree, new_type, left_child_value)

        parent.set_node(right_child_type, right_child_value)

        if len(right_child_children) == 1:
            children.pop(1)

        for i in range(0, len(right_child_children)):
            children[i] = right_child_children[i]

        skolemize(parent)

    skolemize(children[0])

    return tree


def drop_universal(tree):
    S_type = tree.get_type()
    node = tree
    children = node.get_children()

    if len(children) != 2:
        return tree
    else:
        if S_type == "quant":
            leftNode = children[1]
            leftNodeValue = leftNode.get_value()
            universal_varList.append(leftNodeValue)

            rightNode = children[0]
            rightNodeType = rightNode.get_type()
            rightNodeValue = rightNode.get_value()

            rightChildChildren = rightNode.get_children()

            node.set_node(rightNodeType, rightNodeValue)
            if len(rightChildChildren) == 1:
                children.pop(1)

            for i in range(0, len(rightChildChildren)):
                children[i] = rightChildChildren[i]

            drop_universal(node)

        drop_universal(children[0])
        return tree


def fix_symbols(tree):
    node = tree
    if node.get_type() == "variable":
        if node.get_value() not in universal_varList:
            node.set_node("symbol", node.get_value())

    if len(node.get_children()) == 0:
        return tree

    for i in range(0, len(node.get_children())):
        fix_symbols(node.get_children()[i])

    return tree


def CNF(tree):
    parent_type = tree.get_type()
    parent_value = tree.get_value()

    children = tree.get_children()
    n_child_nodes = len(children)

    if is_cnf(tree):
        return tree

    if is_clause(tree):
        new_tree = Node("op", "AND")
        new_tree.set_children([tree])

        return new_tree

    if is_literal(tree):
        new_tree = Node("op", "AND")

        new_parent = Node("op", "OR")
        new_parent.set_children([tree])

        new_tree.set_children([new_parent])

        return new_tree

    if parent_type == "op" and parent_value == "AND" and n_child_nodes > 0:
        new_children = tree.get_children()
        for i in range(len(children)):
            child = children[i]
            x_tree = CNF(child)
            x_child_nodes = x_tree.get_children()
            for x_child_node in x_child_nodes:
                new_children.append(x_child_node)

        new_tree = Node("op", "AND")
        new_tree.set_children(new_children)

        return new_tree

    if parent_type == "op" and parent_value == "OR" and n_child_nodes > 0:
        new_children = []
        for i in range(len(children)):
            child = children[i]

            x_tree = CNF(child)

            x_child_nodes = x_tree.get_children()
            x_children = []
            for x_child_node in x_child_nodes:
                x_children.append(x_child_node)

            new_children.append(x_children)

        new_combined_children = list(itertools.product(*new_children))

        new_x_children = []
        for node_tuple in new_combined_children:
            _new_x_node = concatenate(node_tuple)
            new_x_children.append(_new_x_node)

        new_tree = Node("op", "AND")
        new_tree.set_children(new_x_children)

        return new_tree
    else:
        print("Error")


def is_cnf(tree):
    _symbol_type = tree.get_type()
    _symbol_value = tree.get_value()

    _child_nodes = tree.get_children()

    if _symbol_type == "op" and _symbol_value == "AND":

        for i in range(len(_child_nodes)):
            _child_node = _child_nodes[i]

            _child_node_symbol_type = _child_node.get_type()
            _child_node_symbol_value = _child_node.get_value()

            if not (_child_node_symbol_type == "op" and _child_node_symbol_value == "OR"):
                return False

            _child_child_nodes = _child_node.get_children()

            for i in range(len(_child_child_nodes)):
                _child_child_node = _child_child_nodes[i]

                _child_child_node_symbol_type = _child_child_node.get_type()
                _child_child_node_symbol_value = _child_child_node.get_value()

                if (_child_child_node_symbol_type == "op" and (
                        _child_child_node_symbol_value == "AND" or _child_child_node_symbol_value == "OR")):
                    return False
    else:
        return False

    return True


def is_clause(FOL_Tree):
    _symbol_type = FOL_Tree.get_type()
    _symbol_value = FOL_Tree.get_value()

    _child_nodes = FOL_Tree.get_children()

    if (_symbol_type == "op" and _symbol_value == "OR"):
        for i in range(len(_child_nodes)):
            _child_node = _child_nodes[i]

            _child_node_symbol_type = _child_node.get_type()
            _child_node_symbol_value = _child_node.get_value()

            if _child_node_symbol_type == "op" and _child_node_symbol_value == "NOT":
                continue;

            elif _child_node_symbol_type == "predicate":
                continue;

            else:
                return False

    else:
        return False

    return True


def is_literal(FOL_Tree):
    _symbol_type = FOL_Tree.get_type()
    _symbol_value = FOL_Tree.get_value()

    _child_nodes = FOL_Tree.get_children()

    if (_symbol_type == "op" and _symbol_value == "NOT"):
        _child_node = _child_nodes[0]

        _child_node_symbol_type = _child_node.get_type()
        _child_node_symbol_value = _child_node.get_value()

        if _child_node_symbol_type == "predicate":
            return True

    if _symbol_type == "predicate":
        return True

    return False


def concatenate(node_tuple):
    _new_children = []
    for node in node_tuple:
        _new_children.extend(node.get_children())

    parent = Node("op", "OR")
    parent.set_children(_new_children)
    return parent


VARIABLE = "VARIABLE"
CONSTANT = "CONSTANT"


class Argument(object):
    def __init__(self, name, kind):
        self._name = name
        self._kind = kind

    def is_variable(self):
        return self._kind == VARIABLE

    def is_constant(self):
        return self._kind == CONSTANT

    def get_name(self):
        return self._name

    def set_name(self, name):
        self._name = name

    def same_kind(self, arg):
        """
        Check if the arguments is same
        :param arg:
        :return:
        """
        return self._kind == arg._kind

    def equals(self, arg):
        """
        Checks if the arg and self are same argument
        :param arg:
        :return:
        """
        return (self.same_kind(arg) and self._name == arg._name)

    @classmethod
    def make_var(cls, name):
        return Argument(name, VARIABLE)

    @classmethod
    def make_const(cls, name):
        return Argument(name, CONSTANT)


def get_args_from_nodes(nodes):
    args = list()
    for node in nodes:
        if node.get_type() == 'function':
            symbols = node.get_children()
            arg_token = ','.join([x.get_value() for x in symbols])
            const = '{0}({1})'.format(node.get_value(), arg_token)
            args.append(Argument.make_const(const))
            continue

        if node.get_type() == 'symbol':
            val = node.get_value()
            args.append(Argument.make_const(val))
            continue

        if node.get_type() == 'variable':
            val = node.get_value()
            args.append(Argument.make_var(val))
            continue

    return args


class Predicate(object):
    """
    Represents a predicate like P(x, y) or -P(x, y)
    Order of the args and constants matters
    For a predicate P(x, a, y)
    Name: P, Args: x, a, y; x is a var, a is constant and y is a var
    """

    def __init__(self, name, args, negative=False):
        """

        :param name: string
        :param args: Argument objects
        :param negative: bool
        """
        self._name = name
        self._args = args
        self._negative = negative

    def __str__(self):
        s = "{0}({1})".format(self._name, ",".join([arg._name for arg in self._args]))
        if self._negative:
            return "-" + s

        return s

    def get_name(self):
        return self._name

    def get_args(self):
        return self._args

    def get_negative(self):
        return self._negative

    def same_formula(self, obj):
        """
        Checks whether the self and obj has the same for i.e. P(x,y)
        has same form as P(x,y) and -P(x,y), or P(y, x), or P(a, x)
        :param obj: Predicate()
        :return: bool
        """
        if self._name != obj._name:
            return False

        if len(self._args) != len(obj._args):
            return False

        return True

    def complement_of(self, obj):
        """
        Checks whether the
        :param obj: Predicate()
        :return:
        """
        return (self.same_formula(obj) and self._negative != obj._negative)

    def same_args(self, obj):
        """
        Checks if the args in self and obj are same
        :param obj: Predicate()
        :return:
        """
        for i in range(0, len(obj._args)):
            if not self._args[i].equals(obj._args[i]):
                return False

        return True

    def equals(self, obj):
        """
        Return true if both objects are P(x,y) and P(x,y)
        :param obj: Predicate()
        :return:
        """
        if not self.same_formula(obj):
            return False

        if not self.same_args(obj):
            return False

        if self._negative != obj._negative:
            return False

        return True

    def same_predicate(self, obj):

        if self._name != obj._name:
            return False

        return True

    def complement_of_predicate(self, obj):

        if self.same_predicate(obj) == True and self._negative != obj._negative:
            return True

        return False


def clausal_from_ands(and_node):
    or_list = and_node.get_children()
    clauses = list()
    for r in or_list:
        for node in r.get_children():
            # there's only one predicate here, get that
            if node.get_type() == 'op' and node.get_value() == 'NOT':
                predicate = node.get_children()[0]
                args = get_args_from_nodes(predicate.get_children())
                p = Predicate(predicate.get_value(), args, True)
                clauses.append(p)
            else:
                args = get_args_from_nodes(node.get_children())
                p = Predicate(node.get_value(), args)
                clauses.append(p)

    return clauses


def unification(p1, p2, replacements):
    """
    Takes a two predicates and tries for unifying them which are same, i.e. P(x1, y1) and -P(x1, y1)
    returns None is couldn't be done else returns the list with unification, and,
    a dict() with replacements
    :param replacements:
    :return: unifiable predicates, p1, p2 and bool if unification could be done or not
    """
    p1_args = list(p1.get_args())
    p2_args = list(p2.get_args())

    if len(p1_args) != len(p2_args):
        return p1, p2, False

    if p1.same_args(p2):  # return as it is
        return p1, p2, True

    for i in range(0, len(p1_args)):
        p1_arg = p1_args[i]
        p2_arg = p2_args[i]

        if p2_arg.equals(p1_arg):
            continue

        if p1_arg.is_variable() and p2_arg.is_variable():  # Replace p2 by p1
            token = replacements.get(p2_arg.get_name(), '')
            if token == '':
                token = p1_arg.get_name()
                replacements[p2_arg.get_name()] = token

            p1_args[i].set_name(token)
            p2_args[i].set_name(token)

            continue

        const = ''
        var = ''
        if p1_arg.is_constant() and p2_arg.is_variable():
            const = p1_arg.get_name()
            var = p2_arg.get_name()
        else:
            const = p2_arg.get_name()
            var = p1_arg.get_name()

        if '({0})'.format(const) in var:  # can't to unification
            return p1, p2, False

        replacements[var] = const
        p1_args[i].set_name(const)
        p2_args[i].set_name(const)

    p1._args = p1_args
    p2._args = p2_args

    return p1, p2, True


def addNewClause(refSet, setofSupport):
    newClause = []
    for (i, e) in enumerate(refSet):
        setofSupport.sort(key=len)
        for (j, k) in enumerate(setofSupport):
            check = False
            for (m, n) in enumerate(k):
                if e.complement_of_predicate(n) or check == True:
                    check = True
                    reps = dict()
                    p1, p2, flag = unification(e, n, reps)
                    if flag == True:
                        n = p2
                        e = p1
                    else:
                        continue
            for (a, b) in enumerate(k):
                if e.complement_of(b):
                    newClause = (setofSupport[j])
                    newClause.remove(b)
                    for (c, d) in enumerate(refSet):
                        if d == e:
                            continue
                        elif d in newClause:
                            continue
                        else:
                            newClause.append(d)
                    return newClause
                else:
                    continue

    return None


def resolution(l):
    if len(l) == 1:
        return False
    setofSupport = list(l)
    fgh = list(l)
    sizeFgh = len(fgh)
    l.sort(key=len)
    for (x, y) in enumerate(l):
        refSet = l[x]
        setofSupport.remove(refSet)
        newClause = addNewClause(refSet, setofSupport)
        if newClause == None:
            return False
        elif len(newClause) == 0:
            return True
        else:
            if newClause not in fgh:
                fgh.append(setofSupport)

    newFghSize = len(fgh)
    if newFghSize > sizeFgh:
        resolution(fgh)
    return False


def determine_if_true(statement):
    clauses = []
    for i in range(0, len(statement)):  # for all statements within a list of statement
        tree = parser(statement[i])
        tree = correct(tree)
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
        except BaseException:
            continue
    return results


statements = [["(FORALL x (EXISTS y (p x y)))", "(EXISTS x (FORALL y (NOT (p x y))))"]]  # this is inconsistent
print(parser(statements[0]))
#print(find_true_statements(statements))
