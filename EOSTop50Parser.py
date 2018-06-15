from html.parser import HTMLParser

class TokenTop50Parser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.round = 0
        self.isTd = 0
        self.file = open("~/TokenData/EOSdata.json", "w+")
        self.file.write("[")

    def handle_starttag(self, tag, attrs):
        if(tag == 'td'):
            self.isTd = 1

    def handle_endtag(self, tag):
        if(tag == 'td'):
            self.isTd = 0
        elif(tag == 'table'):
            self.file.write("{\"status\":\"eof\"}]")

    def handle_data(self, data):
        if(self.isTd == 1):
            self.round += 1
            if(self.round == 1):
                self.file.write("{\"rank\":\"" + data + "\",")
            elif(self.round == 2):
                self.file.write("\"address\":\"" + data + "\",")
            elif(self.round == 3):
                self.file.write("\"amount\":\"" + data + "\",")
            elif(self.round == 4):
                self.file.write("\"percentage\":\"" + data + "\"},")
                self.round = 0
            

parser = TokenTop50Parser()

info_page = open('test.html', 'r').read()
parser.feed(info_page)