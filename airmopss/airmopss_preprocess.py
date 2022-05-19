

def get_stop_sentences():
    stops = [ s for l in _stop_sentences for s in l ]
    return stops

stop_sentences_reuters = [
    "Register now for FREE unlimited access to Reuters.com Register",
    "Our Standards: The Thomson Reuters Trust Principles.",
]
stop_sentences_any = [
    "Advertisement",
    "Get in touch",
    "Go to https://apnews.com/hub/russia-ukraine for more coverage"
]

_stop_sentence_patterns = [
    "Other {{#cta}} {{text}} {{/cta}} Email address Please enter a valid email address Please enter your email address Set a reminder Sorry we couldn't set a reminder for you this time. Please try again later. . To find out what personal data we collect and how we use it, view our We will send you a maximum of two emails in. To find out what personal data we collect and how we use it, view our Privacy Policy . If you have any questions about contributing, please We will be in touch to remind you to contribute. Look out for a message in your inbox in. If you have any questions about contributing, please contact us {{/paragraphs}}{{#choiceCards}}{{/choiceCards}}",
    "{{#choiceCards}}",
    "{{topLeft}} {{bottomLeft}} {{topRight}} {{bottomRight}} {{/goalExceededMarkerPercentage}} {{#goalExceededMarkerPercentage}}{{/goalExceededMarkerPercentage}} {{heading}} {{#paragraphs}} {{#ticker}}{{/ticker}}{{#paragraphs}} {{.}} {{/paragraphs}} {{highlightedText}}",
    "Reporting by john Chalmers, Gabriela Baczynska",
    "Reporting by Reuters; editing by Guy Faulconbridge",
    "Reporting by Leah Douglas; Editing by Alison Williams and David Gregorio",
    "Reporting by Stanley Widianto and Angie Teo Writing by Ed Davies Editing by Kanupriya Kapoor",
    "Reporting by Nidhi Verma; Editing by Aditya Soni",
    "Reporting by Phuong Nguyen Editing by Ed Davies",
    "Reporting by Jarrett Renshaw on aboard Afir Force One and Trevor Hunnicutt in Washington; Additional reporting by Alexandra Alper; Editing by Heather Timmons, Mary Milliken and Cynthia Osterman"

]
_stop_sentences = [
    stop_sentences_reuters,
    stop_sentences_any
]

stop_sentences = get_stop_sentences()

def article_to_list(txt):
    return txt.split('\n')

def remove_stop_sentences(txt):
    l_txt = article_to_list(txt)
    return [s for s in l_txt if s not in stop_sentences]

def list_to_text(l):
    return "\n".join(l)

def clean_text(txt):
    return list_to_text(remove_stop_sentences(txt))


def tokens_to_list_unique(tokens):
    l = [" ".join([str(elt) for elt in token]).strip() for token in tokens]
    l = list(dict.fromkeys(l))
    return  l