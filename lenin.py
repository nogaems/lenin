import random
import re


class Symbol:
    def __init__(self, symbol):
        self.symbol = symbol

    def __repr__(self):
        return repr(self.symbol)

    def __eq__(self, other):
        return isinstance(other, Symbol) and self.symbol == other.symbol

    def __ne__(self, other):
        return not isinstance(other, Symbol) or self.symbol != other.symbol

    def __hash__(self):
        return hash(f'{id(self)}{self.symbol}')


class Lenin:
    sentence_terminators = '.!?…'
    sentence_start = Symbol('sentence start')
    sentence_end = Symbol('sentence stop')
    escape_sequences = '\a\b\f\n\r\t\v'
    brackets = '()[]{}'
    quotes = '\'"”“’‘‛’„«»'

    def __init__(self, input_text):
        text = self.prepare_text(input_text)
        self.terminators = {
            t: text.count(t) for t in self.sentence_terminators
        }
        # in case if there's no actual sentence terminators in input_text
        # let's fallback to using '.'
        if not self.terminators['.']:
            self.terminators['.'] = 1
        total = sum(self.terminators.values())
        for t in self.terminators:
            self.terminators[t] = self.terminators[t] / total

        states = []
        sentences = self.split_sentences(text)
        for s in sentences:
            sentence = self.enclose_sentence(s)
            for i in range(len(sentence) - 1):
                state = [sentence[i], sentence[i+1]]
                if state not in states:
                    states.append(state)

        transitions = {}
        for _from, _to in states:
            counter = 0
            if _from not in transitions:
                transitions[_from] = {}
            for s in sentences:
                sentence = self.enclose_sentence(s)
                for f, t in [[sentence[i], sentence[i+1]] for i in range(len(sentence) - 1)]:
                    if _from == f and _to == t:
                        if _to in transitions[_from]:
                            transitions[_from][_to] += 1
                        else:
                            transitions[_from][_to] = 1
        for _from in transitions:
            total = sum(transitions[_from].values())
            for _to in transitions[_from]:
                transitions[_from][_to] = transitions[_from][_to] / total

        if not transitions:
            raise ValueError(
                'Unable to construct Markov\'s chain on the given text')
        self.transitions = transitions

    def enclose_sentence(self, sentence):
        result = [self.sentence_start]
        result.extend(sentence)
        result.extend([self.sentence_end])
        return result

    def strip_html(self, text):
        return re.sub('<[^<]+?>', '', text)

    def prepare_text(self, text):
        text = self.strip_html(text)
        text = text.replace('...', '…').replace('\n', ' ')
        for c in self.escape_sequences + self.brackets + self.quotes:
            text = text.replace(c, '')
        return text

    def split_sentences(self, text):
        for terminator in self.sentence_terminators:
            text = text.replace(terminator, '\n')
        sentences = text.split('\n')
        result = []
        for i in range(len(sentences)):
            s = sentences[i].strip().split()
            if len(s):
                s[0] = s[0].lower()
                result.append(s)
        return result

    def generate_sentence(self, max_words=20):
        result = []
        word = self.sentence_start
        while len(result) < max_words:
            variants = list(self.transitions[word].keys())
            weights = list(self.transitions[word].values())
            word = random.choices(variants, weights)[0]
            if word == self.sentence_end:
                break
            result.append(word)
        if not len(result):
            return ''
        result[0] = result[0].capitalize()
        terminator = random.choices(list(self.terminators.keys()),
                                    list(self.terminators.values()))[0]
        return ' '.join(result) + terminator
