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
def first(rule):
    global rules, nonterm_userdef, \
        term_userdef, diction, firsts
    # recursion base condition
    # (for terminal or epsilon)
    if len(rule) != 0 and (rule is not None):
        if rule[0] in term_userdef:
            return rule[0]
        elif rule[0] == '#':
            return '#'

    # condition for Non-Terminals
    if len(rule) != 0:
        if rule[0] in list(diction.keys()):
            # fres temporary list of result
            fres = []
            rhs_rules = diction[rule[0]]
            # call first on each rule of RHS
            # fetched (& take union)
            for itr in rhs_rules:
                indivRes = first(itr)
                if type(indivRes) is list:
                    for i in indivRes:
                        fres.append(i)
                else:
                    fres.append(indivRes)

            # if no epsilon in result
            # - received return fres
            if '#' not in fres:
                return fres
            else:
                # apply epsilon
                # rule => f(ABC)=f(A)-{e} U f(BC)
                newList = []
                fres.remove('#')
                if len(rule) > 1:
                    ansNew = first(rule[1:])
                    if ansNew != None:
                        if type(ansNew) is list:
                            newList = fres + ansNew
                        else:
                            newList = fres + [ansNew]
                    else:
                        newList = fres
                    return newList
                # if result is not already returned
                # - control reaches here
                # lastly if eplison still persists
                # - keep it in result of first
                fres.append('#')
                return fres


# calculation of follow
# use 'rules' list, and 'diction' dict from above

# follow function input is the split result on
# - Non-Terminal whose Follow we want to compute
def follow(nt):
    global start_symbol, rules, nonterm_userdef, \
        term_userdef, diction, firsts, follows
    # for start symbol return $ (recursion base case)

    solset = set()
    if nt == start_symbol:
        solset.add('$')

    for curNT in diction:
        rhs = diction[curNT]
        for subrule in rhs:
            if nt in subrule:
                while nt in subrule:
                    index_nt = subrule.index(nt)
                    subrule = subrule[index_nt + 1:]
                    if len(subrule) != 0:
                        res = first(subrule)
                        if '#' in res:
                            newList = []
                            res.remove('#')
                            ansNew = follow(curNT)
                            if ansNew != None:
                                if type(ansNew) is list:
                                    newList = res + ansNew
                                else:
                                    newList = res + [ansNew]
                            else:
                                newList = res
                            res = newList
                    else:
                        if nt != curNT:
                            res = follow(curNT)

                    if res is not None:
                        if type(res) is list:
                            for g in res:
                                solset.add(g)
                        else:
                            solset.add(res)
    return list(solset)


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
    for y in list(diction.keys()):
        t = set()
        for sub in diction.get(y):
            res = first(sub)
            if res != None:
                if type(res) is list:
                    for u in res:
                        t.add(u)
                else:
                    t.add(res)

        # save result in 'firsts' list
        firsts[y] = t

    print("\nCalculated firsts: ")
    key_list = list(firsts.keys())
    index = 0
    for gg in firsts:
        print(f"first({key_list[index]}) "
              f"=> {firsts.get(gg)}")
        index += 1


def computeAllFollows():
    global start_symbol, rules, nonterm_userdef, \
        term_userdef, diction, firsts, follows
    for NT in diction:
        solset = set()
        sol = follow(NT)
        if sol is not None:
            for g in sol:
                solset.add(g)
        follows[NT] = solset

    print("\nCalculated follows: ")
    key_list = list(follows.keys())
    index = 0
    for gg in follows:
        print(f"follow({key_list[index]})"
              f" => {follows[gg]}")
        index += 1


# create parse table
def createParseTable():
    import copy
    global diction, firsts, follows, term_userdef
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

    # create matrix of row(NT) x [col(T) + 1($)]
    # create list of non-terminals
    ntlist = list(diction.keys())
    terminals = copy.deepcopy(term_userdef)
    terminals.append('$')

    # create the initial empty state of ,matrix
    mat = []
    for x in diction:
        row = []
        for y in terminals:
            row.append('')
        # of $ append one more col
        mat.append(row)

    # Classifying grammar as LL(1) or not LL(1)
    grammar_is_LL = True

    print('diction:', diction)
    # rules implementation
    for lhs in diction:
        print('lhs:', lhs)
        rhs = diction[lhs]
        print('rhs:', rhs)
        for y in rhs:
            res = first(y)
            # epsilon is present,
            # - take union with follow
            if '#' in res:
                if type(res) == str:
                    firstFollow = []
                    fol_op = follows[lhs]
                    if fol_op is str:
                        firstFollow.append(fol_op)
                    else:
                        for u in fol_op:
                            firstFollow.append(u)
                    res = firstFollow
                else:
                    res.remove('#')
                    res = list(res) + \
                          list(follows[lhs])
            # add rules to table
            ttemp = []
            if type(res) is str:
                ttemp.append(res)
                res = copy.deepcopy(ttemp)
            for c in res:
                print('c:', c)
                xnt = ntlist.index(lhs)
                yt = terminals.index(c)
                if mat[xnt][yt] == '':
                    mat[xnt][yt] = mat[xnt][yt] \
                                   + f"{lhs}->{' '.join(y)}"
                else:
                    # if rule already present
                    print(f"{lhs}->{y}")
                    if f"{lhs}->{y}" in mat[xnt][yt]:
                        continue
                    else:
                        grammar_is_LL = False
                        mat[xnt][yt] = mat[xnt][yt] \
                                       + f",{lhs}->{' '.join(y)}"
    for lhs in diction:
        for c in follows[lhs]:
            xnt = ntlist.index(lhs)
            yt = terminals.index(c)
            if mat[xnt][yt] == '':
                mat[xnt][yt] = 'sync'
    # final state of parse table
    print("\nGenerated parsing table:\n")
    frmt = "{:>12}" * len(terminals)
    print(frmt.format(*terminals))

    j = 0
    for y in mat:
        frmt1 = "{:>12}" * len(y)
        print(f"{ntlist[j]} {frmt1.format(*y)}")
        j += 1

    return (mat, grammar_is_LL, terminals)


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

# sample set 1 (Result: Not LL(1))
# rules=["A -> S B | B",
#        "S -> a | B c | #",
#        "B -> b | d"]
# nonterm_userdef=['A','S','B']
# term_userdef=['a','c','b','d']
# sample_input_string="b c b"

# sample set 2 (Result: LL(1))
# rules=["S -> A | B C",
#        "A -> a | b",
#        "B -> p | #",
#        "C -> c"]
# nonterm_userdef=['A','S','B','C']
# term_userdef=['a','c','b','p']
# sample_input_string="p c"

# sample set 3 (Result: LL(1))
# rules=["S -> A B | C",
#        "A -> a | b | #",
#        "B-> p | #",
#        "C -> c"]
# nonterm_userdef=['A','S','B','C']
# term_userdef=['a','c','b','p']
# sample_input_string="a c b"

# sample set 4 (Result: Not LL(1))
# rules = ["S -> A B C | C",
#          "A -> a | b B | #",
#          "B -> p | #",
#         "C -> c"]
# nonterm_userdef=['A','S','B','C']
# term_userdef=['a','c','b','p']
# sample_input_string="b p p c"

# sample set 5 (With left recursion)
# rules=["A -> B C c | g D B",
#        "B -> b C D E | #",
#        "C -> D a B | c a",
#        "D -> # | d D",
#        "E -> E a f | c"
#       ]
# nonterm_userdef=['A','B','C','D','E']
# term_userdef=["a","b","c","d","f","g"]
# sample_input_string="b a c a c"

# sample set 6
rules = ["E -> T E'",
         "E' -> + T E' | #",
         "T -> F T'",
         "T' -> * F T' | #",
         "F -> ( E ) | id"
         ]
nonterm_userdef = ['E', 'E\'', 'F', 'T', 'T\'']
term_userdef = ['id', '+', '*', '(', ')']
sample_input_string = "id * * id"
sample_input_string = "( id * id )"
sample_input_string = "( id ) * id + id"

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
    "Program -> declaration-list",
    "declaration-list -> declaration | declaration-list declaration",
    "declaration -> variable-declaration | function-declaration",
    "variable-declaration -> type-specifier id initialization",
    "initialization -> Assign expression",
    "declaration -> variable-declaration | function-declaration",
    "variable-declaration -> type-specifier id variable-declaration-tail",
    "variable-declaration-tail -> initialization | array-declaration-tail | Semicolon | Comma id variable-declaration-tail",
    "initialization -> Assign expression",
    "array-declaration-tail -> LB number RB variable-declaration-tail | LB number RB initialization variable-declaration-tail | LB number RB Semicolon",
    "type-specifier -> int | bool | char | void",
    "function-declaration -> type-specifier id LP parameter-list RP compound-statement",
    "parameter-list -> void | parameter | parameter-list Comma parameter",
    "parameter -> type-specifier id",
    "compound-statement -> LC statement-list RC",
    "statement-list -> statement | statement-list statement",
    "statement -> expression-statement | compound-statement | selection-statement | iteration-statement | return-statement | declaration-list | print-statement",
    "expression-statement -> expression Semicolon | Semicolon",
    "selection-statement -> if LP expression RP statement | if LP expression RP statement else statement",
    "iteration-statement -> while LP expression RP statement | for LP for-init-statement expression-statement expression RP statement",
    "for-init-statement -> declaration | expression-statement",
    # "expression -> String | number",
    "print-statement -> printf Lp formatted-string Comma arguments-list RP Semicolon"

<formatted-string> ::= " <string-content> "

<string-content> ::= any series of characters enclosed by double quotes

<arguments-list> ::= <variable>
                 | <arguments-list> , <variable>

<variable> ::= <identifier>
            | <constant>"
    "expression -> identifier Assign expression | simple-expression",
    "simple-expression -> additive-expression relational-operator additive-expression | additive-expression",
    "relational-operator -> ROp_E | ROp_NE | ROp_LE | ROp_L | ROp_G | ROp_GE | LOp_OR | LOp_AND"
    "additive-expression -> additive-expression additive-operator term | term",
    "additive-operator -> AOp_PL | AOp_MN",
    "term -> term multiplicative-operator factor | factor",
    "multiplicative-operator -> DV | RM | ML ",
    "factor -> LP expression RP | id | number | String",
    "number -> Decimal | Hexadecimal"
]

nonterm_userdef = ["Program", "declaration-list", "declration", "variable-declaration", "function-declaration",
                   "type-specifier", "variable-declaration-tail", "variable-declration-tail",
                   "expression", "array-declaration-tail", "initializatoin", "parameter-list", "compound-statement",
                   "number", "term", "factor", "multiplicative-operator", "for-init-statement", "simple-expression",
                   "relational-operator", "additive-expression", "additive-operator",
                   "statement-list", "statement", "expression-statement", "selection-statement", "iteration-statement"
    , "for-init-statement"]
term_userdef = ['int', 'bool', 'char', 'void', 'Assign', 'RB', 'LB', "String", "Decimal", "Hexadecimal", "id", "LC", "RC"
                ,"LP", "RP", "Semicolon", "Comma", "DV", "RM", "ML", "ROp_E", "ROp_NE", "ROp_LE", "ROp_L", "ROp_G", "ROp_GE"
                , "LOp_OR", "LOp_AND", "AOp_PL", "AOp_MN", 'if', 'for', 'break', 'continue', 'else', 'false'
                , "AOp_PL", "AOp_MN", 'print', 'return', 'true', 'while'
                ]

# # nonterm_userdef=['E','E\'','F','T','T\'']
# # term_userdef=['id','+','*','(',')']
# sample_input_string="int id Assign Decimal"

# sample set 8 (Multiple char symbols T & NT)
# rules = ["S -> NP VP",
#          "NP -> P | PN | D N",
#          "VP -> V NP",
#          "N -> championship | ball | toss",
#          "V -> is | want | won | played",
#          "P -> me | I | you",
#          "PN -> India | Australia | Steve | John",
#          "D -> the | a | an"]
#
# nonterm_userdef = ['S', 'NP', 'VP', 'N', 'V', 'P', 'PN', 'D']
# term_userdef = ["championship", "ball", "toss", "is", "want",
#                 "won", "played", "me", "I", "you", "India",
#                 "Australia","Steve", "John", "the", "a", "an"]
# sample_input_string = "India won the championship"

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

(parsing_table, result, tabTerm) = createParseTable()

# validate string input using stack-buffer concept
if sample_input_string != None:
    validity = validateStringUsingStackBuffer(parsing_table, result,
                                              tabTerm, sample_input_string,
                                              term_userdef, start_symbol)
    print(validity)
else:
    print("\nNo input String detected")
