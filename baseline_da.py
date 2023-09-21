import json
import argparse
import logging
import random
from obfuscate_function import obfuscate_function
from obfuscate_variable import obfuscate_variable
from deadcodeInsertion import deadcodeInsertion
from deadcodeInsertion import DEADCODES

logger = logging.getLogger(__name__)


def xlcost2cosqa(input_file_path, output_file_path):

    with open(input_file_path, "r") as f:
        lines = f.readlines()

    with open(output_file_path, "w") as f:
        new_data_list = []
        for line in lines:
            data = json.loads(line)
            new_data_list.append(data)    
        json.dump(new_data_list, f, indent=4)

def codeToken2codeStr(tokens):

    code = ""
    indentation_level = 0

    for token in tokens:
        if token == "NEW_LINE":
            code += "\n"
            code += "    " * indentation_level
        elif token == "INDENT":
            indentation_level += 1
            code += "    "
        elif token == "DEDENT":
            indentation_level -= 1
            code = code[:-4]
        else:
            code += token + " "

    codeStr = code.strip()

    return codeStr

def codeStr2codeToken(code_string):

    import io
    import tokenize
    import ast

    code_bytes = code_string.encode('utf-8')
    tokens = []

    for token in tokenize.tokenize(io.BytesIO(code_bytes).readline):
        if token.type == tokenize.NEWLINE:
            tokens.append('NEW_LINE')
        elif token.type == tokenize.INDENT:
            tokens.append('INDENT')
        elif token.type == tokenize.DEDENT:
            tokens.append('DEDENT')
        else:
            tokens.append(token.string)
     
        if 'utf-8' in tokens:# 'utf-8' 토큰 삭제
            tokens = [x for x in tokens if x != 'utf-8']
        if '\n' in tokens:# '\n' 토큰 삭제
            tokens = [x for x in tokens if x != '\n']
        if '' in tokens:# '' 토큰 삭제
            tokens = [x for x in tokens if x != '']

    return tokens

def baseline_da(input_file_path, output_file_path, do_obf_func=False, do_obf_var=False, do_dead_insert=False):

    # jsonl file. e.g. xlcost.jsonl
    if input_file_path.split('.')[-1] == 'jsonl':
        
        # read
        with open(input_file_path, 'r') as f:
            lines = f.readlines()
        
        # max index checking
        idx_list = []
        for line in lines:
            data = json.loads(line)
            idx = data['idx']
            idx_list.append(idx)
        max_idx = max(idx_list)

        # write
        with open(output_file_path, 'w') as f:
            for line in lines:
                data = json.loads(line)

                # get code
                code = codeToken2codeStr(data['code_tokens'])

                # code modification
                if do_obf_func:
                    modified_code = obfuscate_function(code)
                if do_dead_insert:
                    modified_code = deadcodeInsertion(modified_code, random.choice(DEADCODES))
                if do_obf_var:
                    modified_code = obfuscate_variable(modified_code)
    
                


                # add original code
                new_data = {}
                new_data['idx'] = data['idx']
                new_data['docstring_tokens'] = data['docstring_tokens']
                new_data['code_tokens'] = data['code_tokens']
                new_data['url'] = str(data['idx']) + "-Python"
                f.write(json.dumps(new_data) + '\n')

                # add modified code
                new_data = {}
                new_data['idx'] = max_idx + data['idx']
                new_data['docstring_tokens'] = data['docstring_tokens']
                # new_data['code_tokens'] = codeStr2codeToken(modified_code) # 에러발생 위험. 가끔 modified_code가 parse 되지 않는 경우가 있음.
                try:
                    new_data['code_tokens'] = codeStr2codeToken(modified_code)
                except:
                    continue # new_data['code_tokens'] = []
                new_data['url'] = str(max_idx + data["idx"]) + "-Python"
                f.write(json.dumps(new_data) + "\n")

    # json file. e.g. cosqa.json
    elif input_file_path.split('.')[-1] == 'json':

        # read
        with open(input_file_path, 'r') as f:
            data = json.load(f)

        # max index checking
        idx_list = []
        for d in data:
            idx = int(d["idx"].split("-")[-1])
            idx_list.append(idx)
        max_idx = max(idx_list)

        # write
        with open(output_file_path, 'w') as f:
            for d in data:

                # get code
                code = d['code_tokens'] # cosqa. should i use code or code_tokens? use code but remove the comment in it. I made the code_tokens from code, removing the comment.

                # code modification
                if do_obf_func:
                    modified_code = obfuscate_function(code)
                if do_dead_insert:
                    modified_code = deadcodeInsertion(modified_code, random.choice(DEADCODES))
                if do_obf_var:
                    modified_code = obfuscate_variable(modified_code)





                # add original code
                new_data = {}
                new_data["idx"] = d["idx"]
                new_data['doc'] = d['doc']
                new_data["code_tokens"] = d["code_tokens"]
                new_data["docstring_tokens"] = d["docstring_tokens"]
                new_data["label"] = d["label"]
                new_data['retrieval_idx'] = int(d["idx"].split("-")[-1])
                f.write(json.dumps(new_data) + "\n")

                # add modified code
                new_data = {}
                new_data["idx"] = "cosqa-train-"+str(int(max_idx) + int(d["idx"].split("-")[-1]))
                new_data['doc'] = d['doc']
                new_data["code_tokens"] = modified_code
                new_data["docstring_tokens"] = d["docstring_tokens"]
                new_data["label"] = d["label"]
                new_data['retrieval_idx'] = int(max_idx) + int(d["idx"].split("-")[-1])
                f.write(json.dumps(new_data) + "\n")


if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument('--do_obf_func', action='store_true', help='do obfuscate function')

    parser.add_argument('--do_obf_var', action='store_true', help='do obfuscate variable')

    parser.add_argument('--do_dead_insert', action='store_true', help='do dead code insertion')

    args = parser.parse_args()

    logger.info(args)


    # data augmentation
    in_cosqa = '/home/ysnamgoong42/ws/baseline_da/dataset/cosqa.json'
    out_cosqa = '/home/ysnamgoong42/ws/baseline_da/dataset/cosqa_da_.json'
    baseline_da(in_cosqa, out_cosqa, do_obf_func=args.do_obf_func, do_obf_var=args.do_obf_var, do_dead_insert=args.do_dead_insert)
    in_xlcost = '/home/ysnamgoong42/ws/baseline_da/dataset/xlcost.jsonl'
    out_xlcost = '/home/ysnamgoong42/ws/baseline_da/dataset/xlcost_da.jsonl'
    baseline_da(in_xlcost, out_xlcost, do_obf_func=args.do_obf_func, do_obf_var=args.do_obf_var, do_dead_insert=args.do_dead_insert)
    # xlcost2cosqa: format 변경. cosqa 만 해줌. xlcost는 안해도됨.
    input_file_path = '/home/ysnamgoong42/ws/baseline_da/dataset/cosqa_da_.json'
    output_file_path = '/home/ysnamgoong42/ws/baseline_da/dataset/cosqa_da.json'
    xlcost2cosqa(input_file_path, output_file_path)


# python baseline_da.py --do_obf_func --do_obf_var --do_dead_insert