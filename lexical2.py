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
            tokens.append(('T_Whitespace',' ',line_number))
            line_number += 1
            i += 1
            continue

        # whitespace
        elif ch.isspace():
            tokens.append(('T_Whitespace',' ',line_number))
            i += 1
            continue

        # Check for keywords or identifiers
        elif ch.isalpha() or ch == '_':
            while i < len(code) and (code[i].isalnum() or code[i]=='_'):
                current_token += code[i]
                i += 1
            if current_token in KEYWORDS:
                tokens.append(('T_'+current_token.capitalize(),current_token,line_number))
            else:
                tokens.append(('T_Id',current_token,line_number))

            current_token = ''

        # Check Hexdecimal Numbers
        elif ch=='0' and code[i+1]=='x':
            current_token+='0x'
            i=i+2
            while i<len(code) and (code[i].isdigit() or code[i] in ['A','B','C','D','E','F']):
                current_token +=code[i]
                i+=1
            tokens.append(('T_Hexadecimal',current_token,line_number))
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
                
            tokens.append(('T_Decimal',current_token,line_number))
            current_token = ''
        # Check for < or <=
        elif ch=='<':
            if code[i+1]=='=':
                tokens.append(('T_ROp_LE','<=',line_number))
                i=i+2
                continue
            tokens.append(('T_ROp_L','<',line_number))
            i+=1
        
        # Check for > or >=
        elif ch=='>':
            if code[i+1]=='=':
                tokens.append(('T_ROp_GE','>=',line_number))
                i=i+2
                continue
            tokens.append(('T_ROp_G','>',line_number))
            i+=1
        
        # Check for ! or !=
        elif ch=='!':
            if code[i+1]=='=':
                tokens.append(('T_ROp_NE','!=',line_number))
                i=i+2
                continue
            tokens.append(('T_LOp_NOT','!',line_number))
            i+=1
        
        # Chech for ||
        elif ch=='|' and code[i+1]=='|':
            tokens.append(('T_LOp_OR','||',line_number))
            i=i+2
        
        # Check for &&
        elif ch=='&' and code[i+1]=='&':
            tokens.append(('T_LOp_AND','&&',line_number))
            i=i+2

        # Check for = or ==
        elif ch=='=':
            if code[i+1]=='=':
                tokens.append(('T_ROp_E','==',line_number))
                i=i+2
                continue
            tokens.append(('T_Assign','=',line_number))
            i+=1

        # Check for (
        elif ch=='(':
            tokens.append(('T_LP','(',line_number))
            i+=1
        
        # Check for )
        elif ch==')':
            tokens.append(('T_RP',')',line_number))
            i+=1
        
        # Check for {
        elif ch=='{':
            tokens.append(('T_LC','{',line_number))
            i+=1
        
        # Check for }
        elif ch=='}':
            tokens.append(('T_RC','}',line_number))
            i+=1
        
        # Check for [
        elif ch=='[':
            tokens.append(('T_LB','[',line_number))
            i+=1
        
        # Check for ]
        elif ch==']':
            tokens.append(('T_RB',']',line_number))
            i+=1
        
        # Check for ;
        elif ch==';':
            tokens.append(('T_Semicolon',';',line_number))
            i+=1
        
        # Check for ,
        elif ch==',':
            tokens.append(('T_Comma',',',line_number))
            i+=1
        
        # Check for comments
        elif ch=='/' and code[i+1]=='/':
            current_token+=ch+code[i+1]
            i+=2
            while i<len(code) and code[i]!='\n':
                current_token+=code[i]
                i+=1
            current_token+=code[i]
            tokens.append(('T_Comments',current_token,line_number))
            i+=1
            current_token=''
        
        # Check for /
        elif ch=='/':
            tokens.append(('T_DV','/',line_number))
            i+=1

        # Check for %
        elif ch=='%':
            tokens.append(('T_RM','%',line_number))
            i+=1

        # Check for *
        elif ch=='*':
            tokens.append(('T_ML','*',line_number))
            i+=1
        
        # Check for +
        elif ch=='+':
            tokens.append(('T_AOp_PL','+',line_number))
            i+=1
        
        # Check for -
        elif ch=='-':
            tokens.append(('T_AOp_MN','-',line_number))
            i+=1
        
        # Check for Char
        elif ch=='\'' and code[i+2]=='\'':
            current_token=current_token + ch + code[i+1]+code[i+2]
            tokens.append(('T_Character',current_token,line_number))
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
            tokens.append(('T_String',current_token,line_number))
            current_token=''
            i+=1

        
        # Unknown token
        else:
            tokens.append(('T_Uknown', ch, line_number))
            i += 1

    return tokens


code='''int a=b+c;
bool a=0; //test
char a='a';
'''

tokens=lexical_analyzer(code)

for token in tokens:
    print('<',token[0],',',token[1],',',token[2],'>')