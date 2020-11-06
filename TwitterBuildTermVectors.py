#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
@author: OstermannFO

builds term vectors by lexical matching
    
table in database needs to have vector field "term_vector"
and text field "terms_found" ready and empty;
INSERT statement and other database-related parameters need to be 
manually adjusted
"""

#
# import statements
#
import re
import psycopg2
import sys
import datetime
import nltk

#
#declare user variables in CAPITALS
# 
CONN_DB = ""
PATH = "/path/to/working/directory/"
TERM_FILE = "terms_stemmed.txt"
LOG_FILE = "TwitterBuildTermVectors.log"

def main():

    conn = psycopg2.connect(CONN_DB)
    cur = conn.cursor('server_side_cursor', withhold = True) #for big result sets
    cur2 = conn.cursor()
    stemmer = nltk.PorterStemmer()

    log_file_name = PATH + LOG_FILE
    log_file = open(log_file_name,'a')

    # create dictionary with term:index_number (needed for later adding up found terms)
    term_dict = {}
    file_handle = open(PATH + TERM_FILE)
    dict_index = 0
    for line in file_handle:
        term_dict[line.rstrip()] = dict_index
        dict_index += 1
    file_handle.close()

    # collect ids of entries to process
    try:
        cur.execute("SELECT tweet_id FROM london_tweets WHERE terms_found IS NULL")
        t_ids=cur.fetchall()
    except Exception as e:
        print("DB error: ", sys.exc_info()[0], e)
        log_file.write(str(datetime.datetime.today()) 
                        + " DB Error SELECT while fetching records: " 
                        + str(e).replace("\n"," ") + "\n")
        t_ids = []

    number_records = len(t_ids)
    counter = 1

    # remove unwanted characters from input string
    pattern = re.compile('[\W_]+', re.UNICODE) #remove problematic characters
    
    for t_id in t_ids:

        str_id = str(t_id[0])
        input_unigrams = []
        found_terms = []
        term_vector = [0] * len(term_dict)

        # retrieve data for finding terms
        try:
            cur2.execute("SELECT tweet_text FROM london_tweets WHERE tweet_id = '"
                        + str_id + "'")
            input_text = cur2.fetchall()
        except Exception as e:
            conn.rollback()
            print("DB error: ", sys.exc_info()[0], e)
            log_file.write(str(datetime.datetime.today()) 
                           + " DB Error SELECT Tweet id " 
                           + str_id + " : " 
                           + str(e).replace("\n"," ") + "\n")
            print(str(counter) + " of " + str(number_records)) 
            counter += 1
            continue

        # actual processing of input strings
        # split input up and replace unwanted characters
        unigrams = str(input_text[0]).split(" ")

        # build list of input unigrams
        for unigram in unigrams:
            input_unigrams.append(pattern.sub('', unigram.lower()))

        # create term vector
        for input_unigram in input_unigrams:
            input_unigram_stemmed = stemmer.stem(input_unigram)
            if input_unigram_stemmed in term_dict:
                term_vector[term_dict[input_unigram_stemmed]] += 1
                found_terms.append(input_unigram_stemmed)
        if not found_terms:
            found_terms = '0'
        else:
            found_terms = ','.join(str(s) for s in found_terms)

        # insert into table
        data = ('{' + ','.join(str(i) for i in term_vector) + '}',
                    found_terms,
                    str_id)

        try:  
            cur2.execute("""UPDATE london_tweets
                        SET (term_vector,terms_found) = 
                        (%s,%s) 
                        WHERE tweet_id = (%s);""", data)
            conn.commit()
        except Exception as e:
            conn.rollback()
            print("DB error: ", sys.exc_info()[0], e)
            log_file.write(str(datetime.datetime.today()) 
                           + " DB Error UPDATE Tweet id " 
                           + str_id + " : " 
                           + str(e).replace("\n"," ") + "\n")    
        
        print(str(counter) + " of " + str(number_records)) 
        counter += 1
         
    conn.close()    
    log_file.close()

if __name__=="__main__":
    main() 