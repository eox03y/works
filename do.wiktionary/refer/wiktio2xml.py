#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2010 Bruno Coudoin
#
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, see <http://www.gnu.org/licenses/>.
#

from xml.sax import parse
from xml.sax.handler import ContentHandler
from xml.sax.handler import ErrorHandler
import sys
import re
import os

from optparse import OptionParser

import wiktio
from wiktio import Wiktio

debug = False

class WikiErrorHandler(ErrorHandler):
    def error(self, exception):
        print exception

    def fatalError(self, exception):
        print exception

    def warning(self, exception):
        print exception

class WikiHandler(ContentHandler):

    def __init__ (self, searchWords, locale, _wiktio, verbose):

        self.searchWords= searchWords;
        self.locale = locale
        self.wiktio = _wiktio
        self.verbose = verbose

        self.isPageElement = False

        self.isTitleElement = False
        self.titleContent = u""

        self.isTextElement = False
        self.textContent = u""

        self.lilevel = 0

    def startElement(self, name, attrs):

        if name == 'page':
            self.isPageElement = True
        elif name == 'title':
            self.isTitleElement = True
            self.titleContent = ""
        elif name == 'text':
            self.isTextElement = True
            self.textContent = ""

        self.genders = {
            "{{m}}": u"masculin",
            "{{f}}": u"féminin",
            "{{mf}}": u"masculin et féminin"
            }

        self.wordTypes = {
            u"{{-nom-.*}}": u"nom",
            u"{{-nom-pr.*}}": u"nom propre",
            u"{{-verb.*}}": u"verbe",
            u"{-pronom-.*}": u"pronom",
            u"{-adj-.*}}": u"adjectif",
            u"{-adv-.*}}": u"adverbe",
            u"{-art-.*}}": u"article",
            u"{-conj-.*}}": u"conjunction",
            u"{-prèp-.*}}": u"préposition",
            u"{-post-.*}}": u"postposition"
            }

        # This is the list of word types we don't want to keep
        self.wordSkipTypes = [
            "{{-flex-verb-"
            ]

        self.wordSubTypes = {
            "{{1ergroupe}}": "1er groupe",
            "{{2egroupe}}": "2eme groupe",
            "{{3egroupe}}": "3eme groupe",
            }

        # Some content in wiktionary is obvioulsy not appropriate
        # for children. This contains a list of regexp.
        self.filterContent = [ ur"de sade",
                               ur"pénis",
                               ur"homosexuel",
                               ur"vagin"]

        # These definitions will always be skipped
        self.filterDefinitionType = [ ur"{{vulg[^}]*}}",
                                      ur"{{injur[^}]*}}",
                                      ur"{{sexe[^}]*}}",
                                      ur"{{sexua[^}]*}}",
                                      ur"coït",
                                      ur"argot"]

        # These definitions will be skipped only if not in the first
        # sense found
        self.filterSecondDefinitionType = [
                                      ur"{{dés[^}]*}}",
                                      ur"{{vx[^}]*}}",
                                      ur"{{métonymie[^}]*}}",
                                      ur"{{familier[^}]*}}",
                                      ur"{{hérald[^}]*}}",
                                      ur"{{botan[^}]*}}",
                                      ur"{{zool[^}]*}}",
                                      ur"{{polit[^}]*}",
                                      ur"{{péj[^}]*}}",
                                      ur"{{oeno[^}]*}}",
                                      ur"{{litt[^}]*}}",
#                                      ur"{{par ext[^}]*}}",
                                      ur"{{figuré[^}]*}}"
                                      ]

    def endElement(self, name):

        if name == 'page':
            self.isPageElement= False
            if 1 or self.titleContent in self.searchWords:
                print "[T]", self.titleContent 
                print "[C]", self.textContent 
                word = self.parseText()
                if word and word.name:
                    print "[W]", word.name 
                    self.wiktio.addWord(word)

            self.titleContent = ""
            self.textContent = ""

        elif name == 'title':
            self.isTitleElement= False
        elif name == 'text':
            self.isTextElement = False

    def characters (self, ch):
        if self.isTitleElement:
            self.titleContent += ch
        elif self.isTextElement:
            self.textContent += ch


    # Manages bullets and numbered lists
    # mediawiki specification:
    # Bulleted: *
    # Numbered: #
    # Indent with no marking: :
    # Definition list: ;
    # Notes:
    # These may be combined at the start of the line to create
    # nested lists, e.g. *** to give a bulleted list three levels
    # deep, or **# to have a numbered list within two-levels of
    # bulleted list nesting.
    #
    # html specification:
    # Bulleted: <ul> [<li> </li>]+ </ul>
    # Numbered: <ol> [<li> </li>]+ </ol>
    # Notes:
    # These may be nested.
    #
    # We keep the level of indentation to close in:
    # self.lilevel
    #
    # Returns a list [text, level, numbered]
    # numbered = True if this is a numbered list
    #
    def indents2xml(self, text, asText):
        numbered = False
        result = re.search(r"^[ ]*[*#:;]+[ ]*", text)
        if not result:
            self.lilevel = 0
            return [text, self.lilevel, numbered]

        indent = result.group(0).rstrip()
        self.lilevel = len(indent)
        text = text[result.end():]

        if asText:
            return [text, self.lilevel, numbered]

        if indent[-1:] == "#":
            numbered = True

        return [text, self.lilevel, numbered]

    # Replaces '''xx''' and ''xx'' from the given text
    # with openXml xx closeXml
    def quote2xml(self, quote, openXml, closeXml, text):
        index = 0
        while index >= 0:
            index = text.find(quote)
            index2 = text.find(quote, index + len(quote))
            if index >= 0 and index2 >=0:
                text = text.replace(quote, openXml, 1)
                text = text.replace(quote, closeXml, 1)
            else:
                return text
        return text

    # Replace standard Wiki tags to XML
    # Returns a list [text, level, numbered]
    # numbered = True if this is a numbered list
    def wiki2xml(self, text, asText):

        text = re.sub(r"{{[-\)\(]}}", "", text)
        text = re.sub(r"\[\[\w+:\w+\]\]", "", text)
        text = re.sub(r"{{\(\|(.*)}}", r"", text)
        if text == "":
            return self.indents2xml(text, asText)

        [text, level, numbered] = self.indents2xml(text, asText)
        text = re.sub(ur"{{par ext[^}]*}}", ur"(Par extension)", text)
        text = re.sub(ur"{{figuré[^}]*}}", ur"(Figuré)", text)
        text = re.sub(ur"{{w\|([^}]+)}}", ur"<i>\1</i>", text)
        text = re.sub(ur"{{source\|([^}]+)}}", ur"- (\1)", text)

        # Remove all unrecognized wiki tags
        text = re.sub(r"{{[^}]+}}", "", text)

        # bold
        text = self.quote2xml("'''", "<b>", "</b>", text)
        # italic
        text = self.quote2xml("''", "<i>", "</i>", text)

        # Get rid of hyperlinks
        while text.find("[[") != -1:
            start = text.find("[[")
            stop = text.find("]]")
            pipe = text.find("|", start, stop)
            if pipe == -1:
                text = text.replace("[[", "", 1)
                text = text.replace("]]", "", 1)
            else:
                text = text[:start] + text[pipe+1:]
                text = text.replace("]]", "", 1)

        return [text, level, numbered]

    # Wikipedia text content is interpreted and transformed in XML
    def parseText(self):
        if self.verbose:
            print "Processing " + self.titleContent
        inWord = wiktio.Word()

        state = Wiktio.SKIP

        wordType = ""
        wordSubType = ""
        filterIndent = ""
        gender = ""

        # Append an end of text marker, it forces the end of the definition
        self.textContent += "\n{{-EndOfTest-}}"

        # Remove html comment (multilines)
        self.textContent = re.sub(r"<!--[^>]*-->", "",
                                  self.textContent, re.M)

        definition = wiktio.Definition()
        inWord.addDefinition(definition)
        concat = ""
        for l in self.textContent.splitlines():
            l = concat + l
            concat = ""
            next = False

            if debug: print "   l:" + l + ":"
            if re.search(r"<[^>]+$", l):
                # Wiki uses a trick to format text area by ending in uncomplete
                # html tags. In this case, we concat this line with the next one
                # before processing it
                concat = l
                continue

            # Determine the section of the document we are in
            #if l.startswith("'''" + self.titleContent + "'''"):
            if l.startswith("==English=="):    
                inWord.setName(self.titleContent)
                # Get rid of the word, we don't want it in the definition
                l = re.sub(r"'''.*'''[ ]*(.*)", r"\1", l)
                # Get rid of non wiki tags
                l = re.sub(r'}}[^}]+{{', r'}} {{', l)
                state = Wiktio.DEFINITION

                for wt in self.genders.keys():
                    if re.search(wt, l):
                        gender = self.genders[wt]
                        definition.setGender(gender)
                        break

                for wt in self.wordSubTypes.keys():
                    if re.search(wt, l):
                        wordSubType = self.wordSubTypes[wt]
                        definition.setSubType(wordSubType)
                        break

                definition.addDescription("", 0, False)
                continue

            elif l == "{{-anagr-}}":
                state = Wiktio.ANAGRAM
            elif l == "{{-syn-}}":
                state = Wiktio.SYNONYM
            elif l == "{{-ant-}}":
                state = Wiktio.ANTONYM
            elif l == "{{-hyper-}}":
                state = Wiktio.HYPERONYM
            elif l == "{{-hypo-}}":
                state = Wiktio.HYPONYM
            elif l == "{{-pron-}}":
                state = Wiktio.PRON
            elif l == "{{-note-}}":
                state = Wiktio.SKIP
            elif l == "{{-apr-}}":
                state = Wiktio.SKIP
            elif l == "{{-drv-}}":
                state = Wiktio.SKIP
            elif l == "{{-exp-}}":
                state = Wiktio.SKIP
            elif l == "{{-trad-}}":
                state = Wiktio.SKIP
            elif l == "{{-voc-}}":
                state = Wiktio.SKIP
            elif l == "{{-voir-}}":
                state = Wiktio.SKIP
            elif l == u"{{-réf-}}":
                state = Wiktio.SKIP
            elif re.search(r"{{-.*-.*}}", l):
                if not definition.rootDescription.isEmpty():
                    if debug: print "  new definition:" + l + ":"
                    # Next definition
                    filterIndent = ""
                    definition = wiktio.Definition()
                    inWord.addDefinition(definition)
                state = Wiktio.SKIP

            # Are we still in the correct language section
            # We assume the correct language is ahead
            lang = re.match(r"==[ ]+{{=([a-z]+)=}}[ ]+==", l)
            if lang and lang.group(1) != None and lang.group(1) != self.locale:
                return inWord

            # Image
            if definition and re.match(ur"\[\[Image:", l):
                text = re.sub(ur"\[\[Image:([^|}\]]+).*", r"\1", l)
                definition.add(Wiktio.IMAGE, text)
                continue

            for wt in self.wordTypes.keys():
                if re.search(wt, l):
                    wordType = self.wordTypes[wt]
                    definition.setType(wordType)
                    break

            for wt in self.wordSkipTypes:
                if re.search(wt, l):
                    definition.filtered = True
                    break

            if state == Wiktio.SKIP:
                continue

            for filter in self.filterContent:
                if re.search(filter, l, re.I):
                    definition.filtered = True
                    break

            if filterIndent != "":
                # We are filtering, check this line is
                # at a lower indentation level
                result = re.search(r"^[ ]*[*#:;]+[ ]*", l)
                if result:
                    if len(result.group(0).rstrip()) > len(filterIndent):
                        next = True
                    else:
                        filterIndent = ""
                else:
                    filterIndent = ""


            # Filter meanings having really bad words in them
            for filter in self.filterDefinitionType:
                if re.search(filter, l, re.I):
                    result = re.search(r"^[ ]*[*#:;]+[ ]*", l)
                    if result:
                        # Keep the indent level for which we filter
                        filterIndent = result.group(0).rstrip()
                    next = True
                    break

            # We already found a meaning for this word, we pick
            # other senses restrictively
            if not definition.rootDescription.isEmpty():
                for filter in self.filterSecondDefinitionType:
                    if re.search(filter, l, re.I):
                        result = re.search(r"^[ ]*[*#:;]+[ ]*", l)
                        if result:
                            # Keep the indent level for which we filter
                            filterIndent = result.group(0).rstrip()
                        next = True
                        break

            if next:
                continue

            # Categories
            if re.match(ur"\[\[Catégorie:", l):
                text = re.sub(ur"\[\[Catégorie:([^|}\]]+).*", r"\1", l)
                definition.add(Wiktio.CATEGORY, text)
                continue

            if state == Wiktio.DEFINITION:
                [text, level, numbered] = self.wiki2xml(l, False)
                definition.addDescription(text, level, numbered)
            elif state == Wiktio.PRON:
                file = re.subn(r".*audio=([^|}]+).*", r"\1", l)
                if file[1] == 1:
                    definition.add(state, file[0])
            else:
                if len(l) > 0:
                    definition.add(state, self.wiki2xml(l, True)[0])

        return inWord

# Set UTF-8 stdout in case of the user piping our output
#reload(sys)
#sys.setdefaultencoding('utf-8')
import codecs
sys.stdout = codecs.getwriter('utf-8')(sys.stdout)

usage = "usage: %prog [options] wiktionary_dump.xml word_list.txt"
parser = OptionParser(usage=usage)
parser.add_option("-o", "--output", dest="output",
                  help="write result to file or directory")
parser.add_option("-q", "--quiet",
                  action="store_false", dest="verbose", default=True,
                  help="don't print in progress messages to stdout")
parser.add_option("-d", "--debug",
                  action="store_true", dest="debug", default=False,
                  help="print debug traces to stdout")
parser.add_option("-s", "--site",
                  action="store_true", dest="site", default=False,
                  help="Creates a web site")
(options, args) = parser.parse_args()

if len(sys.argv) < 3:
    parser.print_help()
    sys.exit()

wikiFile = sys.argv[1]
wordsFile = sys.argv[2]

'''
if options.site:
    if not os.path.isdir(options.output):
        print "ERROR: There must me a directory named " + options.output
        sys.exit(1)
else:
    if os.path.exists(options.output):
        print "ERROR: There is already a file named " + options.output
        sys.exit(1)
'''

# Import the list of words
#f = open(wordsFile, "r")
words = []
#words = [w.rstrip() for w in f.readlines()]
#f.close()

_wiktio = wiktio.Wiktio()

parse(wikiFile, WikiHandler(words, 'en', _wiktio, options.verbose), WikiErrorHandler())

debug = options.debug

_wiktio.dump2html("abcd.html")
'''
if options.site:
    _wiktio.dump2htmlSite(options.output)
else:
    _wiktio.dump2html(options.output)
'''
