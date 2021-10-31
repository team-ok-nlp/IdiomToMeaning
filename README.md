# IdiomToMeaning
* Idiom Machine Translation Using Prompt learning 
* gpt3의 prompt learning을 활용한 관용구 기계 번역

## Preprocessing

1. 사전 구축

* 형태소 분석기 : Mecab
    - 선정 근거
        - https://velog.io/@metterian/%ED%95%9C%EA%B5%AD%EC%96%B4-%ED%98%95%ED%83%9C%EC%86%8C-%EB%B6%84%EC%84%9D%EA%B8%B0POS-%EB%B6%84%EC%84%9D-3%ED%8E%B8.-%ED%98%95%ED%83%9C%EC%86%8C-%EB%B6%84%EC%84%9D%EA%B8%B0-%EB%B9%84%EA%B5%90
        - https://iostream.tistory.com/144
* 관용구를 형태소 분석 후 어미 제거
* 관용구 데이터는 국립국어원에서 제공
* 뜻풀이에 직접적인 뜻만 남겨두는 작업은 직접 손수 정제

## Search & Paraphrase

1. 관용구를 정규식으로 OR로 모두 하나의 string 변수로 저장한다.
2. 입력 문장에 대해 토크나이징
3. 입력 문장에 대해 관용구 정규식 규칙으로 관용구를 검색한다.
4. 관용구 사전에서 검색 결과로 나온 관용구를 키값으로 활용하여 해당 관용구의 뜻풀이 값을 가져온다.
5. 원 문장에서 관용구를 뜻풀이로 교체한다.

## Machine Translation 

* gpt3 api 활용법
    - https://gimkuku0708.tistory.com/12
    
