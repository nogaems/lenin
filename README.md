# lenin
LExical NIhilistic Narrator

# Background
Well, actually it's called after Lenin because he's well-known by his ability to generate completely pointless copypastas on a frightening scale. Abbreviation decoding is completely made up.
This implementation is plain simple: it builds Markov chain on a given text and outputs sequences of words randomly chosen with respect to chains' weights.

# Installation
Within a virtual environment execute:
```bash
python setup.py install
```

# Usage
```python
import lenin

input_text = '''
Here you put text the output will be dependent on.
Keep in mind that the quality of the output of this algorithm completely depends on the size and the quality of the input text.
'''
generator = lenin.Lenin(input_text)
sentence = generator.generate_sentence()
print(sentence)
#'Keep in mind that the size and the output of the size and the quality of this algorithm completely depends.'

```
