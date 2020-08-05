#!/usr/bin/env python

import argparse
import gzip
import itertools

def get_args():
    parser = argparse.ArgumentParser(description = "Demultiplexing Algorithm")
    parser.add_argument("-f1", "--fileOne", help="What is your read file name?", required = True)
    parser.add_argument("-f2", "--fileTwo", help="What is your Read 2 file name? (Index One)", required = True)
    parser.add_argument("-f3", "--fileThree", help="What is your Read 3 file name? (Index Two)", required = True)
    parser.add_argument("-f4", "--fileFour", help="What is your Read 4 file name? (Read Two)", required = True)
    parser.add_argument("-b", "--barcodes", help = "Index must be in fourth column and sequence in fifth")
    return parser.parse_args()

args = get_args()
readOne = args.fileOne
readTwo = args.fileTwo
readThree = args.fileThree
readFour = args.fileFour
barcodes = args.barcodes

def rev_complement(stringInput):
    '''takes stringInput parameter and returns the reverse complement of the input'''
    #reverse string
    reverse = stringInput[::-1]
    #replace with commplement
    complement = {"A" : "T", "C" : "G", "G" : "C", "T" : "A", "N" : "N"}
    output = "".join([complement[base] for base in reverse])
    
    return output

def open_files(indexes):
    '''Creates Dictionary of barcodes with names as well as opening output files'''
    #find out what column is index and what column is index sequence
    #create dictionary with index as keys and index sequence as barcodes
    fileList = {}

    for item in indexes.keys():
        #for every barcode create name of barcode "_R1" and "_R2" files
        count=1
        name = indexes[item] + "_R" + str(count)
        fh = open(name, "a")
        fileList[name] = fh
        count+=1
        name = indexes[item] + "_R" + str(count)
        fh = open(name, "a")
        fileList[name] = fh   
    #create unmatched and hopped R1 and R2 files
    name = "Unmatched_R1"
    unmatched_R1 = open(name, "a")
    fileList[name] = unmatched_R1
    name = "Unmatched_R2"
    unmatched_R2 = open(name, "a")
    fileList[name] = unmatched_R2
    name = "Hopped_R1"
    hopped_R1 = open(name, "a")
    fileList[name] = hopped_R1
    name = "Hopped_R2"
    hopped_R2 = open(name, "a")
    fileList[name] = hopped_R2

    #return a list of file objects
    return fileList

def close_files(fileList):
    '''Cloes all files opened in open_files()'''
    #takes file list created by open_files method and closes all files
    for item in fileList.values():
        item.close()
    return "Succesfully closed"

def write_out(records, recordType, fileList):
    '''used to write to respective files'''
    for i in range(len(records[0])):
        #adds new line characters to the end of the records so writelines can be used
        records[0][i] = records[0][i] + "\n"
        records[3][i] = records[3][i] + "\n"
    
    if recordType == "hopped":
        #if the records hopped write to the hopped files
        fileList["Hopped_R1"].writelines(records[0])
        fileList["Hopped_R2"].writelines(records[3])
    elif recordType == "lowQual":
        #if the records are lowquality write to the lowquality file
        fileList["Unmatched_R1"].writelines(records[0])
        fileList["Unmatched_R2"].writelines(records[3])
    else:
        #figure out which barcode file we need to write to, then write to R1 and R2
        barcode = records[1][1].strip()
        fileName = indexes[barcode] + "_R1"
        #print(fileName)
        fileList[fileName].writelines(records[0])
        fileName = fileName[:-1] + "2"
        fileList[fileName].writelines(records[3])
    pass

def quality_score_check(qScores):
    '''takes input parameter of a sequence, converts that sequence to phred scores, and returns if the average quality score is above or below a certain threshold'''
    sum = 0
    for item in qScores:
        #print(item)
        sum += ord(item) - 33
        #if ord(item) - 33 < 30:
            #return False
    
    avg = sum / len(qScores)
    #print(len(qScores))
    return avg >= 30
    #return True

def create_dict(fh):
    '''Create a dictionary of all possible permutations of indexes as supplied by file'''
    #find out what column is index and what column is index sequence
    #create dictionary with index as keys and index name as barcodes
    indexes = {}
    #indexes - key: barcode, value: name of barcode
    accurate = {}
    #accurate - key: barcode tuple, value: number of times that barcode matching occurs
    with open(barcodes, "r") as table:
        lineCount = 0
        index = 0
        sequence = 0 
        for line in table:
            #takes each line in indexes name file
            line = line.strip().split("\t")
            #print(line)
            if lineCount == 0:
                #determine which column has the index sequence and which has the index name
                column = 0
                for item in line:
                    if item == "index":
                        index = column
                    if item == "index sequence":
                        sequence = column
                    column += 1
                #print(index, sequence)
            else:
                #for every other line use the predefined columns to create index dictionary
                indexes[line[sequence]] = line[index]
            lineCount += 1
        #print(len(indexes))
        bars = {}
        #like accurate but with hopping (key is a tuple) value is number of times that permutation happened
        for perm in itertools.permutations(indexes, 2):
            #itertools permutations.  Will create every unique combination of tuples
            bars[perm] = 0
        for item in indexes:
            #creates permutations missed by itertools permutation (when they are the same)
            accurate[(item, item)] = 0

        #print(len(accurate))
        
    return indexes, bars, accurate

def print_dict(indexes, dictionary, correct, hopped, errors, accurate):
    '''iterates through master dictionary printing barcode combinations and occurences'''
    '''parameters are indexed dictionary, values dictionary, number of correct reads, number of hopped reads, and number of error/low quality reads'''
    
    with open("Demultiplexed_Summary.txt", "a") as fh:
        #opens summarys stats
        fh.write("Total Number of Reads: " + str(hopped + errors + correct) + "\n")
        fh.write("Number of Matching Reads: " + str(correct) + "\n")
        fh.write("Number of Hopped Reads: " + str(hopped) + "\n")
        fh.write("Number of Low Quality Indexed Reads: " + str(errors) + "\n")
        
        fh.write("Index One Name\tIndex One Sequence\tIndex Two Name\tIndex Two Sequence\tOccurences\n")
        
        for item in sorted(accurate, key=accurate.get, reverse=True):
            #for item in dictionary where no hoppping occured
            fh.write(indexes[item[0]] + "\t" + item[0] + "\t" +  indexes[item[1]] + "\t" +  item[1]  + "\t" + str(accurate[item]) + "\n")

        for item in sorted(dictionary, key=dictionary.get, reverse=True):
            #for item in hopping dictionary
            fh.write(indexes[item[0]] + "\t" + item[0] + "\t" +  indexes[item[1]] + "\t" +  item[1]  + "\t" + str(dictionary[item]) + "\n") 
            
            #print(indexes[item[0]], indexes[item[1]], item[0], item[1],dictionary[item], sep="\t") 
    pass
    

def demultiplex(index, value, accurate):
    hopped = 0
    lowQuality = 0
    correct = 0

    #create list of file objects
    fileList = open_files(index)
    #print(fileList)
    #print(type(fileList[0]))

    with gzip.open(readOne, "rt") as readOneFile, gzip.open(readTwo, "rt") as indexOneFile, gzip.open(readThree, "rt") as indexTwoFile, gzip.open(readFour, "rt") as readTwoFile:
        #open main files that contain sequences (still zipped)
        lineCount = 0
        records = [[],[],[],[]]
        for readOneLine, indexOneLine, indexTwoLine, readTwoLine in zip(readOneFile, indexOneFile, indexTwoFile, readTwoFile):
            #for each line in that file, strip the lines
            lineCount += 1
            readOneLine = readOneLine.strip()
            indexOneLine = indexOneLine.strip()
            indexTwoLine = indexTwoLine.strip()
            readTwoLine = readTwoLine.strip()

            #add the lines to a temporary 2D list
            records[0].append(readOneLine)
            records[1].append(indexOneLine)
            records[2].append(indexTwoLine)
            records[3].append(readTwoLine)

            if lineCount % 4 == 0:
                #if records are complete
                #add barcodes to records
                barcodesAppend = records[1][1] + "-" + rev_complement(records[2][1])
                records[0][0] = records[0][0] + ":" + barcodesAppend
                records[3][0] = records[3][0] + ":" + barcodesAppend

                #if records[1][1] not in index.keys():
                    #indexOne = rev_complement(records[1][1])
                    #indexTwo = records[2][1]
                #else:
                    #indexTwo = rev_complement(records[2][1])
                    #indexOne = records[1][1]
                indexOne = records[1][1]
                indexTwo = rev_complement(records[2][1])
                
                #if the indexes in the index dictionary
                if indexOne in index.keys() and indexTwo in index.keys():
                    #if they pass the quality score check
                    if quality_score_check(records[1][3]) and quality_score_check(records[2][3]):
                        #if it is high enough quality
                        #if they are the same (no hopping)
                        if indexOne == indexTwo:
                            #they are the same
                            write_out(records, "yay", fileList)
                            correct += 1
                            accurate[(indexOne, indexOne)] += 1
                        else:
                            #index hopping occured
                            write_out(records, "hopped", fileList)
                            hopped += 1
                            tupleDict = (indexOne, indexTwo)
                            value[tupleDict] += 1
                    else:
                        #quality is low
                        #print("low")
                        write_out(records, "lowQual", fileList)
                        lowQuality += 1
                else:
                    #index was not in the dictionary, why?
                    if "N" in indexOne or "N" in indexTwo:
                        #index contained an N
                        write_out(records, "lowQual", fileList)
                        lowQuality += 1
                    else:
                        #sequencing error
                        write_out(records, "lowQual", fileList)
                        lowQuality += 1
                #reset records to being blank 2d list
                records = [[],[],[],[]]
    #close files and print summary stats
    close_files(fileList)
    print_dict(index, value, correct, hopped, lowQuality, accurate)

    return "Demultiplexing Complete"

indexes, bars, accurate = create_dict(barcodes)
demultiplex(indexes, bars, accurate)

