#! /usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
import sys

def tag4_training_set(file_name,file_name_store):
    fin = codecs.open(file_name, 'r', 'utf-8')
    contents = fin.read()
    contents = contents.replace(u'\r', u'')
    contents = contents.replace(u'\n', u'')
    
    words = contents.split(' ')
    print len(words)
 
    tag_words_list = []
    i = 0
    for word in words:
        i += 1
        wordlen=len(word)
        if(i % 100 == 0): 
            tag_words_list.append(u'\r')
        if(wordlen == 0):
            continue
        if(wordlen == 1):
            tag_word = word + '/S'
        elif (wordlen== 2):
            tag_word = word[0] + '/B' + word[1] + '/E'
        else:
            tag_word = word[0] + '/B' 
            mid_words = word[1:-1]
            for mid_word in mid_words:
                tag_word += (mid_word + '/M')
            tag_word += (word[-1] + '/E')
 
        tag_words_list.append(tag_word)
 
    tag_words = ''.join(tag_words_list)
    fout = codecs.open(file_name_store, 'w', 'utf-8')
    fout.write(tag_words)
    fout.close()
 
    return (words, tag_words_list)

def get_near_char(contents, i, times):
    words_len = len(contents) / times;
    if (i < 0 or i > words_len - 1):
        return '_'
    else:
        return contents[i*times]
 
def get_near_tag(contents, i ,times):
    words_len = len(contents) / times;
    if (i < 0 or i > words_len - 1):
        return '_'
    else:
        return contents[i*times*2]
 
def isPu(char):
    punctuation = [u'，', u'。', u'？', u'！', u'；', u'－－', u'、', u'——', u'（', u'）', u'《', u'》', u'：', u'“', u'”', u'’', u'‘']
    if char in punctuation:
        return '1'
    else:
        return '0'
 
def get_class(char):
    zh_num = [u'零', u'○', u'一', u'二', u'三', u'四', u'五', u'六', u'七', u'八', u'九', u'十', u'百', u'千', u'万']
    ar_num = [u'0', u'1', u'2', u'3', u'4', u'5', u'6', u'7', u'8', u'9', u'.', u'０',u'１',u'２',u'３',u'４',u'５',u'６',u'７',u'８',u'９']
    date = [u'日', u'年', u'月']
    letter = ['a', 'b', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'g', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    if char in zh_num or char in ar_num:
        return '1'
    elif char in date:
        return '2'
    elif char in letter:
        return '3'
    else:
        return '4'


# 获取训练集特征
def get_event(tag_file_path, event_file_path):
    f = codecs.open(tag_file_path, 'r', 'utf-8')
    contents = f.read()
    contents = contents.replace(u'\r', u'')
    contents = contents.replace(u'\n', u'')
    words_len = len(contents)/3
    event_list = []
 
    index = range(0, words_len)
    for i in index:
        pre_char = get_near_char(contents, i-1, 3)
        pre_pre_char = get_near_char(contents, i-2, 3)
        cur_char = get_near_char(contents, i, 3)
        next_char = get_near_char(contents, i+1, 3)
        next_next_char = get_near_char(contents, i+2, 3)
        event_list.append(
            contents[i*3+2] + ' '
            + 'C-2='+pre_pre_char + ' ' + 'C-1='+pre_char + ' '
            + ' ' + 'C0=' + cur_char + ' '
            + 'C1=' + next_char + ' ' + 'C2=' + next_next_char + ' '
            + 'C-2=' + pre_pre_char + 'C-1=' + pre_char + ' '
            + 'C-1=' + pre_char + 'C0=' + cur_char + ' '
            + 'C0=' + cur_char + 'C1=' + next_char + ' '
            + 'C1=' + next_char + 'C2=' + next_next_char + ' '
            + 'C-1=' + pre_char + 'C1=' + next_char + ' '
            + 'C-2=' + pre_pre_char + 'C-1=' + pre_char + 'C0=' + cur_char + ' '
            + 'C-1=' + pre_char + 'C0=' + cur_char + 'C1=' + next_char + ' '
            + 'C0=' + cur_char + 'C1=' + next_char + 'C2=' + next_next_char + ' '
            + 'Pu=' + isPu(cur_char) + ' '
            + 'Tc-2=' + get_class(pre_pre_char) + 'Tc-1=' + get_class(pre_char)
            + 'Tc0=' + get_class(cur_char) + 'Tc1=' + get_class(next_char)
            + 'Tc2=' + get_class(next_next_char) + ' '
            + '\r')
 
 
    # events = ''.join(event_list)
    fout = codecs.open(event_file_path, 'w', 'utf-8')
    for event in event_list:
        fout.write(event)
    fout.close()
 

def main():
    args = sys.argv[1:]
    if len(args) < 3: 
        print " "+args[0]+" "+args[1]+" "
        print 'Usage: python ' + sys.argv[0] + ' training_file test_file result_file'
        exit(-1)
    training_file = args[0]
    test_file = args[1]
    result_file = args[2]
 
    tag_training_set_file=training_file +'.tag'
    # 标注训练
    tag4_training_set(training_file, tag_training_set_file)
    #tag6_training_set(training_file, tag_training_set_file)
    print 'tag train set succeed'
 
    # 获取训练集特征
    feature_file_path = training_file + ".feature"
    get_event(tag_training_set_file, feature_file_path)
    print 'get training set feature succeed'



if __name__=="__main__":
    main()