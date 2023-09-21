
import re

def obfuscate_function(code):
    # 함수명을 추출합니다.
    function_names = re.findall(r'def\s+(\w+)\s*\(', code)

    # 함수명을 순차적으로 변경합니다.
    obfuscated_code = code
    for index, func_name in enumerate(function_names):
        obfuscated_code = obfuscated_code.replace(func_name, f"func{index}")

    return obfuscated_code




if __name__ == '__main__':

    code = """
    def add(x, y):
        return x + y
    def sub(x, y):
        return x - y
    def mul(x, y):
        return x * y
    print(add(1, 2))
    print(sub(10, 3) + 4)
    """

    # code = "def string_to_list ( string , sep = \",\" , filter_empty = False ) : return [ value . strip ( ) for value in string . split ( sep ) if ( not filter_empty or value ) ]"

    # code = '''
    # R = 3 
    # C = 3 
    # MAX_K = 1000 
    # def pathCountDP( mat , m , n , k , dp ) : 
    #     if m < 0 or n < 0 : 
    #         return 0 
    #     elif m == 0 and n == 0 : 
    #         return k == mat [ m ] [ n ] 
    #     if dp [ m ] [ n ] [ k ] != - 1 : 
    #         return dp [ m ] [ n ] [ k ] 
    #     dp [ m ] [ n ] [ k ] = ( pathCountDP ( mat , m - 1 , n , k - mat [ m ] [ n ] , dp ) + pathCountDP ( mat , m , n - 1 , k - mat [ m ] [ n ] , dp ) ) 
    #     return dp [ m ] [ n ] [ k ] 
    # def pathCount ( mat , k ) : 
    #     dp = [ [ [ - 1 for col in range ( MAX_K ) ] for col in range ( C ) ] for row in range ( R ) ] 
    #     return pathCountDP ( mat , R - 1 , C - 1 , k , dp ) 
    # k = 12 
    # mat = [ [ 1 , 2 , 3 ] , [ 4 , 6 , 5 ] , [ 3 , 2 , 1 ] ] 
    # print ( pathCount ( mat , k ) )
    # '''

    print(code)
    print('-'*120)
    print(obfuscate_function(code))