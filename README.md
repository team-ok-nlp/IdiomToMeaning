# IdiomToMeaning
* Idiom Machine Translation Using Prompt learning 
* gpt3의 prompt learning을 활용한 관용구 기계 번역

## Preprocessing

1. 사전 구축

* 형태소 분석기 : Mecab
    - 선정 근거
        - https://velog.io/@metterian/%ED%95%9C%EA%B5%AD%EC%96%B4-%ED%98%95%ED%83%9C%EC%86%8C-%EB%B6%84%EC%84%9D%EA%B8%B0POS-%EB%B6%84%EC%84%9D-3%ED%8E%B8.-%ED%98%95%ED%83%9C%EC%86%8C-%EB%B6%84%EC%84%9D%EA%B8%B0-%EB%B9%84%EA%B5%90
        - https://iostream.tistory.com/144
* 관용구 데이터는 국립국어원에서 제공

2. 전처리 

* 손수 정제하는 부분
    * 뜻풀이에 직접적인 뜻만 남겨두는 작업
    * 관용구로만 쓰이지 않고 말그대로의 의미도 사용하는 관용구는 제외
        - 맥락에 따른 관용구 뜻 적용은 현 프로젝트에서는 미적용
    * 관용구의 의미가 여러 개일 경우 더 자주 쓰이는 뜻으로 한 개만 남김 
* 관용구 사전
	- 관용구와 의미를 형태소 분석 후 어미 제거하여 사전으로 저장
	- 관용구는 띄어쓰기 정보 없이 형태소 단위로만 저장 (띄어쓰기 달라도 관용구 찾을 수 있게)
	- 의미는 띄어쓰기 정보 포함(spacing token "__" 사용)하여 저장(의미 대체시 띄어쓰기 있어야 문장 복원 가능)
    - ex) 원문 : "허리가 꼿꼿한"
	- 관용구 : "허리 가 꼿꼿 하", 의미 : "나이 에 __ 비하 여 __ 젊"

## Search & Paraphrase

1. 관용구를 정규식으로 OR로 모두 하나의 string 변수로 저장한다.
2. 입력 문장에 대해 형태소 분석
3. 입력 문장에 대해 관용구 사전을 기반으로 관용구를 검색한다.
4. 관용구 사전에서 검색 결과로 나온 관용구를 키값으로 활용하여 해당 관용구의 뜻풀이 값을 가져온다.
5. 원 문장에서 관용구를 뜻풀이로 교체한다.

## Machine Translation 

* gpt3 api 활용법
    - https://gimkuku0708.tistory.com/12
* gpt3 sandbox api 활용
    - https://github.com/shreyashankar/gpt3-sandbox

## Attribution-ShareAlike 2.0 Korea (CC BY-SA 2.0 KR)

[![CC BY-SA 2.0 KR][cc-by-image]][cc-by]

This work is licensed under a [Creative Commons Attribution 2.0 Korea License][cc-by].

[cc-by]: https://creativecommons.org/licenses/by-sa/2.0/kr/
[cc-by-image]: https://i.creativecommons.org/l/by-sa/2.0/kr/88x31.png


