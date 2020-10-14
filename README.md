Demultiplex.py Help Manual

Inputs:
	-f1 = --fileone = File One (Must be FASTQ) - Read One (Actual Sequence of Read One)
	-f2 = --filetwo = File Two (Must be FASTQ) - Read Two (Index One Sequence)
	-f3 = --filethree = File Three (Must be FASTQ) - Read Three (Index Two Sequence)
	-f4 = --filefour = File Four (Must be FASTQ) - Read Four (Actual Sequence of Read Two)
	-b = --barcodes = barcodes file (Must contain header line with values "index" and "index sequence") - .txt file that contains all indices that should be present in the sequencing run
	-e = --error_correct = boolean if you want to error correct or not, default is True. Will only error correct one mistake per sequence, including N's
Outputs:
	Two FASTQ files per barcode in the barcodes file (named by the name of the index followed by either R1 or R2) (Reads with correct indexes) (Read One and Read Two Sequence Reads)
	Two FASTQ files for reads containing unknown or low quality indices (Unmatched_R1 and Unmatched_R2) (Read one and Read Two Sequence Reads)
	Two FASTQ files for reads containing index hopping (Hopped_R1 and Hopped_R2) (Read one and Read Two Sequence Reads)
	Demultiplexed_Summary.txt
		Contains Summary Stats: 
			Total Number of Reads
			Total Number of Correct Reads and %Correct Reads
			Total Number of Reads in which Index Hopping Occured and %index hopped reads
			Total Number of Reads in which the Indices were Low Quality or Unknown (sequencing error) and %reads with these characteristics
		Tab Delimited Table
			Contains the Number of all Correct Reads sorted in Descending order by Number of Reads
			Contains the Number of all permutations of Index Hopped Reads sorted in Descending Order by Number of Reads
