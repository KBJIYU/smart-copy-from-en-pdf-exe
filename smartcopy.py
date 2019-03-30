# -*- coding: UTF-8 -*-

######################
### SMART COPY      ##
### AUTHOR: KBJIYU  ##
### VERSION: v1.0.0 ##
######################

import re
import sys
import time
import py3compat
import win32clipboard


def split_sentence_by_br(text):
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


def spy_on_clipboard(modify_func):
    """ Loops in spying clipboard's action, then modify  """
    def get_clipboard_text():
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
            return text

    def set_clipboard_text(wanted_data):
        win32clipboard.OpenClipboard()
        # win32clipboard.EmptyClipboard()
        try:
            win32clipboard.SetClipboardText(
                wanted_data, win32clipboard.CF_TEXT)
        except:
            print(">> [WARN] Can't set clipborad's data.")
        finally:
            win32clipboard.CloseClipboard()

    # init
    try:
        last = get_clipboard_text()
    except:
        last = None

    while 1:
        current = get_clipboard_text()
        if current and last != current:
            t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            print(
                ">> [INFO][{}] Smartcopy is modifying your clipborad's data.".format(t))
            try:
                modified = modify_func(current)
                print('success modified')
            except:
                modified = current
                print('failed to modify')
            finally:
                set_clipboard_text(modified)
                last = modified

        time.sleep(0.1)


if __name__ == '__main__':
    try:
        start = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print(">> [INFO][{}] WELCOME TO SMARTCOPY v1.0.0 ^_^".format(start))
        print(">> [INFO][{}] Smartcopy is running!".format(start))
        spy_on_clipboard(split_sentence_by_br)
    except KeyboardInterrupt:
        end = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print(">> [INFO][{}] Smartcopy is Exiting. {}".format(end, sys.stderr))
        sys.exit(0)
