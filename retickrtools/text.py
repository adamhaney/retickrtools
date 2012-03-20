"""
Text tools handles common text manipulations of elements. These operations
include things like stripping html tags, tokenizing, stemming, and filtering
symbols, urls, or other tokens that we aren't interested in.
"""

# Universe imports
from collections import OrderedDict
import nltk.stem.porter
import string
import re

# A listing of symbols that we will strip, from words
STRIP_SYMBOLS = ["<", ">", "\n", ";", ":", "/", "\\", "'",
               '"', "(", ")", "=", "-", "+", "?", "&", "~",
               "|", "{", "}", "[", "]", "#", ".", ",", "\t",
               "!", "@", "`", "%", "^", "*", "_", "$"]

# A listing of common Top Level Domains, this is not complete
TLDS = [".com", ".co.uk", ".net", ".org", ".biz", ".edu", ".gov"]

# A listing of punctuation symbols
SENTENCE_TERMINATION = [".", "!", "?"]


def not_in_word(list_, word):
    """
    A function that returns true if none of the characters in the list
    are in the word
    """
    for elm in list_:
        if elm in word:
            return False

    return True


def strip_tags(text):
    """
    Takes a body of text and strips out the xml tags
    """

    return re.sub('<[^<]+?>', '', text)


def wordlist_from_file(filename):
    """
    Takes a file of word terminated by newline characters,
    and returns a list of those words
    """

    f = open(filename)
    words = f.read()
    f.close()
    return words.split("\n")


def tokenize_and_clean(all_words):
    """
    This function takes a corpus of text and attempts to digest it
    making several assumptions. First, it lower cases all words, where
    a word is defined as a string of characters with a length greater
    than 1 seperated by a space. A word is also defined to be a string
    of characters that does not contain a digit. This cuts down on
    uuid, hashes, etc being filtered through as words.  Words are also
    defined to not contain a top level domain (no .coms, .orgs,
    .nets). This function also strips out so called "bad words" which
    are defined in conf/bad_words.txt.
    """

    # lowercase all words
    all_words = " ".join([word.lower() for word in all_words.split(" ")])

    # List of 'clean' words
    clean_words = []

    # Tokenize words
    for word in all_words.split(" "):

        # Conditionals that should match before symbols
        # are stripped out of the word.

        if (
            # Words should not contain a digit
            not_in_word(string.digits, word)

            # Words should not be urls
            and not_in_word(TLDS, word)
            ):

            # Strip these characters
            for char in STRIP_SYMBOLS:
                word = word.replace(char, "")

            # Conditionals that should match after symbols have been
            # stripped out
            if len(word) > 1:
                clean_words.append(word)

    return clean_words


class Stemmer(object):
    """
    A wrapper around NLTK's PorterStemmer. This doesn't do anything
    special but it allows us to have a common stemmer implementation
    that we use for all projects
    """
    def __init__(self):
        self.porter_stemmer = nltk.stem.porter.PorterStemmer()

    def stem(self, word):
        return self.porter_stemmer.stem_word(word)


class Story(object):
    """
    This object allows us to simplify operations that we very commonly do
    on stories. Generally when we're talking about data mining in retickr
    at some point we're talking about stories. Feeds, afterall are generally
    viewed as a collection of stories. This object implements methods for
    converting a story_object (dictionary) into a string of all of the
    elements that we generally datamine (author, title, content). It
    also goes ahead and wraps in the ability to get tokens, unique_tokens
    stems and unique tokens
    """

    def __init__(self, story_obj):
        self.story_obj = story_obj
        self._tokens = None
        self._stems = None

    def __str__(self):
        return self.dump_string()

    def dump_string(self, elements=None):
        """
        Dump string outputs a string concatenation of elements in a story
        dictionary. This method assumes that if you don't specify the
        elements that you would like a concatenation of the content,
        title and author fields.

        >>> story = Story(
        ... {"author": "Adam Haney",
        ...  "title": "Man bites dog",
        ...  "content": "Tonight in Chattanooga, TN a man bit a dog"
        ... })
        >>> story.dump_string()
        'Tonight in Chattanooga, TN a man bit a dog Man bites dog Adam Haney'

        """
        if not elements:
            elements = ["content", "title", "author"]

        story_words = ""

        for element in elements:
            story_words += self.story_obj.get(element, "") + " "

        return story_words[0:-1]

    def tokens(self, elements=None):
        """
        Outputs a tokenized version of the story. The tokenization is handled
        by the tokenize_and_clean function and the dictionary is serialized
        to a string by the Story.dump_string() or Story.__str__() method.
        If extra dictionary elements are desired they can be selected by
        passing in a list of elements

        >>> story = Story({
        ... "author": "Adam Haney",
        ... "title": "Man bites dog",
        ... "content": "Tonight in Chattanooga, TN a man bit a dog"
        ... })

        # To save space just show the first 8 tokens of the list
        >>> story.tokens()[0:8]
        ['tonight', 'in', 'chattanooga', 'tn', 'man', 'bit', 'dog', 'man']

        """
        if self._tokens == None:
            story_words = self.dump_string(elements=elements)
            self._tokens = tokenize_and_clean(story_words)

        return self._tokens

    def unique_tokens(self, elements=None):
        """
        This is the same as output tokens, but it only outputs each
        token one time.

        NOTE: This method returns a set not a list.

        >>> story = Story({
        ... "author": "Adam Haney",
        ... "title": "Man bites dog",
        ... "content": "Tonight a man bit a dog"
        ... })

        >>> story.unique_tokens()
        set(['haney', 'dog', 'tonight', 'adam', 'bit', 'bites', 'man'])
        """

        return set(self.tokens(elements=elements))

    def token_counts(self, elements=None):
        """
        Outputs a dictionary of all the tokens in the story where the
        token is the key and the number of occurences is the value

        >>> story = Story({
        ... "author": "Adam Haney",
        ... "title": "Man bites dog",
        ... "content": "a man bit a dog"
        ... })

        >>> story.token_counts()
        {'haney': 1, 'dog': 2, 'adam': 1, 'bit': 1, 'bites': 1, 'man': 2}
        """
        counts = {}
        for token in self.tokens(elements):
            counts[token] = counts.get(token, 0) + 1

        return counts

    def token_occurences_vector(
        self,
        token_vector,
        elements=None):
        """
        Outputs a vector of occurences of tokens for a list of words. This
        is helpful if you'd like to consider a word vector space for a list
        of N words.

        NOTE: To normalize this list use retickrtools.matrix

        >>> story = Story({
        ... "author": "Adam Haney",
        ... "title": "Man bites dog",
        ... "content": "a man bit a dog"
        ... })

        >>> story.token_occurences_vector(["man", "dog", "cat"])
        [2, 2, 0]
        """

        token_occurences = OrderedDict()

        # Fill dictionary with keys that have zero values
        for token in token_vector:
            token_occurences[token] = 0

        story_tokens = self.tokens(elements=elements)

        for token in story_tokens:
            if token in token_occurences:
                token_occurences[token] = token_occurences.get(token, 0) + 1

        return token_occurences.values()

    def stems(self, elements=None):
        """
        Outputs a list of word stems which is the root ignoring tense.

        >>> story = Story({
        ... "author": "Adam Haney",
        ... "title": "Man bites dog",
        ... "content": "a man bit a dog"
        ... })

        >>> story.stems()
        ['man', 'bit', 'dog', 'man', 'bite', 'dog', 'adam', 'haney']
        """

        stemmer = Stemmer()
        stems = [
            stemmer.stem(token)
            for token
            in self.tokens(elements=elements)
            ]

        return stems

    def unique_stems(self, elements=None):
        """
        Same as stems but instead outputs a set of the unique stems in
        the story

        >>> story = Story({
        ... "author": "Adam Haney",
        ... "title": "Man bites dog",
        ... "content": "a man bit a dog"
        ... })

        >>> story.unique_stems()
        set(['haney', 'bite', 'dog', 'adam', 'bit', 'man'])
        """

        return set(self.stems(elements=elements))

    def stem_occurences_vector(
        self,
        stem_vector,
        elements=None):
        """
        Given a stem_vector (which is an ordered list of stems)
        outputs a vector of the number of occurences of words in that
        list in order as a vector. NOTE: to normalize this vector use
        retickrtools.matrix.unit_vector(v)

        >>> story = Story({
        ... "author": "Adam Haney",
        ... "title": "Walking Man bites dog",
        ... "content": "He walked along, and bit the dog"
        ... })

        >>> story.stem_occurences_vector(["man", "dog", "cat", "walk"])
        [1, 2, 0, 2]

        """

        stem_occurences = OrderedDict()

        # Fill dictionary with keys that have zero values
        for stem in stem_vector:
            stem_occurences[stem] = 0

        story_stems = self.stems(elements=elements)

        for stem in story_stems:
            if stem in stem_vector:
                stem_occurences[stem] = stem_occurences.get(stem, 0) + 1

        return stem_occurences.values()

    def stem_counts(self, elements=None):
        """
        For a given story return a dictionary where the keys are
        stems which occured in the story and the values are the number
        of occurences in the story.

        >>> story = Story({
        ... "author": "Adam Haney",
        ... "title": "Walking Man bites dog",
        ... "content": "he walked up and bit the dog"
        ... })

        >>> story.stem_counts()
        {'and': 1, 'haney': 1, 'bite': 1, 'dog': 2, 'up': 1, 'walk': 2, 'adam': 1, 'the': 1, 'man': 1, 'bit': 1, 'he': 1}
        """

        counts = {}
        for stem in self.stems(elements=elements):
            counts[stem] = counts.get(stem, 0) + 1

        return counts


def get_feed_words(feed_obj, elements=None):
    if not elements:
        elements = ["content", "title", "author", "source"]

    feed_words = ""

    for story_obj in feed_obj["data"]:
        feed_words += Story(story_obj).dump_string(elements=elements)

    return feed_words

if __name__ == "__main__":
    import doctest

    extraglobs = {}

    print doctest.testmod(extraglobs=extraglobs)
