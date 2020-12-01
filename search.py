from nltk import PorterStemmer
from nltk.corpus import stopwords
import ast
import time
import sys
import re
import os
import collections
import math
from math import *

total_no_of_documents=28694 #total no. of documents
average_document_length=1715 #average document length
k=1
language = "english"
stop_words = set(stopwords.words(language))
#path_to_index="/home/rishika/Documents/mini-project/temp_folder/indexfile"
#path_to_output="/home/rishika/Documents/mini-project/temp_folder/outputfile"
sno = PorterStemmer()
punctuation='!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
remove_punctuation_map = dict((ord(char), 32) for char in punctuation)
number='0123456789'
remove_number_map = dict((ord(char), None) for char in number)

class SearchDocument:
    def __init__(self):
        self.Y=[]
        self.final_list=[]
        self.temp_list = []
        self.X={}
        self.persons_dict={}
        self.doc_rank_score={}

    def find_doc_frequencies(self,doc_freq_term):
        frequencies={"t":0,"i":0,"c":0,"b":0,"r":0,"e":0,"net_total":0}
        term_tokens=doc_freq_term.split("-")
        doc_term=term_tokens[0]
        frequency_terms=term_tokens[1]
        freq_field=""
        freq_str=[]
        count=0
        total=[]
        for t in frequency_terms:
            #####print t
            try:
                int(t)
                freq_str.append(t) #freq_field=num
            except:
                num_str="".join(freq_str)
                try :
                    count=int(num_str)
                    total.append(count)
                except:
                    pass
                if (len(freq_field)>0):
                    frequencies[freq_field]=count
                freq_field=t
                freq_str=[]
                count=0
        num_str="".join(freq_str)
        count=int(num_str)
        total.append(count)
        if (len(freq_field)>0):
            frequencies[freq_field]=count
        net_total=sum(total)
        frequencies["net_total"]=net_total
        #####print (frequencies)
        return (doc_term,frequencies)

                    
                
    
    

    def rank(self,doc_id,frequency_dict,documentFreq,total_no_of_documents,word,score):
        #score = 0
        listOfDocuments, idf_of_word = collections.defaultdict(float), collections.defaultdict(float)
        idf_of_word[word] = math.log((float(total_no_of_documents)/(float(documentFreq) + 1)))
        value_till_now = frequency_dict['net_total']
        ##print (value_till_now)
        if frequency_dict['t'] > 0:
            value_till_now = value_till_now*10 + frequency_dict['t']
            score = score + (math.log(1 + value_till_now)*math.log(total_no_of_documents/documentFreq + 1))*0.25
        if frequency_dict['b'] > 0:
            value_till_now = value_till_now*10 + frequency_dict['b']
            score = score + (math.log(1 + value_till_now)*math.log(total_no_of_documents/documentFreq + 1))*0.25
        if frequency_dict['i'] > 0:
            value_till_now = value_till_now*10 + frequency_dict['i']
            score = score + (math.log(1 + value_till_now)*math.log(total_no_of_documents/documentFreq + 1))* 0.20
        if frequency_dict['c'] > 0:
            value_till_now = value_till_now*10 + frequency_dict['c']
            score = score + (math.log(1 + value_till_now)*math.log(total_no_of_documents/documentFreq + 1))* 0.1
        if frequency_dict['r'] > 0:
            value_till_now = value_till_now*10 + frequency_dict['r']
            score = score + (math.log(1 + value_till_now)*math.log(total_no_of_documents/documentFreq + 1))* 0.05
        if frequency_dict['e'] > 0:
            value_till_now = value_till_now*10 + frequency_dict['e']
            score = score + (math.log(1 + value_till_now)*math.log(total_no_of_documents/documentFreq + 1))* 0.05
        return score




    def find_query_word(self,path_to_index,q_term):
        ###print (type(q_term))
        indexfile=open(path_to_index,"r")
        for line in indexfile:
            line=line.rstrip()
            tokens=line.split(":")
            word=tokens[0]
            ####print (q_term,word)
            if(q_term==word):
                ###print ('yes')
                return tokens[1]
                break



    def findtitle(self,docid):
        f1=open("doc_title_page.txt","r")
        title='No results found'
        #docid=(docid.split("d"))[1]
        ####print (docid)        #####print docid
        for line in f1:
            line=line.rstrip()
            mydict=ast.literal_eval(line)
            #####print docid
            ####print (mydict["id"],docid)
            if str(mydict["id"])==str(docid):
                ####print ('yes')
                title=mydict["title"]
                break
                #return mydict['title']
        ####print (title)
        return title

    def check_line(self,pointer,path_to_index):
        f = open(path_to_index,"r")
        f.seek(pointer)
        line = f.readline()
        f.close()
        split_line = line.split(':')
        ##print (split_line)
        return split_line[0]

    def index_line(self,pointer,path_to_index):
        f = open(path_to_index,"r")
        f.seek(pointer)
        line = f.readline()
        f.close()
        return line

    def binary_search(self,token,offset,path_to_index):
        ##print ('yes')
        start = 0
        end = len(offset) - 1
        ##print (end,start)
        while start <= end:
            mid = int(start +(end-start)/2)
            offset[mid] = int(offset[mid])
            ##print ('mid',offset[mid])
            ##print(self.check_line(offset[mid],path_to_index))
            if (self.check_line(offset[mid],path_to_index) > token):
                ##print(self.check_line(offset[mid],path_to_index))
                end = mid -1
            if(self.check_line(offset[mid],path_to_index) < token):
                ##print(self.check_line(offset[mid],path_to_index))
                start = mid + 1
            if(self.check_line(offset[mid],path_to_index) == token):
                ##print (self.index_line(offset[mid],path_to_index))
                line = self.index_line(offset[mid],path_to_index)
                line=line.rstrip()
                tokens=line.split(":")
                word=tokens[0]
                if(token==word):
                    ##print (tokens[1])
                    return tokens[1]

    def title_check_line(self,pointer):
        f = open("doc_title_page.txt","r")
        f.seek(pointer)
        line = f.readline()
        f.close()
        split1 = line.split(':')
        temp1 = split1[1]
        split2 = temp1.split(',')
        return split2[0]
        ##print (split2[1])

    def title_index_line(self,pointer):
        f = open("doc_title_page.txt","r")
        f.seek(pointer)
        line = f.readline()
        f.close()
        split1 = line.split('[')
        #temp1 = split1[2]
        #split2 = temp1.split(',')
        return split1[1]

    def title_binary_search(self,docid,titleoffset):
        start = 0
        end = len(titleoffset) - 1
        '''mid = int(start +(end-start)/2)
        titleoffset[mid] = int(titleoffset[mid])
        #print (self.title_check_line(titleoffset[mid]),docid)
        #return 'yes'
        if (int(self.title_check_line(titleoffset[mid])) > docid):
            #print('1')
        elif (int(self.title_check_line(titleoffset[mid])) < docid):
            #print('2')'''
        while start <= end:
            mid = int(start +(end-start)/2)
            titleoffset[mid] = int(titleoffset[mid])
            ##print (self.title_check_line(titleoffset[mid]),docid)
            #self.title_check_line(titleoffset[mid])
            if (int(self.title_check_line(titleoffset[mid])) > int(docid)):
                ##print(self.check_line(offset[mid],path_to_index))
                ##print('1')
                end = mid  - 1
               
            if(int(self.title_check_line(titleoffset[mid])) < int(docid)):
                ##print(self.check_line(offset[mid],path_to_index))
                start = mid + 1
                ##print('2')
#
            if(int(self.title_check_line(titleoffset[mid])) == int(docid)):
                ##print (self.index_line(offset[mid],path_to_index))
                line = self.title_index_line(titleoffset[mid])
                line = ''.join(c for c in line if c not in '[]{}<>')
                line = line.strip('\n')
                line1 = line[1:]
                lenght = len(line1)
                if line1[lenght-1]=="'":
                    ##print(line1)
                    line1 = line1[:lenght-1]
                return line1


    def parse_refine_query(self,path_to_index,query,offset,titleoffset):

        #####print 'query1',query
        temp = query.split(':')
        query = query.lower()
        ####print (query)
        query_dict = {}
        query_id =''
        temp1 = []
        temp2 = []
        temp3 = []
        temp4 = []
        temp5 = []
        binary_temp = []
        count1 = 0
        count2 = 0
        index_entry = None
        if re.match(r'(title|body|infobox|category|ref):', query):
            ###print ('special',temp)
            words = re.findall(r'(title|body|infobox|category|ref):([^:]*)(?!\S)', query)
            tempFields = re.findall(r'(title|body|infobox|category|ref):', query)
            #####print ('extract',words,tempFields)
            tokens = []
            fields = []
            for word in words:
                query_dict[word[0]] = word[1]
            #####print (query_dict)
            for que in query_dict:
                ####print (que,query_dict[que])
                if que=="body":
                    for alpha in query_dict[que].split():
                        if alpha not in stop_words:
                            ####print (alpha)
                            #index_entry=self.find_query_word(path_to_index,alpha)
                            index_entry=self.binary_search(alpha,offset,path_to_index)
                            #print ("index_entry=",index_entry)
                            if (index_entry==None):
                                break
                            else:
                                docs_freq_terms=index_entry.split("|")
                                for doc in docs_freq_terms:
                                    (doc_id,frequency_dict)=self.find_doc_frequencies(doc)
                                    ####print ("document_frequency",frequency_dict)
                                    if frequency_dict['b']!=0:
                                        ####print (doc_id)
                                        if len(query_id) < 1:
                                            query_id = doc_id
                                        else:
                                            if query_id==doc_id:
                                                pass
                                            else:
                                                query_id =''
                elif que=="category":
                    for alpha in query_dict[que].split():
                        if alpha not in stop_words:
                            ####print (alpha)
                            #index_entry=self.find_query_word(path_to_index,alpha)
                            index_entry=self.binary_search(alpha,offset,path_to_index)
                            #print ("index_entry=",index_entry)
                            if (index_entry==None):
                                break
                            else:
                                docs_freq_terms=index_entry.split("|")
                                for doc in docs_freq_terms:
                                    (doc_id,frequency_dict)=self.find_doc_frequencies(doc)
                                    ####print ("document_frequency",frequency_dict)
                                    if frequency_dict['c']!=0:
                                        ####print (doc_id)
                                        if len(query_id) < 1:
                                            query_id = doc_id
                                        else:
                                            if query_id==doc_id:
                                                pass
                                            else:
                                                query_id = ''
                                            
                elif que=="infobox":
                    for alpha in query_dict[que].split():
                        if alpha not in stop_words:
                            ####print (alpha)
                            #index_entry=self.find_query_word(path_to_index,alpha)
                            index_entry=self.binary_search(alpha,offset,path_to_index)
                            #print ("index_entry=",index_entry)
                            if (index_entry==None):
                                break
                            else:
                                docs_freq_terms=index_entry.split("|")
                                for doc in docs_freq_terms:
                                    (doc_id,frequency_dict)=self.find_doc_frequencies(doc)
                                    ####print ("document_frequency",frequency_dict)
                                    if frequency_dict['i']!=0:
                                        ####print (doc_id)
                                        if len(query_id) < 1:
                                            query_id = doc_id
                                        else:
                                            if query_id==doc_id:
                                                pass
                                            else:
                                                query_id =''
                                            
                elif que=="ref":
                    for alpha in query_dict[que].split():
                        if alpha not in stop_words:
                            ####print (alpha)
                            #index_entry=self.find_query_word(path_to_index,alpha)
                            index_entry=self.binary_search(alpha,offset,path_to_index)
                            #print ("index_entry=",index_entry)
                            if (index_entry==None):
                                break
                            else:
                                docs_freq_terms=index_entry.split("|")
                                for doc in docs_freq_terms:
                                    (doc_id,frequency_dict)=self.find_doc_frequencies(doc)
                                    ####print ("document_frequency",frequency_dict)
                                    if frequency_dict['r']!=0:
                                        ####print (doc_id)
                                        if len(query_id) < 1:
                                            query_id = doc_id
                                        else:
                                            if query_id==doc_id:
                                                pass
                                            else:
                                                query_id =''

            if len(query_id) < 1:
                temp4.append('No results found')
                self.final_list.append(temp4)
                temp4 = []
            else:
                binary_title = self.title_binary_search(doc_id,titleoffset)
                binary_title = ''.join(c for c in binary_title if c not in '[]{}<>')
                temp5.append(str(binary_title))
                self.final_list.append(temp5)
                temp5 = []

        else:
            query_terms = query.split()
            ###print (query_terms,len(query_terms))
            if len(query_terms) > 1:
                final_query_terms=[]
                score_dict ={}
                for i in range(total_no_of_documents):
                    score_dict[i+1] = 0
                #print (score_dict[10002])
                for q in query_terms:
                    if q not in stop_words:
                        final_query_terms.append(q)

                for q in final_query_terms:
                    ###print ("query_terms",q)
                    index_entry = self.binary_search(q,offset,path_to_index)
                    ##print ('output',index_entry)
                    #index_entry=self.find_query_word(path_to_index,q)
                    ###print ("index_entry=",index_entry)
                    if (index_entry==None):
                        temp3.append('No results found')
                        self.final_list.append(temp3)
                        temp3 = []
                    else:
                        docs_freq_terms=index_entry.split("|")
                        df=len(docs_freq_terms)
                        ####print (df,docs_freq_terms)
                        for doc in docs_freq_terms:
                            score = 0
                            count1 = count1 + 1                        
                            (doc_id,frequency_dict)=self.find_doc_frequencies(doc)
                            #print (doc_id)
                            old_value = score_dict[int(doc_id)]
                            ####print (doc_id)
                            ####print ("document_frequency",frequency_dict)
                            net_score = self.rank(doc_id,frequency_dict,df,total_no_of_documents,query,score)
                            ##print(type(net_score))
                            new_value = old_value + net_score
                            score_dict[doc_id] = new_value
                sorted_score_docid = sorted(score_dict, key=score_dict.get, reverse=True)[:10]
                for docid in sorted_score_docid:
                    binary_title=self.title_binary_search(docid,titleoffset)
                    binary_title = ''.join(c for c in binary_title if c not in '[]{}<>')
                    temp2.append(binary_title)
                    

                ###print ("care",temp2)
                self.final_list.append(temp2)
                temp2 = []
            
            if len(query_terms)<=1:
                query= ''.join(c for c in query if c not in '[]{}<>')
                query = os.linesep.join([s for s in query.splitlines() if s])
                ##print (query)
                score_dict={}
                temp_dict1={}
                sorted_score_docid=[]
                if query not in stop_words:
                    #index_entry=self.find_query_word(path_to_index,query)
                    index_entry= self.binary_search(query,offset,path_to_index)
                    ##print ('output',index_entry)
                    if (index_entry==None):
                        temp3.append('No results found')
                        self.final_list.append(temp3)
                        temp3 = []
                    else:
                        docs_freq_terms=index_entry.split("|")
                        df=len(docs_freq_terms)
                        ##print ('sp',df,docs_freq_terms)
                        for doc in docs_freq_terms:
                            score = 0
                            count2 = count2 + 1                       
                            (doc_id,frequency_dict)=self.find_doc_frequencies(doc)

                            ####print (doc_id)
                            ##print ("document_frequency",frequency_dict)
                            net_score = self.rank(doc_id,frequency_dict,df,total_no_of_documents,query,score)
                            ##print (net_score)
                            score_dict[doc_id] = net_score

                        
                        ##print(score_dict)
                        sorted_score_docid = sorted(score_dict, key=score_dict.get, reverse=True)[:10]
                        ##print(sorted_score_docid)
                        #self.title_binary_search(7815,titleoffset)
                        for docid in sorted_score_docid:
                            binary_title=self.title_binary_search(docid,titleoffset)
                            binary_title = ''.join(c for c in binary_title if c not in '[]{}<>')
                            #doc_title = self.findtitle(docid)
                            #doc_title = ''.join(c for c in doc_title if c not in '[]{}<>')
                            ##print (docid,doc_title)
                            #temp_dict1[doc_id] = doc_title
                            ###print ("title:",doc_title)
                            #binary_temp.append(binary_title)
                            temp1.append(binary_title)

                        ##print (temp1,binary_temp)
                        #temp1 = self.sorting(score_dict,temp_dict1)
                        self.final_list.append(temp1)
                        temp1 = []
        ####print (self.final_list)
        return self.final_list


def read_file(testfile):
    with open(testfile, 'r') as file:
        queries = file.readlines()
    return queries


def write_file(outputs, path_to_output):
    ####print (outputs)
    '''outputs should be a list of lists.
        len(outputs) = number of queries
        Each element in outputs should be a list of titles corresponding to a particular query.'''
    with open(path_to_output, 'w') as file:
        for output in outputs:
            ####print("oo",output)
            for word in output:
                file.write(word + '\n')
            file.write('\n')


def search(path_to_index, queries):
    ####print ("queries",queries)
    out = []
    offset = []
    titleoffset = []
    doc=SearchDocument()
    begin= time.time()
    f = open("offset.txt","r")
    lines = f.readlines()
    for line in lines:        
        line = ''.join(c for c in line if c not in '[]{}<>')
        line = line[:-1]
        offset.append(line)

    f1 = open("titleoffset.txt","r")
    lines1 = f1.readlines()
    for line in lines1:        
        line = ''.join(c for c in line if c not in '[]{}<>')
        line = line[:-1]
        titleoffset.append(line)

    ##print(titleoffset)
    for query in queries:
        listOfFields, temp = [], []
        queryWords = query.strip().split(' ')
        for word in queryWords:
            if re.search(r'[t|b|c|e|i]{1,}:', word):
                _fields = list(word.split(':')[0])
                _words = [word.split(':')[1]] * len(_fields)
            else:
                _fields = ['t', 'b', 'c', 'e', 'i']
                _words = [word] * len(_fields)

            listOfFields.extend(_fields)
            #temp.extend(cleanup_string(" ".join(_words)))
        ##print ("Fields:", listOfFields)
        ##print ("Words:", temp)
        out = doc.parse_refine_query(path_to_index,query,offset,titleoffset)

    ####print ("total",time.time()-begin)
    return out
    pass


def main():
    out = []
    outputs=[]
    path_to_index = sys.argv[1]
    testfile = sys.argv[2]
    path_to_output = sys.argv[3]
    begin = time.time()
    queries = read_file(testfile)
    outputs = search(path_to_index, queries)
    write_file(outputs, path_to_output)
    end = time.time()
    #time = end-begin
    print ('response time:',end-begin)


if __name__ == '__main__':
    main()
