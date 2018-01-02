# TAD_pipeline

This pipeline is written to process fastq reads of R1 and R2 to a list of topologically associating domains (TADs) in .bed format

IMPORTANT SET UP STEPS:
1. Compile build_matrix program using build_matrix.cpp in HiC-Pro src folder
2. Edit first line of run_MrTADFinder.jl file in the MrTADFinder folder to include the correct path of MrTADFinder.jl on your local computer/server

config.ini file editing instruction:

