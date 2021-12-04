# 실행시 root 권한 부여해서 실행 바람

# Mecab
wget -O - https://bitbucket.org/eunjeon/mecab-ko/downloads/mecab-0.996-ko-0.9.2.tar.gz | tar zxfv -
mv mecab-0.996-ko-0.9.2 ~/
cd ~/mecab-0.996-ko-0.9.2; ./configure; make; make install; ldconfig

# Mecab-Ko-Dic
wget -O - https://bitbucket.org/eunjeon/mecab-ko-dic/downloads/mecab-ko-dic-2.1.1-20180720.tar.gz | tar zxfv -
mv mecab-ko-dic-2.1.1-20180720 ~/
cd ~/mecab-ko-dic-2.1.1-20180720; sh ./autogen.sh
cd ~/mecab-ko-dic-2.1.1-20180720; ./configure; make; make install; ldconfig

# Mecab-Python
git clone https://bitbucket.org/eunjeon/mecab-python-0.996.git
mv mecab-python-0.996 ~/
cd ~/mecab-python-0.996; python setup.py build; python setup.py install

