# -*- coding: utf8 -*-

class Node(object):
    def __init__(self):
        self.word = None
        self.is_head = False
        self.is_tail = False
        self.sub_words = dict()


class TreeMatch(object):

    def __init__(self):
        self.head_node = Node()

    # given a list of words, push into Match Trees
    def build(self, words_list):
        for words in words_list:
            if not words:
                continue
            pre_node = self.head_node
            for idx, w in enumerate(words):
                cur_node = pre_node.sub_words.get(w, None)
                if cur_node is None:
                    cur_node = Node()
                cur_node.word = w
                if idx == 0:
                    cur_node.is_head = True
                elif idx == len(words) - 1:
                    cur_node.is_tail = True
                pre_node.sub_words[w] = cur_node
                pre_node = cur_node

    # find matched keywords
    def find(self, sentence, find_once=False):
        found_keywords = set()
        pre_nodes = list()
        temp_res_list = list()
        valid_index = set()
        for w in sentence:
            iter_range = [idx for idx in range(len(temp_res_list)) if idx in valid_index]
            for idx in iter_range:
                pre_node = pre_nodes[idx]
                temp_res = temp_res_list[idx]
                if w in pre_node.sub_words:  # which means there is a match in current subwords
                    cur_node = pre_node.sub_words[w]
                else:  # no match at all
                    cur_node = self.head_node
                    temp_res = list()
                    valid_index.remove(idx)
                for i, _ in enumerate(temp_res):  # temp result forward
                    temp_res[i] += w
                if cur_node.is_tail:  # all temp results are real match
                    found_keywords |= set(temp_res)
                    if find_once:
                        return found_keywords
                pre_nodes[idx] = cur_node

            if w in self.head_node.sub_words:  # we need to check if we need to start over from head node
                pre_nodes.append(self.head_node.sub_words[w])
                temp_res_list.append([w])
                valid_index.add(len(temp_res_list) - 1)
        return found_keywords

    def is_match(self, sentence):
        return len(self.find(sentence, True)) > 0
