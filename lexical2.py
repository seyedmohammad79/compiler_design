import string

# Token types
TOKEN_KEYWORD = 'KEYWORD'
TOKEN_IDENTIFIER = 'IDENTIFIER'
TOKEN_INTEGER_CONSTANT = 'INTEGER_CONSTANT'
TOKEN_OPERATOR = 'OPERATOR'
TOKEN_DELIMITER = 'DELIMITER'
TOKEN_UNKNOWN = 'UNKNOWN'

# Keywords
KEYWORDS = [
    'bool','break','char','continue','else','false',
    'for','if','int','print','return','true'
]

# Punctuation_marks
PUNCTUATION = [
    '{' , '}' , '(' , ')' , '[' , ']' , ',' , ';'
]

# Comments
COMMENT = '//'

# Operators
OPERATORS = [
    '+', '-', '*', '/', '%', '>', '>=', '<', '<=', '==', '!=', '&&', '||', '!', '=', '**'  #add a pow
]

# Delimiters
DELIMITERS = [
    ' ','\n'
]

def lexical_analyzer(code :str):
    tokens = []
    current_token = ''
    i=0
    line_number = 1
    while i < len(code):
        ch :str= code[i]
        # Check for new lines
        if ch == '\n':
            tokens.append(('Whitespace',' ',line_number))
            line_number += 1
            i += 1
            continue

        # whitespace
        elif ch.isspace():
            tokens.append(('Whitespace',' ',line_number))
            i += 1
            continue

        # Check for keywords or identifiers
        elif ch.isalpha() or ch == '_':
            while i < len(code) and (code[i].isalnum() or code[i]=='_'):
                current_token += code[i]
                i += 1
            if current_token in KEYWORDS:
                tokens.append((current_token.capitalize(),current_token,line_number))
            else:
                tokens.append(('Id',current_token,line_number))

            current_token = ''

        # Check Hexdecimal Numbers
        elif ch=='0' and code[i+1]=='x':
            current_token+='0x'
            i=i+2
            while i<len(code) and (code[i].isdigit() or code[i] in ['A','B','C','D','E','F']):
                current_token +=code[i]
                i+=1
            tokens.append(('Hexadecimal',current_token,line_number))
            current_token = ''
            
        # Check Decimal Numbers
        elif ch.isdigit():
            while i < len(code) and code[i].isdigit():
                current_token += code[i]
                i += 1
            if code[i]=='.':
                current_token += code[i]
                i+=1
                while i< len(code) and code[i].isdigit():
                    current_token +=code[i]
                    i +=1
            if code[i]=='E':
                current_token +=code[i]
                i+=1
                if code[i] in ['+','-']:
                    current_token +=code[i]
                    i+=1
                while i<len(code) and code[i].isdigit():
                    current_token +=code[i]
                    i+=1
                
            tokens.append(('DEcimal',current_token,line_number))
            current_token = ''
        # Check for < or <=
        elif ch=='<':
            if code[i+1]=='=':
                tokens.append(('Rop_LE','<=',line_number))
                i=i+2
                continue
            tokens.append(('ROp_L','<',line_number))
            i+=1
        
        # Check for > or >=
        elif ch=='>':
            if code[i+1]=='=':
                tokens.append(('Rop_GE','>=',line_number))
                i=i+2
                continue
            tokens.append(('ROp_G','>',line_number))
            i+=1
        
        # Check for ! or !=
        elif ch=='!':
            if code[i+1]=='=':
                tokens.append(('ROp_NE','!=',line_number))
                i=i+2
                continue
            tokens.append(('LOp_NOT','!',line_number))
            i+=1
        
        # Chech for ||
        elif ch=='|' and code[i+1]=='|':
            tokens.append(('LOp_OR','||',line_number))
            i=i+2
        
        # Check for &&
        elif ch=='&' and code[i+1]=='&':
            tokens.append(('LOp_AND','&&',line_number))
            i=i+2

        # Check for = or ==
        elif ch=='=':
            if code[i+1]=='=':
                tokens.append(('ROp_E','==',line_number))
                i=i+2
                continue
            tokens.append(('Assign','=',line_number))
            i+=1

        # Check for (
        elif ch=='(':
            tokens.append(('LP','(',line_number))
            i+=1
        
        # Check for )
        elif ch==')':
            tokens.append(('RP',')',line_number))
            i+=1
        
        # Check for {
        elif ch=='{':
            tokens.append(('LC','{',line_number))
            i+=1
        
        # Check for }
        elif ch=='}':
            tokens.append(('RC','}',line_number))
            i+=1
        
        # Check for [
        elif ch=='[':
            tokens.append(('LB','[',line_number))
            i+=1
        
        # Check for ]
        elif ch==']':
            tokens.append(('RB',']',line_number))
            i+=1
        
        # Check for ;
        elif ch==';':
            tokens.append(('Semicolon',';',line_number))
            i+=1
        
        # Check for ,
        elif ch==',':
            tokens.append(('Comma',',',line_number))
            i+=1
        
        # Check for comments
        elif ch=='/' and code[i+1]=='/':
            current_token+=ch+code[i+1]
            i+=2
            while i<len(code) and code[i]!='\n':
                current_token+=code[i]
                i+=1
            current_token+=code[i]
            tokens.append(('Comments',current_token,line_number))
            i+=1
            current_token=''
        
        # Check for /
        elif ch=='/':
            tokens.append(('DV','/',line_number))
            i+=1

        # Check for %
        elif ch=='%':
            tokens.append(('RM','%',line_number))
            i+=1

        # Check for *
        elif ch=='*':
            tokens.append(('ML','*',line_number))
            i+=1
        
        # Check for +
        elif ch=='+':
            tokens.append(('AOp_PL','+',line_number))
            i+=1
        
        # Check for -
        elif ch=='-':
            tokens.append(('AOp_MN','-',line_number))
            i+=1
        
        # Check for Char
        elif ch=='\'' and code[i+2]=='\'':
            current_token=current_token + ch + code[i+1]+code[i+2]
            tokens.append(('Char',current_token,line_number))
            i=i+3
            current_token=''            
        
        # Check for string
        elif ch=='\"':
            current_token+=ch
            i+=1
            while i<len(code) and code[i]!='\"':
                current_token+=code[i]
                i+=1
            current_token+=code[i]
            tokens.append(('String',current_token,line_number))
            current_token=''
            i+=1

        
        # Unknown token
        else:
            tokens.append(('Uknown', ch, line_number))
            i += 1

    return tokens


code='''int a=b+c;
bool a=0; //test
'''

tokens=lexical_analyzer(code)

for token in tokens:
    print('<',token[0],',',token[1],',',token[2],'>')