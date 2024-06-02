def removeLeftRecursion(rulesDiction):
    # for rule: A->Aa|b
    # result: A->bA',A'->aA'| e

    # new rules add
    store = {}
    # traverse over rules
    for rule in rulesDiction:
        # alphaRules stores subrules with left-recursion
        # betaRules stores subrules without left-recursion
        left_rules = []
        right_rules = []

        allrhs = rulesDiction[rule]
        for subrhs in allrhs:
            if subrhs[0] == rule:
                left_rules.append(subrhs[1:])
            else:
                right_rules.append(subrhs)

        if len(left_rules) != 0:
            # to generate new unique symbol
            # add ' till unique not generated
            lhs_ = rule + "'"
            while (lhs_ in rulesDiction.keys()) \
                    or (lhs_ in store.keys()):
                lhs_ += "'"
            # make beta rule
            for b in range(0, len(right_rules)):
                right_rules[b].append(lhs_)
            rulesDiction[rule] = right_rules
            # make alpha rule
            for a in range(0, len(left_rules)):
                left_rules[a].append(lhs_)
            left_rules.append(['#'])
            # store in temp dict, append to
            # - rulesDiction at end of traversal
            store[lhs_] = left_rules
    # add newly generated rules generated
    # - after removing left recursion
    for left in store:
        rulesDiction[left] = store[left]
    return rulesDiction


def LeftFactoring(rulesDiction):
    # for rule: A->aDF|aCV|k
    # result: A->aA'|k, A'->DF|CV

    # newDict stores newly generated
    # - rules after left factoring
    newDict = {}
    # iterate over all rules of dictionary
    for lhs in rulesDiction:
        # get rhs for given lhs
        allrhs = rulesDiction[lhs]
        # temp dictionary helps detect left factoring
        temp = dict()
        for subrhs in allrhs:
            if subrhs[0] not in list(temp.keys()):
                temp[subrhs[0]] = [subrhs]
            else:
                temp[subrhs[0]].append(subrhs)
        # if value list count for any key in temp is > 1,
        # - it has left factoring
        # new_rule stores new subrules for current LHS symbol
        new_rule = []
        # temp_dict stores new subrules for left factoring
        tempo_dict = {}
        for term_key in temp:
            # get value from temp for term_key
            allStartingWithTermKey = temp[term_key]
            if len(allStartingWithTermKey) > 1:
                # left factoring required
                # to generate new unique symbol
                # - add ' till unique not generated
                lhs_ = lhs + "'"
                while (lhs_ in rulesDiction.keys()) \
                        or (lhs_ in tempo_dict.keys()):
                    lhs_ += "'"
                # append the left factored result
                new_rule.append([term_key, lhs_])
                # add expanded rules to tempo_dict
                ex_rules = []
                for g in temp[term_key]:
                    ex_rules.append(g[1:])
                tempo_dict[lhs_] = ex_rules
            else:
                # no left factoring required
                new_rule.append(allStartingWithTermKey[0])
        # add original rule
        newDict[lhs] = new_rule
        # add newly generated rules after left factoring
        for key in tempo_dict:
            newDict[key] = tempo_dict[key]
    return newDict


# calculation of first
# epsilon is denoted by '#' (semi-colon)

# pass rule in first function
def cal_first(s):
    global rules, nonterm_userdef, \
        term_userdef, diction, firsts
    first = set()
    for i in range(len(diction[s])):
        for j in range(len(diction[s][i])):
            c = diction[s][i][j]
            if c in nonterm_userdef:
                f = cal_first(c)
                if '#' not in f:
                    for k in f:
                        first.add(k)
                    break
                else:
                    if j == len(diction[s][i])-1:
                        for k in f:
                            first.add(k)
                    else:
                        f.remove('#')
                        for k in f:
                            first.add(k)
            else:
                first.add(c)
                break
    return first
    # recursion base condition
    # (for terminal or epsilon)
    # if rule[0] in term_userdef:
    #     return rule[0]
    # elif rule[0] == '#':
    #     return '#'
    #
    # # condition for Non-Terminals
    # if len(rule) != 0:
    #     if rule[0] in list(diction.keys()):
    #         # fres temporary list of result
    #         fres = []
    #         rhs_rules = diction[rule[0]]
    #         # call first on each rule of RHS
    #         # fetched (& take union)
    #         indivRes = first(rhs_rules)
    #         if type(indivRes) is list:
    #             for i in indivRes:
    #                 fres.append(i)
    #         else:
    #             fres.append(indivRes)
    #
    #         # if no epsilon in result
    #         # - received return fres
    #         if '#' not in fres:
    #             return fres
    #         else:
    #             # apply epsilon
    #             # rule => f(ABC)=f(A)-{e} U f(BC)
    #             newList = []
    #             fres.remove('#')
    #             if len(rule) > 1:
    #                 ansNew = first(rule[1:])
    #                 if ansNew != None:
    #                     if type(ansNew) is list:
    #                         newList = fres + ansNew
    #                     else:
    #                         newList = fres + [ansNew]
    #                 else:
    #                     newList = fres
    #                 return newList
    #             # if result is not already returned
    #             # - control reaches here
    #             # lastly if eplison still persists
    #             # - keep it in result of first
    #             fres.append('#')
    #             return fres


# calculation of follow
# use 'rules' list, and 'diction' dict from above

# follow function input is the split result on
# - Non-Terminal whose Follow we want to compute
def cal_follow(s):
    global start_symbol, rules, nonterm_userdef, \
        term_userdef, diction, firsts, follows
    # for start symbol return $ (recursion base case)
    follow = set()
    # if len(s) != 1:
    #     return {}
    if s == list(diction.keys())[0]:
        follow.add('$')

    for i in diction:
        for j in range(len(diction[i])):
            if s in diction[i][j]:
                idx = diction[i][j].index(s)

                if idx == len(diction[i][j]) - 1:
                    if diction[i][j][idx] == i:
                        break
                    else:
                        f = cal_follow(i)
                        for x in f:
                            follow.add(x)
                else:
                    while idx != len(diction[i][j]) - 1:
                        idx += 1
                        if diction[i][j][idx] in term_userdef:
                            follow.add(diction[i][j][idx])
                            break
                        else:
                            f = firsts[diction[i][j][idx]]

                            if '#' not in f:
                                for x in f:
                                    follow.add(x)
                                break
                            elif '#' in f and idx != len(diction[i][j]) - 1:
                                f.remove('#')
                                for k in f:
                                    follow.add(k)

                            elif '#' in f and idx == len(diction[i][j]) - 1:
                                f.remove('#')
                                for k in f:
                                    follow.add(k)

                                f = cal_follow(i)
                                for x in f:
                                    follow.add(x)
    return follow
    # solset = set()
    # if nt == start_symbol:
    #     solset.add('$')
    #
    # for curNT in diction:
    #     rhs = diction[curNT]
    #     for subrule in rhs:
    #         if nt in subrule:
    #             while nt in subrule:
    #                 index_nt = subrule.index(nt)
    #                 subrule = subrule[index_nt + 1:]
    #                 if len(subrule) != 0:
    #                     res = cal_first(subrule)
    #                     if '#' in res:
    #                         newList = []
    #                         res.remove('#')
    #                         ansNew = follow(curNT)
    #                         if ansNew != None:
    #                             if type(ansNew) is list:
    #                                 newList = res + ansNew
    #                             else:
    #                                 newList = res + [ansNew]
    #                         else:
    #                             newList = res
    #                         res = newList
    #                 else:
    #                     if nt != curNT:
    #                         res = follow(curNT)
    #
    #                 if res is not None:
    #                     if type(res) is list:
    #                         for g in res:
    #                             solset.add(g)
    #                     else:
    #                         solset.add(res)
    # return list(solset)


def computeAllFirsts():
    global rules, nonterm_userdef, \
        term_userdef, diction, firsts
    for rule in rules:
        k = rule.split("->")
        # remove un-necessary spaces
        k[0] = k[0].strip()
        k[1] = k[1].strip()
        rhs = k[1]
        multirhs = rhs.split('|')
        # remove un-necessary spaces
        for i in range(len(multirhs)):
            multirhs[i] = multirhs[i].strip()
            multirhs[i] = multirhs[i].split()
        diction[k[0]] = multirhs
    print(f"\nRules: \n")

    for y in diction:
        print(f"{y}->{diction[y]}")
    print(f"\nAfter elimination of left recursion:\n")

    diction = removeLeftRecursion(diction)
    for y in diction:
        print(f"{y}->{diction[y]}")
    print("\nAfter left factoring:\n")

    diction = LeftFactoring(diction)
    for y in diction:
        print(f"{y}->{diction[y]}")

    # calculate first for each rule
    # - (call first() on all RHS)
    # print(diction['statement-list'][0][0])
    # print(diction['statement-list'][0])
    for s in list(diction.keys()):
        firsts[s] = cal_first(s)

    # firsts['statement-list'] = cal_first('statement-list')
        # t = set()
        # for sub in diction.get(y):
        #     res = first(sub)
        #     if res != None:
        #         if type(res) is list:
        #             for u in res:
        #                 t.add(u)
        #         else:
        #             t.add(res)
        #
        # # save result in 'firsts' list
        # firsts[y] = t

    print("\nCalculated firsts: ")
    key_list = list(firsts.keys())
    index = 0
    for gg in firsts:
        print(f"first({key_list[index]}) "
              f"=> {firsts.get(gg)}")
        index += 1
    print("--end firsts--")


def computeAllFollows():
    global start_symbol, rules, nonterm_userdef, \
        term_userdef, diction, firsts, follows

    # follows['selection-statement'] = cal_follow('selection-statement')
    # follows['iteration-statement'] = cal_follow('iteration-statement')
    # follows['variable-declaration-tail'] = cal_follow('variable-declaration-tail')
    for s in diction.keys():
        follows[s] = cal_follow(s)
    # for NT in diction:
    #     solset = set()
    #     sol = follow(NT)
    #     if sol is not None:
    #         for g in sol:
    #             solset.add(g)
    #     follows[NT] = solset

    print("\nCalculated follows: ")
    key_list = list(follows.keys())
    index = 0
    for gg in follows:
        print(f"follow({key_list[index]})"
              f" => {follows[gg]}")
        index += 1


# get_rule
def get_rule(non_terminal, terminal):
    global diction, firsts, nonterm_userdef
    for rhs in diction[non_terminal]:
        if rhs[0] == terminal:
            return rhs

        elif rhs[0] in nonterm_userdef and terminal in firsts[rhs[0]]:
            return rhs
        else:
            return ''


def generate_parse_table():
    global term_userdef, diction, firsts, follows
    non_terminals = list(diction.keys())
    parse_table = [[""] * len(term_userdef) for i in range(len(non_terminals))]

    print("\nFirsts and Follow Result table\n")

    # find space size
    mx_len_first = 0
    mx_len_fol = 0
    for u in diction:
        k1 = len(str(firsts[u]))
        k2 = len(str(follows[u]))
        if k1 > mx_len_first:
            mx_len_first = k1
        if k2 > mx_len_fol:
            mx_len_fol = k2

    print(f"{{:<{10}}} "
          f"{{:<{mx_len_first + 5}}} "
          f"{{:<{mx_len_fol + 5}}}"
          .format("Non-T", "FIRST", "FOLLOW"))
    for u in diction:
        print(f"{{:<{10}}} "
              f"{{:<{mx_len_first + 5}}} "
              f"{{:<{mx_len_fol + 5}}}"
              .format(u, str(firsts[u]), str(follows[u])))

    for non_terminal in non_terminals:
        for terminal in term_userdef:
            # print("non:",non_terminal)
            # print("term:",terminal)
            # print(terminal)
            # print(grammar_first[non_terminal])
            if terminal in firsts[non_terminal]:
                rule = get_rule(non_terminal, terminal)
                # print(rule)

            elif '#' in firsts[non_terminal] and terminal in follows[non_terminal]:
                rule = '#'

            elif terminal in follows[non_terminal]:
                rule = "Sync"

            else:
                rule = ""

            parse_table[non_terminals.index(non_terminal)][term_userdef.index(terminal)] = rule

    return parse_table


def display_parse_table(parse_table):
    global term_userdef, diction
    non_terminals = list(diction.keys())
    print("\t\t\t\t", end="")
    for terminal in term_userdef:
        print(terminal + "\t\t", end="")
    print("\n\n")
    print(parse_table)

    for non_terminal in non_terminals:
        print("\t\t" + non_terminal + "\t\t", end="")
        for terminal in term_userdef:
            print(str(parse_table[non_terminals.index(non_terminal)][term_userdef.index(terminal)]) + "\t\t", end="")
        print("\n")


# create parse table
# def createParseTable():
#     import copy
#     global diction, firsts, follows, term_userdef
#     print("\nFirsts and Follow Result table\n")
#
#     # find space size
#     mx_len_first = 0
#     mx_len_fol = 0
#     for u in diction:
#         k1 = len(str(firsts[u]))
#         k2 = len(str(follows[u]))
#         if k1 > mx_len_first:
#             mx_len_first = k1
#         if k2 > mx_len_fol:
#             mx_len_fol = k2
#
#     print(f"{{:<{10}}} "
#           f"{{:<{mx_len_first + 5}}} "
#           f"{{:<{mx_len_fol + 5}}}"
#           .format("Non-T", "FIRST", "FOLLOW"))
#     for u in diction:
#         print(f"{{:<{10}}} "
#               f"{{:<{mx_len_first + 5}}} "
#               f"{{:<{mx_len_fol + 5}}}"
#               .format(u, str(firsts[u]), str(follows[u])))
#
#     # create matrix of row(NT) x [col(T) + 1($)]
#     # create list of non-terminals
#     ntlist = list(diction.keys())
#     terminals = copy.deepcopy(term_userdef)
#     terminals.append('$')
#
#     # create the initial empty state of ,matrix
#     mat = []
#     for x in diction:
#         row = []
#         for y in terminals:
#             row.append('')
#         # of $ append one more col
#         mat.append(row)
#
#     # Classifying grammar as LL(1) or not LL(1)
#     grammar_is_LL = True
#
#     # print('diction:', diction)
#     # rules implementation
#     for lhs in diction:
#         print('lhs:', lhs)
#         rhs = diction[lhs]
#         print('rhs:', rhs)
#         for y in rhs:
#             res = firsts[y[0]]
#             print(res)
#             # epsilon is present,
#             # - take union with follow
#             if '#' in res:
#                 if type(res) == str:
#                     firstFollow = []
#                     fol_op = follows[lhs]
#                     if fol_op is str:
#                         firstFollow.append(fol_op)
#                     else:
#                         for u in fol_op:
#                             firstFollow.append(u)
#                     res = firstFollow
#                 else:
#                     res.remove('#')
#                     res = list(res) + \
#                           list(follows[lhs])
#             # add rules to table
#             ttemp = []
#             if type(res) is str:
#                 ttemp.append(res)
#                 res = copy.deepcopy(ttemp)
#             for c in res:
#                 # print('c:', c)
#                 xnt = ntlist.index(lhs)
#                 yt = terminals.index(c)
#                 if mat[xnt][yt] == '':
#                     mat[xnt][yt] = mat[xnt][yt] \
#                                    + f"{lhs}->{' '.join(y)}"
#                 else:
#                     # if rule already present
#                     print(f"{lhs}->{y}")
#                     if f"{lhs}->{y}" in mat[xnt][yt]:
#                         continue
#                     else:
#                         grammar_is_LL = False
#                         mat[xnt][yt] = mat[xnt][yt] \
#                                        + f",{lhs}->{' '.join(y)}"
#     for lhs in diction:
#         for c in follows[lhs]:
#             xnt = ntlist.index(lhs)
#             yt = terminals.index(c)
#             if mat[xnt][yt] == '':
#                 mat[xnt][yt] = 'sync'
#     # final state of parse table
#     print("\nGenerated parsing table:\n")
#     frmt = "{:>12}" * len(terminals)
#     print(frmt.format(*terminals))
#
#     j = 0
#     for y in mat:
#         frmt1 = "{:>12}" * len(y)
#         print(f"{ntlist[j]} {frmt1.format(*y)}")
#         j += 1
#
#     return (mat, grammar_is_LL, terminals)


def validateStringUsingStackBuffer(parsing_table, grammarll1,
                                   table_term_list, input_string,
                                   term_userdef, start_symbol):
    print(f"\nValidate String => {input_string}\n")

    # for more than one entries
    # - in one cell of parsing table
    if grammarll1 == False:
        return f"\nInput String = " \
               f"\"{input_string}\"\n" \
               f"Grammar is not LL(1)"

    # implementing stack buffer

    stack = [start_symbol, '$']
    buffer = []

    # reverse input string store in buffer
    input_string = input_string.split()
    input_string.reverse()
    buffer = ['$'] + input_string

    print("{:>20} {:>20} {:>20}".
          format("Buffer", "Stack", "Action"))

    while True:
        # end loop if all symbols matched
        if stack == ['$'] and buffer == ['$']:
            print("{:>20} {:>20} {:>20}"
                  .format(' '.join(buffer),
                          ' '.join(stack),
                          "Valid"))
            return "\nValid String!"
        elif stack[0] not in term_userdef:
            # take font of buffer (y) and tos (x)
            x = list(diction.keys()).index(stack[0])
            y = table_term_list.index(buffer[-1])
            if parsing_table[x][y] != '':
                # format table entry received
                entry = parsing_table[x][y]
                print("{:>20} {:>20} {:>25}".
                      format(' '.join(buffer),
                             ' '.join(stack),
                             f"T[{stack[0]}][{buffer[-1]}] = {entry}"))
                lhs_rhs = entry.split("->")
                lhs_rhs[1] = lhs_rhs[1].replace('#', '').strip()
                entryrhs = lhs_rhs[1].split()
                stack = entryrhs + stack[1:]
            else:
                return f"\nInvalid String! No rule at " \
                       f"Table[{stack[0]}][{buffer[-1]}]."
        else:
            # stack top is Terminal
            if stack[0] == buffer[-1]:
                print("{:>20} {:>20} {:>20}"
                      .format(' '.join(buffer),
                              ' '.join(stack),
                              f"Matched:{stack[0]}"))
                buffer = buffer[:-1]
                stack = stack[1:]
            else:
                return "\nInvalid String! " \
                       "Unmatched terminal symbols"


sample_input_string = None

# sample set 6
# rules = ["E -> T E'",
#          "E' -> + T E' | #",
#          "T -> F T'",
#          "T' -> * F T' | #",
#          "F -> ( E ) | id"
#          ]
# nonterm_userdef = ['E', 'E\'', 'F', 'T', 'T\'']
# term_userdef = ['id', '+', '*', '(', ')']
# sample_input_string = "id * * id"
# sample_input_string = "( id * id )"
# sample_input_string = "( id ) * id + id"

# sample set 7 (left factoring & recursion present)
# rules=["S -> A k O",
#        "A -> A d | a B | a C",
#        "C -> c",
#        "B -> b B C | r"]
# rules=["E -> T E'",
#         "E' -> + T E' | #",
#         "T -> F T'",
#         "T' -> * F T' | #",
#         "F -> ( E ) | id"
# ]

rules = [
    "Program -> declaration-list | #",
    "declaration-list -> declaration declaration-list'",
    "declaration-list' -> declaration declaration-list' | #",
    "declaration -> variable-declaration | function-declaration",
    "variable-declaration -> type-specifier id variable-declaration-tail",
    "variable-declaration-tail -> initialization | LB number RB variable-declaration-tail | Semicolon | Comma id variable-declaration-tail",
    "initialization -> Assign expression",
    # "array-declaration-tail -> LB number RB variable-declaration-tail",
    "type-specifier -> int | bool | char | void",
    "function-declaration -> type-specifier id LP parameter-list RP statement-list",
    "parameter-list -> void | parameter Comma parameter-list | #",
    "parameter -> type-specifier id",
    # "compound-statement -> LC declaration-list statement-list RC",
    "statement-list -> statement statement-list | #",
    "statement -> expression-statement | selection-statement | iteration-statement | return-statement | declaration-list | print-statement",
    "expression-statement -> expression Semicolon | Semicolon",
    "selection-statement -> if LP expression RP LC statement RC | if LP expression RP statement else LC statement RC",
    "iteration-statement -> while LP expression RP LC statement RC | for LP expression-statement expression-statement expression RP LC statement RC",
    # "for-init-statement -> declaration | expression-statement",
    # "expression -> String | number",
    "print-statement -> printf Lp String Comma arguments-list RP Semicolon",
    "return-statement -> return expression",
    "arguments-list -> variable | arguments-list Comma variable",
    "variable -> id | number",
    "expression -> id Assign expression | simple-expression",
    "simple-expression -> additive-expression relational-operator additive-expression | additive-expression",
    "relational-operator -> ROp_E | ROp_NE | ROp_LE | ROp_L | ROp_G | ROp_GE | LOp_OR | LOp_AND",
    "additive-expression -> additive-expression additive-operator term | term",
    "additive-operator -> AOp_PL | AOp_MN",
    "term -> term multiplicative-operator factor | factor",
    "multiplicative-operator -> DV | RM | ML ",
    "factor -> LP expression RP | id | number | String",
    "number -> Decimal | Hexadecimal"
]

nonterm_userdef = ["Program", "declaration-list", "declaration", "variable-declaration", "function-declaration",
                   "type-specifier", "variable-declaration-tail", "variable-declaration-tail",
                   "expression", "initialization", "parameter-list", "number", "term", "factor",
                   "multiplicative-operator", "simple-expression", "relational-operator", "additive-expression",
                   "additive-operator", "statement-list", "statement", "expression-statement", "selection-statement",
                   "iteration-statement", "variable", "print-statement", "arguments-list", "declaration-list'"]
term_userdef = ['int', 'bool', 'char', 'void', 'Assign', 'RB', 'LB', "String", "Decimal", "Hexadecimal", "id", "LC", "RC"
                , "LP", "RP", "Semicolon", "Comma", "DV", "RM", "ML", "ROp_E", "ROp_NE", "ROp_LE", "ROp_L", "ROp_G", "ROp_GE"
                , "LOp_OR", "LOp_AND", "AOp_PL", "AOp_MN", 'if', 'for', 'break', 'continue', 'else', 'false'
                , "AOp_PL", "AOp_MN", 'printf', 'return', 'true', 'while'
            ]

# # nonterm_userdef=['E','E\'','F','T','T\'']
# # term_userdef=['id','+','*','(',')']
sample_input_string = "int id Assign Decimal"


# diction - store rules inputted
# firsts - store computed firsts
diction = {}
firsts = {}
follows = {}

# computes all FIRSTs for all non terminals
computeAllFirsts()
# assuming first rule has start_symbol
# start symbol can be modified in below line of code
start_symbol = list(diction.keys())[0]
# computes all FOLLOWs for all occurrences
computeAllFollows()
# generate formatted first and follow table
# then generate parse table

# (parsing_table, result, tabTerm) = createParseTable()
parse_table = generate_parse_table()
display_parse_table(parse_table)
# validate string input using stack-buffer concept
# if sample_input_string != None:
#     validity = validateStringUsingStackBuffer(parsing_table, result,
#                                               tabTerm, sample_input_string,
#                                               term_userdef, start_symbol)
#     print(validity)
# else:
#     print("\nNo input String detected")
