import re
import pandas as pd
from utils.hanguel import preprocess_morpheme_sentence, split_syllables, levenshteinDistance
import MeCab
import time
import openai
from api import GPT, Example


class Idiom_Translator(object):

    def __init__(self, openai_api_key=None, data_path='data/tokenized_idiom.csv', device='cpu') -> None:
        self.data_path = data_path
        self.openai_api_key = openai_api_key
        self.total_rules = ''
        self.idiom_dict = {}
        self.make_rules()
        self.mecab = MeCab.Tagger()
        self.gpt = None
        self.device = device
        if openai_api_key is not None:
            self.setGPT3()
        else:
            self.setMarainMTModel()

    def make_rules(self):
        idioms = pd.read_csv(self.data_path, encoding='utf-8')

        for i, word in enumerate(idioms['idiom']):
            if word.replace(' ', '') == '':
                continue
            self.idiom_dict[word] = f'{idioms.loc[i, "meaning"]}'.strip()
            if i==0:
                self.total_rules= f'{word}'
            else:
                self.total_rules += f'|{word}'
    
    def setGPT3(self):
        openai.api_key = self.openai_api_key
        self.gpt = GPT(engine="davinci",
                       temperature=0.4,
                       max_tokens=512)
        # examples for prompt learning
        self.gpt.add_example(Example('리더십은 조직의 다른 구성원들에게 영향을 미치고 지도하는 개인의 능력이다.',
                        'Leadership is the ability of an individual to influence and guide other members of an organization.'))
        self.gpt.add_example(Example('그 호텔에는 장애인들을 맞을 수 있는 특수 시설이 되어 있다.',
                                'The hotel has special facilities for welcoming disabled people.'))
        self.gpt.add_example(Example('외형상으로는 어느 모로 보아도 그들은 완벽하게 행복했다.',
                                'To all outward appearances they were perfectly happy.'))
        self.gpt.add_example(Example('선택할 수 있는 길은 항복하느냐 끝까지 싸우느냐 둘 중의 하나다.',
                                'The alternative possibilities are surrender or fighting to the last ditch. '))

    def setMarainMTModel(self):
        from transformers import MarianMTModel, MarianTokenizer

        # neural machine translation model name (Korean to English)
        model_name = 'Helsinki-NLP/opus-mt-ko-en'
        self.nmt_tokenizer = MarianTokenizer.from_pretrained(model_name)
        # print(tokenizer.supported_language_codes)

        self.nmt = MarianMTModel.from_pretrained(model_name).to(self.device)


    def tokenize(self, text, spacing_tkn='__'):
        '''
        사전 구성시 사용한 전처리 방식대로 한 토큰화 함수
        '''
        # replace white space to spacing token
        text_spacing = text.replace(' ', spacing_tkn)
        # tokenize
        pos = self.mecab.parse(text_spacing).split('\n')
        tokens = []
        for i, p in enumerate(pos):
            token = p.split('\t')[0]
            # 연결 어미, 종결 어미 제외
            if token == "EOS":
                break
    #         if "EC" in p and len(pos) == i+3:
    #             break
    #         if "다" in token and len(pos) == i+3:
    #             token = token.replace('다','')
            # 복합 일때
            features = p.split(',')
            
            if features[-1] != '*':
                for f in features[-1].split('+'):
                    tokens.append(f.split('/')[0])
            else:
                tokens.append(token)
        return tokens

    def getRange(self, match:re.Match, text:str, extend_front:int=20, extend_rear:int=5):
        ''' 
        관용구를 제외한 관용구 앞, 뒤 문장 반환.
        Arguments:
            match (re.Match): tokenized sentence에서 관용구 정규식 매칭 결과
            text (str): 최초 입력 문장
            extend_front (int): text에서 관용구를 찾을 앞의 확장 범위
            extend_rear (int): text에서 관용구를 찾을 뒤의 확장 범위
        Returns:
            list[str, str]
        '''
        # match는 tokenized sentence를 ' ' 공백으로 이어 붙인 것이라 원 문장보다 더 길기 때문에 확장해서 찾아야 한다.
        start = match.start() - extend_front if match.start() -extend_front >= 0 else 0
        end = match.end() + extend_rear if match.end() + extend_rear < len(text) else len(text)
        
        best = None
        bestScore = 9999
        # 관용구를 음절 단위 분리
        right_syllables = split_syllables(match.group())
        
        for i in range(start, end):
            for j in range(i+1, end):
                tmp = text[i:j]
                # 블랭크는 제외
                if tmp.replace(' ','') == "":
                    continue
                # 관용구와 가장 유사한 원문장의 문자열 일부를 찾는 기준을 "편집거리"를 사용한다.
                score = levenshteinDistance(match.group(), tmp)
                # 편집거리는 작을수록 가장 유사한 것이고, 0이면 동일한 문자열
                if bestScore > score:
                    # 문자열의 시작, 끝 위치를 저장한다.
                    best = (i, j)
                    bestScore = score
                    best_syllables = split_syllables(tmp)
                    # 동일하면 바로 반환
                    if score == 0:
                        return [text[:best[0]], text[best[1]:]]
                elif bestScore == score: # 편집거리가 같으면
                    # 더 긴 것을 베스트로 한다.
                    # 논리적 근거보다는 경험적 근거로 긴 것이 더 유사한 경우가 많았다.
                    # ex) "기가 차"에 대해 "기가 "와 "기가 찼"이 있을 경우 둘의 편집거리는 같으나 후자가 더 바람직한 유사답안이다.
                    if best[1] - best[0] < j-i:
                        best = (i, j)
                        bestScore = score
                        best_syllables = split_syllables(tmp)
                    elif best[1] - best[0] == j-i: # 길이도 동일하면
                        # 그다음은 음절 단위로 edit distance 비교
                        tmp_syllables = split_syllables(tmp)
                        if levenshteinDistance(right_syllables, tmp_syllables) > levenshteinDistance(right_syllables, best_syllables):
                            best = (i, j)
                            bestScore = score
                            best_syllables = tmp_syllables
        
        # 매칭되는 값이 있는데 못 찾은 것이라 에러 메세지 반환
        if best is None:
            raise Exception('Not Found')
        else:
            best_sentence = [text[:best[0]], text[best[1]:]]
            return best_sentence


    def idiomToMeaning(self, target, constraints):
        '''
        문장 내의 관용구를 그 의미로 바꿔서 반환해준다.
        Arguments:
            target (str): 대상 문장
            constraints (list): 최초 문장에서 re.findall()로 찾은 관용구 목록
        Return:
            A string
        '''
        
        rest = None
        
        while True:
            # print(f'\ntarget : {target}')
            # tokenize
            tokenized = self.tokenize(target, spacing_tkn=' ')
            # 공백으로 토큰을 이어 붙인다.
            tokenized = ' '.join(tokenized)
            
            # 관용구 찾기
            search_res = re.search(self.total_rules, tokenized)
            
            # 관용구가 있으면
            if search_res:
                if search_res.group() not in constraints:
                    return target
                # print(f'{search_res}')
                # 관용구 사전에서 뜻 찾기
                meaning = self.idiom_dict[search_res.group()]
                
                # 의미 문장 전처리하기
                meaning = preprocess_morpheme_sentence(meaning)
                rest = self.getRange(search_res, target)
                
                # TODO : 여기서 대체할 때 조사라든지 유의할 부분 있음. 자연스럽게 이을 방법 고민하기
                if '' == rest[0] or ' ' == rest[0]:
                    target = f"{rest[0]}{meaning} {self.idiomToMeaning(rest[1], constraints)}"
                else:
                    if rest[0][-1] != ' ':
                        target = f"{self.idiomToMeaning(rest[0], constraints)} {meaning} {self.idiomToMeaning(rest[1], constraints)}"
                    else:
                        target = f"{self.idiomToMeaning(rest[0], constraints)}{meaning} {self.idiomToMeaning(rest[1], constraints)}"
                
            else: 
                return target

    def translate(self, text:str):
        tokenized = self.tokenize(text, spacing_tkn=' ')
        # 공백으로 토큰을 이어 붙인다.
        tokenized = ' '.join(tokenized)
        re_totals = re.findall(self.total_rules, tokenized)
        
        itm_sentence = self.idiomToMeaning(text, re_totals)
        if self.gpt is not None:
            output = self.gpt.submit_request(itm_sentence)['choices'][0]["text"]
        
            '''
            {
            "choices": [
                {
                "finish_reason": "stop",
                "index": 0,
                "logprobs": null,
                "text": "output: She tried to get his attention by grabbing his sleeve.\n\n"
                }
            ],
            "created": 1638189924,
            "id": "asfrnvkelssssepe3k32dm",
            "model": "davinci:2020-05-03",
            "object": "text_completion"
            }
            '''
            if output[:8] == 'output: ':
                output = output[8:]
            output = output.replace('\n','')
        else: # hf's NMT model
            translated = self.nmt.generate(**self.nmt_tokenizer(f'>>eng<< {itm_sentence}', return_tensors="pt", padding=True))
            output = self.nmt_tokenizer.decode(translated[0], skip_special_tokens=True)
        return output
        





# s = time.time()
# target_sent = "그의 뻔뻔스러운 태도에 할 말을 잊고 기가 찼다."
# tokenized = tokenize(target_sent, spacing_tkn=' ')
# # 공백으로 토큰을 이어 붙인다.
# tokenized = ' '.join(tokenized)
# re_totals = re.findall(total_rules, tokenized)
# print('\noriginal : {target_sent}\nresult\n',idiomToMeaning(target_sent, re_totals))
# print(idiomToMeaning('그의 뻔뻔스러운 태도에 놀랍거나 어처구니없는 일을 당하여 기가 막히고 기가 찼다.'))

# print(time.time()-s)