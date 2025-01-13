import re
import copy
from collections import defaultdict
from semperpy.plot.plotdirective import PlotDirective
from semperpy.plot.namegenerator import NameGenerator
from semperpy.plot.mplib.layout import Layout
from semperpy.plot.mplib.titles import MainTitle

class Document(PlotDirective):

    filenames_ = defaultdict(int)
    used_ = set()
    silent_ = False

    def __init__(self,*args,**kargs):
        super(Document,self).__init__(*args,**kargs)
        self.checkLanguage()
        self.checkDataType()
        self.distribute()
        self.layout_ = Layout(self['layout'],self['size'],interactive=self['interactive'],layout_tiles=self['layout_tiles'])
        collection = []
        i = 1
        for document in self.documents_:
            document.title_ = ''
            for plot in document['plot']:
                if not Document.silent_:
                    print("Retrieving data...",i)
                plot.doRetrieve()
                subplot = self.layout_()
                if not Document.silent_:
                    print("Plotting data...",i)
#                print('calling dodraw')
                plot.dodraw(self.layout_,subplot)
#                print('calling plotText')
                document.plotText(self.layout_,subplot,plot)
                collection.append(plot)
                if self.layout_.fullPage():
#                    print('calling plotTitle')
                    document.plotTitle(self.layout_,subplot,collection)
#                    print('calling layout_.draw')
                    self.layout_.draw(filename=document.filename(collection))
                    collection = []
                i += 1
        if self.layout_.remaining():
            print('calling plotTitle-2')
            document.plotTitle(self.layout_,subplot,collection)
            print('calling layout_.draw-2')
            self.layout_.draw(filename=document.filename(collection))
        if not Document.silent_:
            print("Complete.")

    def checkDataType(self):
        theType = set()
        if 'plotdata' in self:
            theType.add(type(self['plotdata']))
        if 'plot' in self:
            for plot in self['plot']:
                if 'plotdata' in plot:
                    theType.add(type(plot['plotdata']))
                if 'curve' in plot:
                    for curve in plot['curve']:
                        if 'plotdata' in curve:
                            theType.add(type(curve['plotdata']))
        if len(theType) != 1:
            raise ValueError('The data type to be plotted has to be specified at least at one level using the "plotdata" keyword and needs to be consistent between all the graphical elements')
        theType = theType.pop()
        if not 'plotdata' in self:
            self['plotdata'] = theType()
            self['plotdata'].checkLanguage()
        if 'plot' in self:
            for plot in self['plot']:
                if not 'plotdata' in plot:
                    plot['plotdata'] = theType()
                    plot['plotdata'].checkLanguage()
                if 'curve' in plot:
                    for curve in plot['curve']:
                        if not 'plotdata' in curve:
                            curve['plotdata'] = theType()
                            curve['plotdata'].checkLanguage()

    def distribute(self):
        length = set()
        distributed = []
        for plot in self['plot']:
            all = self.data.distribute(self,plot.me())
            distributed.append(all)
            length.add(len(all))
        if len(length) > 1:
            raise ValueError('Different plot types in this document generate a different number of combinations of keywords, this cannot be handled in the same document')
        documents = []
        all = distributed[0]
        for one in all:
            d = copy.copy(self)
            d.data = one
            documents.append(d)
        self.documents_ = documents
        for document in documents:
            plots = []
            for plot in document['plot']:
                pl = copy.copy(plot)
                keys = pl.inherit_from(document,exclude='filename')
                # semperpy/plot/plot.py distribute()
                pl.distribute() #<- causes 11 curves
                plots.append(pl)
                pl.finalise()
            document['plot'] = plots
        #if not Document.silent_:
        #    for d in documents:
        #        print d
        #    print

    def dodraw(self):
        self.layout_ = Layout(self['layout'],self['size'],interactive=self['interactive'])
        collection = []
        i = 1
        while len(self.documents_) > 0:
            document = self.documents_.pop(0)
            document.title_ = ''
            for plot in document['plot']:
                subplot = self.layout_()
                plot.dodraw(self.layout_,subplot)
                document.plotText(self.layout_,subplot,plot)
                collection.append(plot)
                if self.layout_.fullPage():
                    document.plotTitle(self.layout_,subplot,collection)
                    self.layout_.draw(filename=document.filename(collection))
                    collection = []
            del(document)
        if self.layout_.remaining():
            document.plotTitle(self.layout_,subplot,collection)
            self.layout_.draw(filename=document.filename(collection))
        if not Document.silent_:
            print("Complete.")

    def filename(self,plots):
        if self['interactive']:
            return ''
        generator = self.nameGenerator()
        info = self.data.mergeDirective([ x.createTitleInfo() for x in plots ],overwrite=True)
        filename = self['output']
        filename = re.sub('<count>','1count1',filename)
        filename = generator(plots,filename,info)
        self.filenames_[filename] += 1
        count = '%03d' % self.filenames_[filename]
        filename = re.sub('1count1',count,filename)
        if filename in self.used_:
            raise IOError('The document generated a file name which would ovewrite an existing file, please add variables in the name or use the keyword <count>')
        self.used_.add(filename)
        return filename

    def nameGenerator(self):
        return NameGenerator()

    def plotText(self,layout,subplot,plot):
        if self['has_title']:
            plot['has_title'] = False
            title,legends = plot.createTextTemplates()
            if 'title' in self:
                title = self['title']
            if len(title) > len(self.title_):
                self.title_ = title
            plot.plotText(self,layout,subplot,main_title=title,legends=legends)
        else:
            plot.plotText(self,layout,subplot)

    def plotTitle(self,layout,subplot,plots):
        if self['has_title']:
            title = self.title_
            if 'title' in self:
                title = '\n'.join(self['title'])
            info = self.data.mergeDirective([ x.createTitleInfo() for x in plots ],overwrite = True)
            text = self.data.createTextTemplate()
            title = text.processText(title,info,section='title')
            MainTitle()(layout,subplot,title,self['title_font'])

document = Document
