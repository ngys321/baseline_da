# xlcost.jsonl
  {원본 데이터}

  idx: int                  - 인덱스        -> unixcoder run.py 에서 불러오긴 하는데, 실질적으론 안쓰는듯

  docstring_tokens: list    - 설명 NL       -> unixcoder run.py 에서 이거씀

  code_tokens: list         - 코드 PL       -> unixcoder run.py 에서 이거씀
  
  url: str                  - xlcost url   -> unixcoder run.py 에서 불러오긴 하는데, 실질적으론 안쓰는듯
  
  paradigm_label: int       - 예전에 뉴럴모델로 패러다임 분류한 결과 저장한것. 지금은 안씀. 



# xlcost_da.jsonl
  {원본 데이터}
+ {<함수명 난독화 + 변수명 난독화 + deadcode 삽입> 해서 da 한 데이터}

  idx: int                   - 인덱스        -> unixcoder run.py 에서 불러오긴 하는데, 실질적으론 안쓰는듯

  docstring_tokens: list     - 설명 NL       -> unixcoder run.py 에서 이거씀

  code_tokens: list          - 코드 PL       -> unixcoder run.py 에서 이거씀

  url: str                   - xlcost url   -> unixcoder run.py 에서 불러오긴 하는데, 실질적으론 안쓰는듯

