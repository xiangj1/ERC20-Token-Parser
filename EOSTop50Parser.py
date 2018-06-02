from html.parser import HTMLParser

class MyHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.round = 0
        self.isTd = 0

    def handle_starttag(self, tag, attrs):
        if(tag == 'td'):
            self.isTd = 1

    def handle_endtag(self, tag):
        if(tag == 'td'):
            self.isTd = 0

    def handle_data(self, data):
        if(self.isTd == 1):
            self.round += 1
            if(self.round < 4):
                print(data, end=",")
            else:
                print(data, end="\n")
                self.round = 0

parser = MyHTMLParser()

info_page = open('test.html', 'r').read()
parser.feed(info_page)