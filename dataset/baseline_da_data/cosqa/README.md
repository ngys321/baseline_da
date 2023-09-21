# cosqa.json
  {원본 데이터}

  idx: str                - 인덱스                    -> unixcoder run.py 에서 불러오긴 하는데, 실질적으론 안쓰는듯

  doc: str                - 쿼리 NL                   -> unixcoder run.py 에서 이거씀

  code: str               - 코드 PL + 코드내부 코멘트

  code_tokens: str        - 코드 PL                   -> unixcoder run.py 에서 이거씀

  docstring_tokens: str   - NL 이긴한데, 안씀

  label: int              - cosqa label

  retrieval_idx: int      - cosqa retrieval idx      -> unixcoder run.py 에서 불러오긴 하는데, 실질적으론 안쓰는듯


# cosqa_da.json
  {원본 데이터}
+ {<함수명 난독화 + 변수명 난독화 + deadcode 삽입> 해서 da 한 데이터}

  idx: str                - 인덱스                    -> unixcoder run.py 에서 불러오긴 하는데, 실질적으론 안쓰는듯

  doc: str                - 쿼리 NL                   -> unixcoder run.py 에서 이거씀

  code_tokens: str        - 코드 PL                   -> unixcoder run.py 에서 이거씀

  docstring_tokens: str   - NL 이긴한데, 안씀

  label: int              - cosqa label

  retrieval_idx: int      - cosqa retrieval idx      -> unixcoder run.py 에서 불러오긴 하는데, 실질적으론 안쓰는듯
