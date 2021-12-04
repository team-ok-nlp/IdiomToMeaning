from idiom_translator import Idiom_Translator
import time

if __name__=="__main__":

    sentence = "어려운 집안 사정으로 가방끈이 짧았던 아버지는 자식만큼은 대학에 보내려고 무진장 애를 쓰셨다."
    
    # nmt를 gpt3로 사용하는 경우
    openai_api_key = "sk-ENTERYOURSECRETKEY" # key 받아서 교체할 것.
    it = Idiom_Translator(openai_api_key=openai_api_key)
    print(it.translate(sentence))
    
    # nmt를 hf model 사용하는 경우
    # gpu가 없을 시 미입력 혹은 -1 부여
    device = 0
    # gpu 있으면 더 빠름
    it = Idiom_Translator(device=device)
    start= time.time()
    print(it.translate(sentence))
    print(f'time : {(time.time() - start)/60}')
    
    
    '''
    원문장 : 어려운 집안 사정으로 가방끈이 짧았던 아버지는 자식만큼은 대학에 보내려고 무진장 애를 쓰셨다.
    원문장을 번역한 문장 : The father, who had a short bag strap due to difficult family circumstances, struggled to send his child to college.

    관용구 풀이 문장 : 어려운 집안 사정으로 많이 배우지 못하아 학력이 낮 았던 아버지는 자식만큼은 대학에 보내려고 무진장 애를 쓰셨다.
    관용구 풀이 문장을 gpt3로 번역한 문장 : His father, who had been unable to get a good education because of the difficult circumstances at home, had been determined to send his son to college, come what may.
    
    "가방끈이 짧다"라는 관용구는 "많이 배우지 못하여 학력이 낮다"는 의미로 번역 문장 중 itm 번역문장은 이를 반영했으나 원문장 번역 문장은 속뜻이 아니라 말그대로 반영했습니다.
    '''


