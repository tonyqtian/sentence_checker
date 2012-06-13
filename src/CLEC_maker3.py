'''
Created on Jun 8, 2012

@author: Tony
'''
filename = '../data/CLEC_error.dat'
input_ =  open(filename, 'r')

filename = '../data/CLEC_tagged.dat'
output_ =  open(filename, 'w')

head = '<ERR type='
tail = ' </ERR>'

for line in input_:
    line = line.strip()
    words = line.split()
    this_word = list(words)
    for i in range(len(this_word)):
        if this_word[i].startswith('['):
            if i > 0:
                if this_word[i-1].endswith('ERR>') or this_word[i-1] == '':
                    this_word[i] = ''
                    if i < len(this_word)-1:
                        if this_word[i+1].endswith(']'):
                            this_word[i+1] = ''
                    continue
                tag = this_word[i]
                target = this_word[i-1]
                if i < len(this_word)-1:
                    if this_word[i+1].endswith(']'):
                        tag = tag + this_word[i+1]
                        this_word[i+1] = ''
                this_word[i-1] = head + tag + '>'
                this_word[i] = target + tail
    line = ''
    for word in this_word:
        if word == '':
            continue
        else:
            line = line + ' ' + word
    line = line.strip()
    line = line + '\n'
    output_.write(line)