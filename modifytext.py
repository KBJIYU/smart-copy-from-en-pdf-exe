import re


def modify_en_text(text, modify_mode='BASIC', keep_emoji=True):
    """ Make your text easy to read and to translate.

        Args:
            text(str):
                target dirty text.
            modify_mode(str):
                mode selection
            keep_emoji(bool):
                call back remove_emoji func or not.

        Returns:
            text_output(str):
                formatted output.

    """
    if not keep_emoji:
        text = remove_emoji(text)

    sents = split_text_to_sentences_en(text)
    text_output = mode_factory(modify_mode)(sents)

    return text_output


def remove_emoji(text):
    """ Remove emoji. """
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               "]+", flags=re.UNICODE)

    return emoji_pattern.sub(r'', text)


def split_text_to_sentences_en(text):
    """ Make your text easy to read and to translate.

        Args:
            text(str):
                target dirty text.
        Returns:
            sents(list):
                sentences splited.

    """

    text = text.replace(" . . . ","...") #replace LaTex ellipses with original ellipses
    
    sents = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', text)

    return sents


def mode_factory(modify_mode):
    if modify_mode == "BASIC":
        return mode_basic

    if modify_mode == 'LIST-MARK':
        return mode_listmark


def mode_basic(sents):
    text_output = ""

    for _s in sents:
        s = ' '.join(_s.split(), )
        text_output += s + "\n\n"

    return text_output


def mode_listmark(sents):
    text_output = ""

    for _s in sents:
        s = ' '.join(_s.split(), )
        text_output += "- " + s + "\n\n"

    return text_output
