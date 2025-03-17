#Uni.:   VUT FIT
#Name:   First part of a project to subject IPP - parser for IPPcode24
#Author: Halva Jindřich
#login:	 xhalva05
#Date:   13/2/2024

import sys
import re

#FUNCTIONS_____________________________________________________________________________

def operands_num_check(num):
    if(len(line.split('#')[0].split()) != (num+1)):
        print('ERROR(23) - Error in lexical or syntax analysis of source code in IPPcode24', file=sys.stderr)
        sys.exit(23)


def check_var(variable):
    parts_list = variable.split("@")
    #only one "@"
    if(len(parts_list) != 2):
        print('ERROR(23) - Error in lexical or syntax analysis of source code in IPPcode24', file=sys.stderr)
        sys.exit(23)
    #frame name 
    if((parts_list[0] != "GF") & (parts_list[0] != "TF") & (parts_list[0] != "LF")):
        print('ERROR(23) - Error in lexical or syntax analysis of source code in IPPcode24', file=sys.stderr)
        sys.exit(23)
    firstchar = True
    #only alfanumerical characters or some special chars...
    for char in parts_list[1]:
        char_ascii = ord(char)
        if(((char_ascii >= ord("a")) & (char_ascii <= ord("z"))) | ((char_ascii >= ord("A")) & (char_ascii <= ord("Z"))) | ((char_ascii >= ord("0")) & (char_ascii <= ord("9"))) | (char == "_") | (char == "-") | (char == "$") | (char == "&") | (char == "%") | (char == "*") | (char == "!") | (char == "?")):
            #first character cant start with number
            if(firstchar):
                if((char_ascii >= ord("0")) & (char_ascii <= ord("9"))):
                    print('ERROR(23) - Error in lexical or syntax analysis of source code in IPPcode24', file=sys.stderr)
                    sys.exit(23)
            firstchar = False
        else:
            print('ERROR(23) - Error in lexical or syntax analysis of source code in IPPcode24', file=sys.stderr)
            sys.exit(23)

def check_symb(symbol):
    parts_list = symbol.split("@")
    if(len(parts_list) != 2):
        #in string symbols, more "@" are allowed, it can be part of a string
        if((len(parts_list) > 2) & (parts_list[0] == "string" )):
            pass
        else:
            print('ERROR(23) - Error in lexical or syntax analysis of source code in IPPcode24', file=sys.stderr)
            sys.exit(23)
    if((parts_list[0] != "GF") & (parts_list[0] != "TF") & (parts_list[0] != "LF")):
        #constant or non-available symbol:
        if((parts_list[0] == "bool") & ((parts_list[1] == "true") | (parts_list[1] == "false"))):
            return
        if((parts_list[0] == "nil") & (parts_list[1] == "nil")):
            return    
        if(parts_list[0] == "int"):
            #regex for integers: decimal/octal/hexadeciaml
            pattern = r'[+-]*\d+|[+-]*0[xX][a-fA-F0-9]+|[+-]*0[oO][0-7]+'
            p = re.fullmatch(pattern, parts_list[1])
            if(p):
                return
        if(parts_list[0] == "string"):
            if((len(symbol.split()) != 1) | (len(symbol.split("#")) != 1)):
                print('ERROR(23) - Error in lexical or syntax analysis of source code in IPPcode24', file=sys.stderr)
                sys.exit(23)
            parts_list.remove("string")
            sep = ''
            #empty string "string@"
            if((len(parts_list) == 1) & (parts_list[0] == '')):
                return
            #only letters/numbers or special escape sequencies in new_joined_parts
            new_joined_parts = sep.join(parts_list)
            #regex for symbols: alfanumerical symbols, except '#' and '\' ... /xyz sequencies are allowed, x,y,z are from interval<0,9>
            pattern = r'(?:[^#\\]+|\\[0-9][0-9][0-9])+'
            p = re.fullmatch(pattern, new_joined_parts)
            if(p):
                return
        print('ERROR(23) - Error in lexical or syntax analysis of source code in IPPcode24', file=sys.stderr)
        sys.exit(23)
    else:   #symbol should be a variable
        check_var(symbol)


def check_label(label):
    firstchar = True
    #only alfanumerical characters or some special chars...
    for char in label:
        char_ascii = ord(char)
        if(((char_ascii >= ord("a")) & (char_ascii <= ord("z"))) | ((char_ascii >= ord("A")) & (char_ascii <= ord("Z"))) | ((char_ascii >= ord("0")) & (char_ascii <= ord("9"))) | (char == "_") | (char == "-") | (char == "$") | (char == "&") | (char == "%") | (char == "*") | (char == "!") | (char == "?")):
        	#first character cant start with number
            if(firstchar):
                if((char_ascii >= ord("0")) & (char_ascii <= ord("9"))):
                    print('ERROR(23) - Error in lexical or syntax analysis of source code in IPPcode24', file=sys.stderr)
                    sys.exit(23)
            firstchar = False
        else:
            print('ERROR(23) - Error in lexical or syntax analysis of source code in IPPcode24', file=sys.stderr)
            sys.exit(23)


def check_type(type):
    #only these 3 options for <type>
    if ((type != "int") & (type != "string") & (type != "bool")):
            print('ERROR(23) - Error in lexical or syntax analysis of source code in IPPcode24', file=sys.stderr)
            sys.exit(23)


def generate_xml(program):
    xml = []
    #header
    xml.append('<?xml version="1.0" encoding="UTF-8"?>')
    xml.append('<program language="IPPcode24">')

    ins_count = 1
    #iterate through all instructions(opcodes with args) in program
    for instruction in program:
    	
    	#example:
    	#instruction on input: READ GF@var int
    	#element in program list:
    	#{"opcode": READ, "arg1": {"type": "var", "value": GF@var}, "arg2": {"type": "type", "value": int}}
    	
        instruction_elem = f'  <instruction order="{ins_count}" opcode="{instruction["opcode"]}">'
        #maximum amount of arguments is three... (arg1, arg2, arg3)
        for i in range(1, 4):
            arg_key = f"arg{i}"
            if arg_key in instruction:
                arg_elem = f'    <{arg_key} type="{instruction[arg_key]["type"]}">{replace_chars(instruction[arg_key]["value"])}</{arg_key}>'
                #connection of the raw intruction code in xml with its arguments, divided with new_line
                instruction_elem = instruction_elem + "\n" + arg_elem
        #instruction ends
        instruction_elem += "\n  </instruction>"
        #insert instruction to the xml list
        xml.append(instruction_elem)
        #inkrement instruction counter
        ins_count += 1

	#end of program
    xml.append('</program>')
    return xml

#function that converts characters that are not allowed in xml text to the allowed ones
def replace_chars(string):
    return string.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


#ARGUMENTS_HANDLING______________________________________________________________________

arg_list = sys.argv

if(len(arg_list) > 1):
    if((len(arg_list) == 2) & (arg_list[1] == "--help")):
        print('PROGRAM USAGE:\nExecution format: python3.10 parse.py < input_file')
        sys.exit(0)
    else:
        print('ERROR(10) - Missing parameters or wrong parameters used', file=sys.stderr)
        sys.exit(10)

#MAIN_PART_______________________________________________________________________________

program = []
header_found = False 

for line in sys.stdin:
    #Comment lines or empty lines in the input file will be skipped
    if((line[0] == '#') or (len(line.strip()) == 0)):
        continue
    line = line.rstrip()
    #Searching for header
    if(header_found == False):
        if (line.split('#')[0].lower().strip() != ".ippcode24"):
            print('ERROR(21) - Missing Header in input File', file=sys.stderr)
            sys.exit(21)
        header_found = True
        continue

    #keeps inctruction name and its operands in list
    instruction_list = line.split('#')[0].split()
    #keeps instruction name in uppercase chars (opcode)
    first = instruction_list[0].upper()

    match first:
    	#no arguments... easy
        case "CREATEFRAME" | "PUSHFRAME" | "POPFRAME" | "BREAK" | "RETURN":
            operands_num_check(0)
            program.append({"opcode": first})

        # <var>
        case "DEFVAR" | "POPS":
            operands_num_check(1)
            check_var(instruction_list[1])
            program.append({
                "opcode": first, 
                "arg1": {"type": "var", "value": instruction_list[1]}})
            
        # <symb>
        case "EXIT" | "DPRINT" | "WRITE" | "PUSHS":
            operands_num_check(1)
            check_symb(instruction_list[1])
            if((instruction_list[1].split("@")[0] == "LF")|(instruction_list[1].split("@")[0] == "GF")|(instruction_list[1].split("@")[0] == "TF")):
                type_ = "var"
                value_ = instruction_list[1]
            else:
                type_ = instruction_list[1].split("@")[0] 
                if(instruction_list[1].split("@")[0] == "string"):
                    value_ = instruction_list[1].removeprefix("string@")
                else:
                    value_ = instruction_list[1].split("@")[1]  
            program.append({
                "opcode": first, 
                "arg1": {"type": type_, "value": value_}})
            
        # <label>
        case "CALL" | "LABEL" | "JUMP":
            operands_num_check(1)
            check_label(instruction_list[1])
            program.append({
                "opcode": first, 
                "arg1": {"type": "label", "value": instruction_list[1]}})

        # <var> <symb>
        case "MOVE" | "INT2CHAR" | "STRLEN" | "TYPE" | "NOT":
            operands_num_check(2)
            check_var(instruction_list[1])
            check_symb(instruction_list[2])
            if((instruction_list[2].split("@")[0] == "LF")|(instruction_list[2].split("@")[0] == "GF")|(instruction_list[2].split("@")[0] == "TF")):
                type_ = "var"
                value_ = instruction_list[2]
            else:
                type_ = instruction_list[2].split("@")[0]
                if(instruction_list[2].split("@")[0] == "string"):
                    value_ = instruction_list[2].removeprefix("string@")
                else:
                    value_ = instruction_list[2].split("@")[1] 
            program.append({
                "opcode": first, 
                "arg1": {"type": "var", "value": instruction_list[1]}, 
                "arg2": {"type": type_, "value": value_}})
            
        # <var> <type>
        case "READ":
            operands_num_check(2)
            check_var(instruction_list[1])
            check_type(instruction_list[2])
            program.append({
                "opcode": first, 
                "arg1": {"type": "var", "value": instruction_list[1]}, 
                "arg2": {"type": "type", "value": instruction_list[2]}})

        # <var> <symb1> <symb2>
        case "ADD" | "SUB" | "MUL" | "IDIV" | "LT" | "GT" | "EQ" | "AND" | "OR" | "STRI2INT" | "CONCAT" | "GETCHAR" | "SETCHAR":
            operands_num_check(3)
            check_var(instruction_list[1])
            check_symb(instruction_list[2])
            check_symb(instruction_list[3])
            if((instruction_list[2].split("@")[0] == "LF")|(instruction_list[2].split("@")[0] == "GF")|(instruction_list[2].split("@")[0] == "TF")):
                type_1 = "var"
                value_1 = instruction_list[2]
            else:
                type_1 = instruction_list[2].split("@")[0] 
                if(instruction_list[2].split("@")[0] == "string"):
                    value_1 = instruction_list[2].removeprefix("string@")
                else:
                    value_1 = instruction_list[2].split("@")[1] 
            if((instruction_list[3].split("@")[0] == "LF")|(instruction_list[3].split("@")[0] == "GF")|(instruction_list[3].split("@")[0] == "TF")):
                type_2 = "var"
                value_2 = instruction_list[3]
            else:
                type_2 = instruction_list[3].split("@")[0] 
                if(instruction_list[3].split("@")[0] == "string"):
                    value_2 = instruction_list[3].removeprefix("string@")
                else:
                    value_2 = instruction_list[3].split("@")[1]  
            program.append({
                "opcode": first, 
                "arg1": {"type": "var", "value": instruction_list[1]}, 
                "arg2": {"type": type_1, "value": value_1},
                "arg3": {"type": type_2, "value": value_2}})

        # <label> <symb1> <symb2>
        case "JUMPIFEQ" | "JUMPIFNEQ":
            operands_num_check(3)
            check_label(instruction_list[1])
            check_symb(instruction_list[2])
            check_symb(instruction_list[3])
            if((instruction_list[2].split("@")[0] == "LF")|(instruction_list[2].split("@")[0] == "GF")|(instruction_list[2].split("@")[0] == "TF")):
                type_1 = "var"
                value_1 = instruction_list[2]
            else:
                type_1 = instruction_list[2].split("@")[0] 
                if(instruction_list[2].split("@")[0] == "string"):
                    value_1 = instruction_list[2].removeprefix("string@")
                else:
                    value_1 = instruction_list[2].split("@")[1] 
            if((instruction_list[3].split("@")[0] == "LF")|(instruction_list[3].split("@")[0] == "GF")|(instruction_list[3].split("@")[0] == "TF")):
                type_2 = "var"
                value_2 = instruction_list[3]
            else:
                type_2 = instruction_list[3].split("@")[0] 
                if(instruction_list[3].split("@")[0] == "string"):
                    value_2 = instruction_list[3].removeprefix("string@")
                else:
                    value_2 = instruction_list[3].split("@")[1] 
            program.append({
                "opcode": first, 
                "arg1": {"type": "label", "value": instruction_list[1]}, 
                "arg2": {"type": type_1, "value": value_1},
                "arg3": {"type": type_2, "value": value_2}})
            

        #more headers in a source file
        case ".IPPCODE24":
            print('ERROR(23) - Error in lexical or syntax analysis of source code in IPPcode24', file=sys.stderr)
            sys.exit(23)

        #otherwise
        case _:
            print('ERROR(22) - Wrong format of an operation code in source code IPPcode24', file=sys.stderr)
            sys.exit(22)
            
if(header_found == False):
    print('ERROR(21) - Missing Header in input File', file=sys.stderr)
    sys.exit(21)
    
#xml output generator
xml_code = generate_xml(program)
#printing the xml output
for part in xml_code:
    print(part)
