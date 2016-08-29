import sublime
import sublime_plugin
import re
import json
from os.path import basename, splitext
from lxml import etree

class BaseIndentCommand(sublime_plugin.TextCommand):
  
    def __init__(self, view):
        self.view = view
        self.language = self.get_language()

    def get_language(self):
        syntax = self.view.settings().get('syntax')
        language = splitext(basename(syntax))[0].lower() if syntax is not None else "plain text"
        return language

    def check_enabled(self, lang):
        return True

    def is_enabled(self):
        """
        Enables or disables the 'indent' command. Command will be disabled if
        there are currently no text selections and current file is not 'XML' or
        'Plain Text'. This helps clarify to the user about when the command can
        be executed, especially useful for UI controls.
        """
        if self.view is None:
            return False

        return self.check_enabled(self.get_language())

    def run(self, edit):
        """
        Main plugin logic for the 'indent' command.
        """
        view = self.view
        regions = view.sel()
        # if there are more than 1 region or region one and it's not empty
        if len(regions) > 1 or not regions[0].empty():
            for region in view.sel():
                if not region.empty():
                    s = view.substr(region).strip()
                    s = self.indent(s)
                    if s:
                        view.replace(edit, region, s)
        else:  # format all text
            alltextreg = sublime.Region(0, view.size())
            s = view.substr(alltextreg).strip()
            s = self.indent(s)
            if s:
                view.replace(edit, alltextreg, s)


class AutoIndentCommand(BaseIndentCommand):

    def get_text_type(self, s):
        language = self.language
        if language == 'xml':
            return 'xml'
        if language == 'json':
            return 'json'
        if language == 'plain text' and s:
            if s[0] == '<':
                return 'xml'
            if s[0] == '{' or s[0] == '[':
                return 'json'

        return 'notsupported'

    def indent(self, s):
        text_type = self.get_text_type(s)
        if text_type == 'xml':
            command = IndentXmlCommand(self.view)
        if text_type == 'json':
            command = IndentJsonCommand(self.view)
        if text_type == 'notsupported':
            return s

        return command.indent(s)

    def check_enabled(self, lang):
        return True


class IndentXmlCommand(BaseIndentCommand):

    def indent(self, s):
        # figure out encoding
        idx = re.search(r"[\r\n]", s)
        idx = idx.start() if idx is not None else None
        utfEncoded = s[:idx].encode("utf-8")
        encoding = "utf-8"
        encodingMatch = re.match(b"<\\?.*encoding=['\"](.*?)['\"].*\\?>", utfEncoded)
        if encodingMatch:
            encoding = encodingMatch.group(1).decode("utf-8").lower()
        utfEncoded = None

        s = s.encode(encoding)
        xmlheader = True if re.match(br"<\?.*\?>", s) is not None else False
        try:
            parser = etree.XMLParser(remove_blank_text=True, strip_cdata=False)
            #xml = etree.fromstring(s, parser)
            #s = self.prettify(xml)
            s = etree.tostring(etree.fromstring(s, parser), pretty_print=True, xml_declaration=xmlheader, encoding=encoding).decode(encoding)
        except etree.LxmlError as err:
            message = "Invalid XML: %s" % (err)
            sublime.status_message(message)
            return
        
        # change default two space indent to tab, respect multiline text nodes and CDATA
        isCdata = False
        L = []
        startCdata = re.compile(r".*<!\[CDATA\[")
        endCdata = re.compile(r".*\]\]>")
        # leading pairs of spaces, only if on a line beginning with an xml node, NOT a multiline text node
        leadingSpace = re.compile("  (?= *<)")
        for line in s.splitlines():
            if isCdata:
                L.append(line)
                isCdata = not endCdata.match(line)
            else:
                L.append(leadingSpace.sub("\t", line))
                isCdata = startCdata.match(line)
            
        s = "\n".join(L)
        return s

    """
    # example of pretty print using an XSLT transform
    def prettify(self, someXML):
        #for more on lxml/XSLT see: http://lxml.de/xpathxslt.html#xslt-result-objects
        xslt_tree = etree.XML('''\
            <!-- XSLT taken from Comment 4 by Michael Kay found here:
            http://www.dpawson.co.uk/xsl/sect2/pretty.html#d8621e19 -->
            <xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
                <xsl:output method="xml" indent="yes" encoding="UTF-8" omit-xml-declaration="yes"/>
                <xsl:strip-space elements="*"/>
                <xsl:template match="/">
                    <xsl:copy-of select="."/>
                </xsl:template>
            </xsl:stylesheet>''')
        transform = etree.XSLT(xslt_tree)
        result = transform(someXML)
        return str(result)
    """

    def check_enabled(self, language):
        return ((language == "xml") or (language == "plain text"))


class IndentJsonCommand(BaseIndentCommand):

    def check_enabled(self, language):
        return ((language == "json") or (language == "plain text"))

    def indent(self, s):
        parsed = json.loads(s)
        return json.dumps(parsed, sort_keys=True, indent=4, separators=(',', ': '), ensure_ascii=False)
