import ast
import random
import textwrap


DEADCODES = [
    """
    if False:
        print("This will never print.")
    """,

    """
    OF_NO_USE_VAR = 10
    if OF_NO_USE_VAR != 10:
        OF_NO_USE_VAR = 5
    """,

    """
    def unused_function():
        return "I am never used!"
    """,

    """
    just_str_var = "Hello"
    if just_str_var == "Goodbye":
        just_str_var = "Hi"
    """,

    """
    list_var_of_no_use = [1, 2, 3]
    if len(list_var_of_no_use) > 100:
        list_var_of_no_use.append(4)
    """,

    """
    just_normal_var = 5
    if just_normal_var == 6:
        just_normal_var = 7
    """,

    """
    just_dictionary_var = {"key": "value"}
    if "nonexistent_key" in just_dictionary_var:
        print(just_dictionary_var["nonexistent_key"])
    """,

    """
    boolean_var_for_deadcode = True
    if not boolean_var_for_deadcode:
        boolean_var_for_deadcode = False
    """,

    """
    list_var_for_deadcode = [10, 20, 30]
    if 40 in list_var_for_deadcode:
        list_var_for_deadcode.remove(40)
    """,

    """
    sth_of_no_use = None
    if sth_of_no_use:
        sth_of_no_use = "I am not None now!"
    """
]




def deadcodeInsertion(given_code: str, deadcode: str) -> str:
    # 함수 정의 시작을 찾는다.
    function_start = given_code.find("def ")

    # 'def '를 찾을 수 없으면, 그대로의 given_code를 반환한다.
    if function_start == -1:
        return given_code

    # 함수 정의 끝을 찾기 위해 ':'를 이용한다.
    function_end = given_code.find(":", function_start)

    # ':' 를 찾을 수 없으면, 그대로의 given_code를 반환한다.
    if function_end == -1:
        return given_code

    # ':' 뒤의 첫 번째 개행까지를 함수 헤더로 간주하고 그 위치를 찾는다.
    first_newline_after_function = given_code.find("\n", function_end)

    # 함수 내부의 기본 들여쓰기를 결정한다. (4 스페이스로 가정)
    indentation = " " * 4

    # DEADCODE의 각 줄에 들여쓰기를 추가한다. 단, 마지막 줄은 제외한다.
    lines = deadcode.split("\n")
    indented_deadcode_lines = [indentation + line if line.strip() else line for line in lines[:-1]]  # 마지막 줄 전까지
    indented_deadcode_lines.append(lines[-1])  # 마지막 줄은 들여쓰기 없이 추가
    indented_deadcode = "\n".join(indented_deadcode_lines)

    # 들여쓰기가 추가된 DEADCODE를 삽입한다.
    modified_code = given_code[:first_newline_after_function + 1] + indented_deadcode + "\n" + given_code[first_newline_after_function + 1:]

    return modified_code



if __name__ == '__main__':


    # 테스트
    sample_code = """
    def test_function():
        print("Hello, World!")

    if True:
        print("Inside if")

    print("Outside function")
    """

    # sample_code = """
    # def is_majority ( arr , n , x ) : 
    #     last = n // 2 
    #     if n % 2 == 0 : 
    #         last += 1 
    #     for i in range ( last ) : 
    #         if arr [ i ] == x and arr [ i + n // 2 ] == x : 
    #             return 1 
    #     return - 1 
    # arr = [ 1 , 2 , 3 , 4 , 4 , 4 , 4 ] 
    # n = len ( arr ) 
    # x = 4 
    # if is_majority ( arr , n , x ) == 1 : 
    #     print ( f"{x} appears more than {n//2} times in arr[]" ) 
    # else : 
    #     print ( f"{x} does not appear more than {n//2} times in arr[]" )
    # """

    modified_code = deadcodeInsertion(sample_code, random.choice(DEADCODES))
    print(sample_code)
    print('-'*120)
    print(modified_code)


# modified_code = deadcodeInsertion(sample_code, random.choice(DEADCODES))