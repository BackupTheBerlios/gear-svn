import sys, string
from xml.sax import handler, make_parser

class MySaxDocumentHandler(handler.ContentHandler):             # [1]
    def __init__(self, outfile):                                # [2]
        self.outfile = outfile
        self.level = 0
        self.inInterest = 0
        self.interestData = []
        self.interestList = []
    def get_interestList(self):
        return self.interestList
    def set_interestList(self, interestList):
        self.interestList = interestList
    def startDocument(self):                                    # [3]
        print "--------  Document Start --------"
    def endDocument(self):                                      # [4]
        print "--------  Document End --------"
    def startElement(self, name, attrs):                        # [5]
        self.level += 1
        self.printLevel()
        self.outfile.write('Element: %s\n' % name)
        self.level += 2
        for attrName in attrs.keys():                           # [6]
            self.printLevel()
            self.outfile.write('Attribute -- Name: %s  Value: %s\n' % \
                (attrName, attrs.get(attrName)))
        self.level -= 2
        if name == 'interest':
            self.inInterest = 1
            self.interestData = []
    def endElement(self, name):                                 # [7]
        if name == 'interest':
            self.inInterest = 0
            interest = string.join(self.interestData)
            self.printLevel()
            self.outfile.write('Interest: ')
            self.outfile.write(interest)
            self.outfile.write('\n')
            self.interestList.append(interest)
        self.level -= 1
    def characters(self, chrs):                                 # [8]
        if self.inInterest:
            self.interestData.append(chrs)
    def printLevel(self):                                       # [9]
        for idx in range(self.level):
            self.outfile.write('  ')

def test(inFileName):
    outFile = sys.stdout
    # Create an instance of the Handler.
    handler = MySaxDocumentHandler(outFile)
    # Create an instance of the parser.
    parser = make_parser()
    # Set the content handler.
    parser.setContentHandler(handler)
    inFile = open(inFileName, 'r')
    # Start the parse.
    parser.parse(inFile)                                        # [10]
    # Alternatively, we could directly pass in the file name.
    #parser.parse(inFileName)
    inFile.close()
    # Print out a list of interests.
    interestList = handler.get_interestList()
    print 'Interests:'
    for interest in interestList:
        print '    %s' % (interest, )

def main():
    #args = sys.argv[1:]
    #if len(args) != 1:
    #    print 'usage: python test.py infile.xml'
    #    sys.exit(-1)
    test('people.xml')

if __name__ == '__main__':
    main()