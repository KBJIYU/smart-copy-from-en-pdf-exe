# -*- coding: UTF-8 -*-

######################
### SMART COPY      ##
### AUTHOR: KBJIYU  ##
### VERSION: v1.0.0 ##
######################

import re
import sys
import time
import logging
import py3compat
import win32clipboard

logging.basicConfig(level=logging.DEBUG,
                    format='[%(asctime)s][%(levelname)s]: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')


def split_sentence_by_br(text):
    """ Make your text easy to read and to translate.

        Args:
            text(str):
                target dirty text.

        Returns:
            text_output(str):
                formatted output.

    """
    def purify_text(text):
        """ Remove emoji. """
        emoji_pattern = re.compile("["
                                   u"\U0001F600-\U0001F64F"  # emoticons
                                   u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                   u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                   u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                   "]+", flags=re.UNICODE)

        return emoji_pattern.sub(r'', text)

    text_output = ""

    text = purify_text(text)
    sents = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', text)
    # sents = nltk.sent_tokenize(text) # can't fix the pyinstaller problem with it.

    for _s in sents:
        s = ' '.join(_s.split(), )
        text_output += s + "\n\n"

    return text_output


def smartcopy_spy(modify_func):
    """ Loops in spying clipboard's action, then modify

        Args:
            modify_func (func):  The middleware function to modify your text.

    """

    def get_clipboard_text():
        """ Try to get clipboard's text

            Returns:
                text(str):
                    string: data from clipboard

        """

        win32clipboard.OpenClipboard()
        try:
            text = win32clipboard.GetClipboardData(
                win32clipboard.CF_UNICODETEXT)
        except (TypeError, win32clipboard.error):
            try:
                text = win32clipboard.GetClipboardData(win32clipboard.CF_TEXT)
                text = py3compat.cast_unicode(text, py3compat.DEFAULT_ENCODING)
            except (TypeError, win32clipboard.error):
                text = None
        finally:
            win32clipboard.CloseClipboard()
            if text:
                return text
            else:
                raise TypeError(
                    "Can't get clipboard's data, might be wrong encode type.")

    def set_clipboard_text(new_text):
        """ Try to get clipboard's text

            Args:
                new_text(str):
                    data for updating clipboard.

        """

        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        try:
            win32clipboard.SetClipboardText(new_text)
            logging.info(
                "Successfully updated your clipborad's data.")
            win32clipboard.CloseClipboard()
        except:
            logging.warn(
                "Sorry we can't update your clipborad, you SHOULD copy only UTF-8 format text.")
            win32clipboard.CloseClipboard()
            raise TypeError(
                "Can't set clipboard's data, might be wrong encode type.")

    # init
    try:
        last = get_clipboard_text()
    except TypeError:
        last = ''

    # main flow
    while True:
        try:
            current = get_clipboard_text()
            if current and (current != last):
                try:
                    modified = modify_func(current)
                    logging.info(
                        "Successfully modified your clipborad's data.")
                except:
                    modified = current
                    logging.info("Failed to modify your clipborad's data.")

                if modified != current:
                    try:
                        set_clipboard_text(modified)
                        last = modified
                    except:
                        set_clipboard_text(current)
                        last = current
                else:
                    last = current
        except TypeError:
            pass

        time.sleep(0.1)


if __name__ == '__main__':
    print(""" \n
            WELCOME TO SMARTCOPY v1.0.0 ^_^
            -------------------------------
            > Author: github@kbjiyu
            > Info: https://goo.gl/Pnkazc
            ------------------------------- \n\n"""
          )

    logging.info("Smartcopy is running!")

    try:
        smartcopy_spy(split_sentence_by_br)
    except KeyboardInterrupt:
        logging.info("Smartcopy is Exiting. {}".format(sys.stderr))
        sys.exit(0)
    except:
        logging.error(
            "Something not excepted happened, please try again, or report it!")
        print(""" \n
            -------------------------------
            > Author: github@kbjiyu
            > Info: https://goo.gl/Pnkazc
            ------------------------------- \n"""
              )
        print("> press any key to exit.")
        input()
