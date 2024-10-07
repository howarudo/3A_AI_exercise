# EOSとは End Of Sentence の略であり，文の終わりを意味する
# EOSの単語IDを0と定義する

from collections import Counter

EOS_ID = 0
UNKWOWN_WORD_ID = 1
UNKNOWN_THRESHOLD = 1


class SentenceData:
    def __init__(self, file_name):
        with open(file_name, "r") as f:
            self.en_word_to_id = {"<EOS>": EOS_ID, "<UNKNOWN>": UNKWOWN_WORD_ID}
            self.en_word_list = ["<EOS>", "<UNKNOWN>"]
            self.jp_word_to_id = {"<EOS>": EOS_ID, "<UNKNOWN>": UNKWOWN_WORD_ID}
            self.jp_word_list = ["<EOS>", "<UNKNOWN>"]
            self.raw_en_sentences = []
            self.raw_jp_sentences = []


            self.en_sentences = []
            self.jp_sentences = []
            line = f.readline().rstrip("\n")
            while line:
                sentences = line.split("\t")
                english = sentences[0].split(" ")
                japanese = sentences[1].split(" ")
                self.raw_en_sentences.append(list(map(str.lower, english)))
                self.raw_jp_sentences.append(japanese)
                line = f.readline().rstrip("\n")

            self.en_counter = Counter()
            self.jp_counter = Counter()
            for raw_en_sentence, raw_jp_sentence in zip(self.raw_en_sentences, self.raw_jp_sentences):
                self.en_counter.update(raw_en_sentence)
                self.jp_counter.update(raw_jp_sentence)

            for raw_en_sentence in self.raw_en_sentences:
                en_sentence = []
                for word in raw_en_sentence:
                    if self.en_counter[word] <= UNKNOWN_THRESHOLD:
                        word = "<UNKNOWN>"
                    if word not in self.en_word_to_id:
                        id = len(self.en_word_list)
                        self.en_word_list.append(word)
                        self.en_word_to_id[word] = id
                    id = self.en_word_to_id[word]
                    en_sentence.append(id)
                self.en_sentences.append(en_sentence)

            for raw_jp_sentence in self.raw_jp_sentences:
                jp_sentence = []
                for word in raw_jp_sentence:
                    if self.jp_counter[word] <= UNKNOWN_THRESHOLD:
                        word = "<UNKNOWN>"
                    if word not in self.jp_word_to_id:
                        id = len(self.jp_word_list)
                        self.jp_word_list.append(word)
                        self.jp_word_to_id[word] = id
                    id = self.jp_word_to_id[word]
                    jp_sentence.append(id)
                self.jp_sentences.append(jp_sentence)

                # # 単語IDのリスト
                # en_sentence = []
                # for word in english:
                #     word = word.lower()
                #     id = 0
                #     if word in self.en_word_to_id:
                #         id = self.en_word_to_id[word]
                #     else:
                #         id = len(self.en_word_list)
                #         self.en_word_list.append(word)
                #         self.en_word_to_id[word] = id
                #     en_sentence.append(id)

                # # 単語IDのリスト
                # jp_sentence = []
                # for word in japanese:
                #     id = 0
                #     if word in self.jp_word_to_id:
                #         id = self.jp_word_to_id[word]
                #     else:
                #         id = len(self.jp_word_list)
                #         self.jp_word_list.append(word)
                #         self.jp_word_to_id[word] = id
                #     jp_sentence.append(id)
                # self.en_sentences.append(en_sentence)
                # self.jp_sentences.append(jp_sentence)

    def sentences_size(self):
        return len(self.en_sentences)

    def japanese_word_size(self):
        return len(self.jp_word_list)

    def english_word_size(self):
        return len(self.en_word_list)

    def japanese_sentences(self):
        return self.jp_sentences

    def english_sentences(self):
        return self.en_sentences

    def japanese_word_id(self, word):
        if word in self.jp_word_to_id:
            return self.jp_word_to_id[word]
        else:
            return UNKWOWN_WORD_ID

    def english_word_id(self, word):
        if word in self.en_word_to_id:
            return self.en_word_to_id[word]
        else:
            return UNKWOWN_WORD_ID

    def japanese_word(self, id):
        return self.jp_word_list[id]

    def english_word(self, id):
        return self.en_word_list[id]
