#!/bin/bash
#PBS -S /bin/bash

## Queue to which the job is to be submitted
#PBS -q [[queue]]

## Request N processors 
#PBS -l procs=[[processors]]

## Request 2 GB per processor
#PBS -l pmem=[[memory]]gb

## Maximum walltime to be used by the job 
#PBS -l walltime=[[hours]]:00:00

## Sent e-mail when the job begins, ends and aborts (bea)
#PBS -m bea

## Where the e-mail is to be sent
#PBS -M [[email]]

## Define variables to be used below
ADAPTER=""
BOWTIE2=[[bowtie2]]
FASTQC=[[fastqc]]
PYTHON=[[python]]
GENOME=[[genome]]
HICPRO_DIR=[[hicpro_dir]]
OUTPUT_DIR=[[output_dir]]
INPUT_DIR=[[input_dir]]
PREFIX=[[prefix]]
R1=[[r1]]
R2=[[r2]]
SAMTOOLS=[[samtools]]
TRIM_ADAPTER=[[trim_adapter]]
TRIMMOMATIC=[[trimmomatic]]
BWA=[[bwa]]
PROC=[[processors]]
RESFRAG=[[resfrag]]
BINSIZE=[[binsize]]
CHRSIZE=[[chrsize]]
JULIA=[[julia]]
TADFINDER=[[tadfinder]]
RES=[[res]]
BFILE1=[[bfile1]]
BFILE2=[[bfile2]]
RES=[[tadres]]
ADCORE=$(($PROC-1))

## align R1 and R2 (fasta.gz) reads separately to reference genome(hg19/hg38) using BWA mem

$BWA mem -t $PROC $GENOME $INPUT_DIR/$R1  > $OUTPUT_DIR/alignment.R1.sam

## sort and convert sam to bam file them remove orginta
$SAMTOOLS view -@ $ADCORE -o $OUTPUT_DIR/alignment_unsorted.R1.bam $OUTPUT_DIR/alignment.R1.sam

$SAMTOOLS sort  -@ $ADCORE -n -o $OUTPUT_DIR/alignment.R1.bam $OUTPUT_DIR/alignment_unsorted.R1.bam

rm -rf $OUTPUT_DIR/alignment.R1.sam

$BWA mem -t $PROC $GENOME $INPUT_DIR/$R2  > $OUTPUT_DIR/alignment.R2.sam

$SAMTOOLS view -@ ADCORE -o $OUTPUT_DIR/alignment_unsorted.R2.bam $OUTPUT_DIR/alignment.R2.sam

$SAMTOOLS sort  -@ ADCORE -n -o $OUTPUT_DIR/alignment.R2.bam $OUTPUT_DIR/alignment_unsorted.R2.bam

rm -rf $OUTPUT_DIR/alignment.R2.sam

## Pair R1 and R2 mates and filter reads
$PYTHON $HICPRO_DIR/scripts/mergeSAM.py -f $OUTPUT_DIR/alignment.R1.bam -r $OUTPUT_DIR/alignment.R2.bam -o $OUTPUT_DIR/paired.bam

## Hi-C pro mapping restriction fragments

$PYTHON $HICPRO_DIR/scripts/mapped_2hic_fragments.py -a -f $RESFRAG -r $OUTPUT_DIR/paired.bam -o $OUTPUT_DIR/

##matrix generation by Hi-C pro

$HICPRO_DIR/scripts/build_matrix --binsize $BINSIZE --chrsizes $CHRSIZE --ifile $OUTPUT_DIR/paired.validPairs --oprefix $OUTPUT_DIR/matrix_$BINSIZE

$JULIA $TADFINDER $OUTPUT_DIR/matrix_$BINSIZE $BFILE1 $BFILE2 res=$RES $OUTPUT_DIR/TAD_$PREFIX.bed
