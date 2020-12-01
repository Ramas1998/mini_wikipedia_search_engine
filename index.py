import xml.sax
import sys
import logging
import time
import ast
import re
#import Stemmer
import glob
import heapq
import os
import importlib
#from itertools import imap
from operator import itemgetter
#from XMLParser import WikiXmlHandler,Page
from nltk.tokenize import RegexpTokenizer, WhitespaceTokenizer
from nltk.corpus import stopwords
from nltk import PorterStemmer
from string import digits

sno = PorterStemmer()
#stemmer = Stemmer.Stemmer('english')
INDEXFILE=None
language = "english"
stop_words = set(stopwords.words(language))
path_to_index = "."
doc_page=open(path_to_index+ "/doc_title_page.txt","w")
stem_dict={}


##print(stop_words)

class MergeIndices():


    def extract_key(self,line):
        """Extract key and convert to a form that gives the
        expected result in a comparison
        """
        return line.split(":",1)[0]


    def batch_sort(self,batch_size,path_to_index):

        filenames=glob.glob(path_to_index +"/*")
        ##print ("len filenames",len(filenames))
    #    if(len(filenames)==1):
    #        exit()
        k=batch_size
        no_of_batches=len(filenames)/float(k)
        ##print ("no_of_batches",no_of_batches)
        i=0
        m=0
        while(len(filenames)>1):
            i=0
            while(i<len(filenames)):
                    m=m+1
                    ##print i
                    #f=open("indexfiles2/index_"+str(m), 'w')
                    files=[]
                    for j in range(i,i+k):
                        if j < len(filenames):
                            files.append(open(filenames[j]))

                    with open(path_to_index +"/"+ "index_"+str(m), 'w') as dest:
                            decorated = [
                                ((self.extract_key(line), line) for line in f)
                                for f in files]
                            merged = heapq.merge(*decorated)
                            undecorated = map(itemgetter(-1), merged)
                            dest.writelines(undecorated)

#                    f.close()
                    for j in range(i,i+k):
                        if j < len(filenames):
                            os.remove(filenames[j])
                    i=i+k
                    ##print "i",i
            filenames=glob.glob(path_to_index+"/*")

    def mergelines_after_sort(self,path_to_index):
        filenames=glob.glob(path_to_index+"/*")
        ##print (len(filenames),filenames)
        indexfile=open(path_to_index + "/"+"indexfile","w")
        offset_file = open("offset.txt","w")
        final_index_file=indexfile
        f=None
        if len(filenames)==1:
            ##print ('yes')
            f=open(filenames[0])

        line=f.readline()
        if line :
            line=line.rstrip()
            prev_key=line.split(":",1)[0]
            offset_file.write(str(final_index_file.tell()) + "\n")
            #offset_file.write("\n")
            final_index_file.write(line)
            
        while True:
            line=f.readline()
            if not line:
                break
            line=line.rstrip()
            line_tokens=line.split(":",1)
            new_key=line_tokens[0]
            value=line_tokens[1]
            if(prev_key==new_key):
                ##print (value)
                final_index_file.write("|"+value)
                #offset_file.write(str(final_index_file.tell()) + "\n")
            else :
                final_index_file.write("\n")
                offset_file.write(str(final_index_file.tell()) +"\n")
                final_index_file.write(line)
            prev_key=new_key


class Page():
  def __init__(self):
        self.title=""
        self.text=""
        self.comment=""
        self.ref=""
        self.id=""
        self.wordlist=[]
        self.text_lines=[]

class WikiXmlHandler(xml.sax.ContentHandler):
  def __init__(self):
      self.current_data=""
      self.Page=""
      self.Pages=[]
      self.page_id=[]
      self.page_id_txt=""
      self.temp_txt=[]
      self.tmp_text2=[]
      self.all_lines=[]
      self.pages_file="documents.txt"
      self.line_tokens=[]
      self.f=None
      self.word_txt=[]
      self.word_list=[]
      self.page_title_text=""
      self.page_title=[]
      self.page_count = 0


  def startElement(self, tag, attrs):
    self.current_data=tag
    if(tag=="page"):
       # #print "-----------New Page--------------"
        self.Page=Page()
#    if(tag=="ref"):
#        #print "new ref"

  def endElement(self, tag):

      if(tag=="page"):
          if(len(self.page_id)>0):
              self.Page.id=self.page_id[0]
          page_title="".join(self.page_title)
          page_title=page_title.rstrip()
          page_title.replace("\"", "")
          mylist=[]
          mylist.append(page_title)
          self.page_count = self.page_count + 1
          ##print
          #self.f.write("{'id':"+self.Page.id+",'text':"+str(self.Page.text_lines)+",'title':'"+str(page_title)+"'}"+"\n")
          self.f.write('{"id":'+str(self.page_count)+',"text":'+str(self.Page.text_lines)+',"title":'+str(mylist)+'}'+'\n')
          self.page_id=[]
          self.page_title=[]


      if(tag=="id" ):
          self.page_id.append(self.page_id_txt)
          self.page_id_txt=""

      #if(tag=="title" ):


  def characters(self, content):
      if self.current_data=="title":
          self.page_title.append(content)
          #self.Page.title=self.Page.title+content
          #self.Page.title=self.Page.title+content

      if self.current_data=="text":

          self.tmp_text2.append(content.lower())


          if(content=='\n'):
              line="".join(self.tmp_text2)
              ##print line
              self.Page.text_lines.append(line)
              self.tmp_text2=[]


      if self.current_data=="id" :
          self.page_id_txt=content


class Document():
    def __init__(self):
        self.doc_id={}
        self.title={}
        self.body={}
        self.infobox={}
        self.categories={}
        self.external_links={}
        self.references={}

class Driver():

    def __init__(self):
        self.title=""
        self.text=""
        self.comment=""
        self.ref=""
        #self.STOPLIST=self.loadstoplist("code/stopwords.txt")
        self.wikihandler=None
        #self.finalindexpath="temp_index"
        self.DUMP=None
        self.INDEXFILE=None
        self.total_doc_length=0

    def makeindexfordocument(self,doc,pageid,path_to_index):
        indexfile=open(path_to_index+"/"+str(pageid),"w")
        index={}
        for key in doc.title:
            try:
                index[key]=index[key]+"t"+str(doc.title[key])
            except :
                index[key]="t"+str(doc.title[key])

        for key in doc.body:
            try:
                index[key]=index[key]+"b"+str(doc.body[key])
            except :
                index[key]="b"+str(doc.body[key])

        for key in doc.infobox:
            try:
                index[key]=index[key]+"i"+str(doc.infobox[key])
            except :
                index[key]="i"+str(doc.infobox[key])

        for key in doc.categories:
            try:
                index[key]=index[key]+"c"+str(doc.categories[key])
            except :
                index[key]="c"+str(doc.categories[key])

        for key in doc.external_links:
            try :
                index[key]=index[key]+"e"+str(doc.external_links[key])
            except :
                index[key]="e"+str(doc.external_links[key])
        for key in doc.references:
            try :
                index[key]=index[key]+"r"+str(doc.references[key])
            except :
                index[key]="r"+str(doc.references[key])


        s=sorted(index.keys())
        for k in s:
           v=index[k]
           indexfile.write(k+":"+str(pageid)+"-"+v+"\n")

        indexfile.close()

    def add_to_dict(self,tokens,dict_name):
        for token in tokens:
            try :
                dict_name[token]=dict_name[token]+1
            except :
                dict_name[token]=1




    def tokenise(self,string):
        global stem_dict
        string = string.lower()
        #string1 = re.sub('[^a-zA-Z0-9 \n\.]',  ' ', string)
        string =string.replace("_"," ")
        res = "".join(filter(lambda x: not x.isdigit(), string))
        #re.sub("<.*?_>"," ",string)
        ##print (string)
        tokenizer = RegexpTokenizer(r'\w+')
        tokens = tokenizer.tokenize(res)
        filtered_words = []
        for word in tokens:
            ##print word
            if word not in stop_words:
                ##print word
                token = str(word)
                if token != "":
                    if token in stem_dict:
                        w_data = stem_dict[token]
                    else:
                        w_data = sno.stem(token)
                        stem_dict[token] = w_data
                    #data = stemmer.stemWords(token)
                    ##print data
                    #token = sno.stem(token)
                    ##print (token)
                    filtered_words.append(w_data)
                ##print str(res)
                #token = sno.stem(token)
                ##print token


        return filtered_words



    def selectwordsToIndex(self,lines,doc,pageid):
      i=-1
      lines_len=len(lines)
      no_of_body_tokens = 0
#      #print lines_len,pageid
      no_of_body_tokens=0
      if(lines_len==1):
          ##print 'yes'
          return 0

      while(i<lines_len-1):
            i=i+1
            #if pageid == 42567219:
            #    #print i,lines[i]
            #if pageid == 42567223:
            #    #print i,lines[i]
            line=lines[i]
            line = line.strip()
            #if pageid == 42567223:
            #    #print line
            if line.startswith("{{infobox") :
                ##print 'infobox',line,pageid
                while True :
                    ##print 'yes'
                    if ((i+1)>=lines_len or lines[i+1].startswith("}}")):
                        break
                    i=i+1
                    line=lines[i]
                    ##print 'infobox',line,i
                    '''if line.startswith("[[category:"):
                        line = line[11:]
                        self.add_to_dict(self.tokenise(line),doc.categories)
                        break
                    elif  line.startswith("="):
                        break'''
                    ##print self.tokenise(line),pageid
                    self.add_to_dict(self.tokenise(line),doc.infobox)


            elif line.startswith("[[category:"):
                ##print 'category',pageid
                line=line[11:]
                self.add_to_dict(self.tokenise(line),doc.categories)

            elif line.startswith("=") :
                title_text=line.replace("=","")
                title_text=title_text.strip()

                if title_text=="references":
                    while True :
                        if (i+1)>=lines_len or lines[i+1].startswith("=") or lines[i+1].startswith("[[category:") :
                            ##print 'yes'
                            break
                        i=i+1
                        line=lines[i]

                        if (line.startswith("<ref") or line.startswith("")):
                            ##print self.tokenise(line)
                            self.add_to_dict(self.tokenise(line),doc.references)
                    continue


                elif title_text=="see also":
                    while True :
                        if (i+1)>=lines_len or lines[i+1].startswith("=") or lines[i+1].startswith("[[category:"):
                            break
                        i=i+1
                    continue

                elif title_text=="further reading":
                    while True :
                        if (i+1)>=lines_len or lines[i+1].startswith("=") or lines[i+1].startswith("[[category:"):
                            break
                        i=i+1
                    continue

                elif (title_text=="external links"):
                    while True:
                        if( i+1>=lines_len or lines[i+1].startswith("[[category:")):
                              break
                        i=i+1
                        line=lines[i]
                        if(line.startswith('*')):
                            self.add_to_dict(self.tokenise(line),doc.external_links)
                    continue

                else :
                    self.add_to_dict(self.tokenise(title_text),doc.title)
            else :
                tokens_in_line=self.tokenise(line)
                no_of_body_tokens=no_of_body_tokens+len(tokens_in_line)
                self.add_to_dict(tokens_in_line,doc.body)

      self.total_doc_length = self.total_doc_length + no_of_body_tokens
      return no_of_body_tokens


def main(sourceFileName,path_to_index):
    ##print (indexfile)
    #files=glob.glob("temp_folder/"+"/*")
    #for f in files:
    #    os.remove(f)
    source = open(sourceFileName)
    wikihandler=WikiXmlHandler()
    wikihandler.f=open(wikihandler.pages_file,"w")
    xml.sax.parse(source,wikihandler )              #XmlParsing

    ##print ("total number of pages",len(wikihandler.Pages))
    wikihandler.f.close()
    d=Driver()
    i=1
    count = 0
    begin=time.time()
    m=open(wikihandler.pages_file,"r")
    files_count = 0
    mi=MergeIndices()
    titleoffset_file = open("titleoffset.txt","w")
    titleoffset_file.write(str(doc_page.tell()) +"\n")
    doc_page.write('{"id":'+ str(0) +',"title":'+"['not found']"+'}\n')
    for line in m:
        count = count + 1
        mylist=ast.literal_eval(line)
        doc=Document()
        page_id=mylist["id"]
        page_title=mylist["title"]
      ##print page_id
        #start = time.time()
        l=d.selectwordsToIndex(mylist["text"],doc,count)
        ##print (time.time()-start)
      #for am in doc.categories:
      #      #print am
        #if l > 0:
        #start = time.time()
        ##print ("l;",l)
        d.makeindexfordocument(doc,count,path_to_index)
        #doc_page.write('\n')
        titleoffset_file.write(str(doc_page.tell()) +"\n")
        doc_page.write('{"id":'+ str(count)+',"title":'+str(page_title)+'}\n')
        ##print (time.time()-start)
        i = i +1
        files_count = files_count + 1
        ##print (files_count)
        if files_count==1000:
            #start=time.time()
            ##print ('yes')
            mi.batch_sort(1000,path_to_index)
            #mi.mergelines_after_sort(path_to_index)
            ##print ("merging time : ",  str(time.time()-start))
            files_count = 0
        l=0
    ##print ("files indexing time :", time.time()-begin)
    ##print ("total number of documents M:" ,i-1)
    ##print ("average document length :",d.total_doc_length/float(i-1))
    #mi=MergeIndices()
    #start=time.time()
    mi.batch_sort(1000,path_to_index)
    mi.mergelines_after_sort(path_to_index)
    ##print ("merging time : ",  str(time.time()-start))

  #d.merge_indices()

if __name__ == "__main__":
    importlib.reload(sys)
    #sys.setdefaultencoding('utf-8')
    logging.basicConfig()
    start_time=time.time()
    path_to_dump=sys.argv[1]
    path_to_index = sys.argv[2]
    #doc_page=open(path_to_index+ "/doc_title_page.txt","w")
    #main("enwiki-latest-pages-articles26.xml-p42567204p42663461")
    main(path_to_dump,path_to_index)
    end_time=time.time()
    parse_time=end_time-start_time
    print ("parsing time : ",parse_time)
