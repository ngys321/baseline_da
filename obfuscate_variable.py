from parser import DFG_python,DFG_java,DFG_ruby,DFG_go,DFG_php,DFG_javascript
from parser import (remove_comments_and_docstrings,
                   tree_to_token_index,
                   index_to_code_token,
                   tree_to_variable_index)
from tree_sitter import Language, Parser
dfg_function={
    'python':DFG_python,
    'java':DFG_java,
    'ruby':DFG_ruby,
    'go':DFG_go,
    'php':DFG_php,
    'javascript':DFG_javascript
}

parsers={}        
for lang in dfg_function:
    LANGUAGE = Language('parser/my-languages.so', lang)
    parser = Parser()
    parser.set_language(LANGUAGE) 
    parser = [parser,dfg_function[lang]]    
    parsers[lang]= parser
                                
def extract_dataflow(code, parser,lang):
    # try:
    #     code=remove_comments_and_docstrings(code,lang)
    # except:
    #     pass    
    if lang=="php":
        code="<?php"+code+"?>"    
    try:
        tree = parser[0].parse(bytes(code,'utf8'))    
        root_node = tree.root_node  
        tokens_index=tree_to_token_index(root_node)     
        code=code.split('\n')
        code_tokens=[index_to_code_token(x,code) for x in tokens_index]  
        index_to_code={}
        for idx,(index,code) in enumerate(zip(tokens_index,code_tokens)):
            index_to_code[index]=(idx,code)  
        try:
            DFG,_=parser[1](root_node,index_to_code,{}) 
        except:
            DFG=[]
        DFG=sorted(DFG,key=lambda x:x[1])
        indexs=set()
        for d in DFG:
            if len(d[-1])!=0:
                indexs.add(d[1])
            for x in d[-1]:
                indexs.add(x)
        new_DFG=[]
        for d in DFG:
            if d[1] in indexs:
                new_DFG.append(d)
        dfg=new_DFG
        
        variable_index=tree_to_variable_index(root_node, index_to_code)
        
    except:
        dfg=[]
    return code_tokens, dfg, tokens_index, index_to_code, variable_index

parser = parsers['python']
lang = 'python'













def get_variables(code):
    
    code_tokens, dfg, tokens_index, index_to_code, variable_index = extract_dataflow(code, parser, lang)

    v = []
    v_id = []
    for item in dfg:
        if item[2] == 'computedFrom':
            if item[0] != '_' and item[0] != 'self':
                v.append(item[0])
                v_id.append(item)
    
    for item in dfg:
        if item[2] == 'comesFrom':
            if item[0] in v and item[0] in item[3]:
                v_id.append(item)
    

    return list(set(v)), v_id # variable, variable_identification

def obfuscate_variable(code):

    code_tokens, dfg, tokens_index, index_to_code, variable_index = extract_dataflow(code, parser, lang)

    var, var_id = get_variables(code)

    for i, v in enumerate(var):
        for v_i in var_id:
            if v == v_i[0]:
                code_tokens[v_i[1]] = 'var' + str(i)
    obfuscated_code = ' '.join(code_tokens)

    return obfuscated_code


if __name__ == '__main__':
    code = '''
    x = 1
    y = x + 2
    z = y + 3
    print(z)
    print(x)
    '''
    print(code)
    print('-'*120)
    print(obfuscate_variable(code))