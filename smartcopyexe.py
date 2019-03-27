######################
### SMART COPY      ##
### AUTHOR: KBJIYU  ##
### VERSION: v1.0.0 ##
######################


import sys
import time
import nltk
import win32clipboard


def sentence_split_by_br(text):
    text_output = ""
    sents = nltk.sent_tokenize(text)

    for _s in sents:
        s = ' '.join(_s.split(), )
        text_output += s + "\n\n"

    return text_output


def spy_on_clipboard(modify_func):
    def get_clipboard_data():
        # get clipboard data
        win32clipboard.OpenClipboard()
        try:
            data = win32clipboard.GetClipboardData()
            return data
        except TypeError:
            return None
        finally:
            win32clipboard.CloseClipboard()

    def set_clipboard_data(wanted_data):
        # set clipboard data
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardText(wanted_data)
        win32clipboard.CloseClipboard()

    # init
    try:
        last = get_clipboard_data()
    except:
        last = None

    while 1:
        current = get_clipboard_data()
        if current and last != current:
            print(">> modifying clipborad's data.")
            modified = modify_func(current)
            set_clipboard_data(modified)
            last = modified

        time.sleep(0.1)


if __name__ == '__main__':
    try:
        print(">> smartcopy is running!")
        spy_on_clipboard(sentence_split_by_br)
    except KeyboardInterrupt:
        print(">>", sys.stderr, "\nExiting by user request.\n")
        sys.exit(0)
