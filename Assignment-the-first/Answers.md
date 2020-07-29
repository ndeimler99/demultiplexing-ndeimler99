# Assignment the First

## Part 1
1. Be sure to upload your Python script.

| File name | label |
|---|---|
| 1294_S1_L008_R1_001.fastq.gz |  |
| 1294_S1_L008_R2_001.fastq.gz |  |
| 1294_S1_L008_R3_001.fastq.gz |  |
| 1294_S1_L008_R4_001.fastq.gz |  |

2. Per-base NT distribution
    1. Use markdown to insert your 4 histograms here.
    2. ```Your answer here```
    3. ```Your answer here```
    
## Part 2
1. Define the problem
    Unique indices allow numerous libraries to be run on the same flow cell, but this also results in the problem of how to differentiate which
    sequences belong to which library.  By writing a demultiplexing algorithm that looks at the forward and reverse read indices, one can determine
    which library the read belongs to.  However, problems arise when the read quality of the index is low as well as during an event known as index hopping 
    in which the wrong index gets appended to one of the reads due to errors during PCR.  
2. Describe output
    Since we are using 24 unique indices, there will be 48 fastq files that correlate to the forward and reverse reads for these barcodes.  In addition there will be 
    two files that contain the forward and reverse read pairs that have indexes that are too low of quality or contain a N (unknown nucleotide).  Lastly, there will be two files 
    for the forward and reverse reads that exhibited index hopping.
    
3. Upload your [4 input FASTQ files](../TEST-input_FASTQ) and your [4 expected output FASTQ files](../TEST-output_FASTQ).
4. Pseudocode
5. High level functions. For each function, be sure to include:
    1. Description/doc string
    2. Function headers (name and parameters)
    3. Test examples for individual functions
    4. Return statement
