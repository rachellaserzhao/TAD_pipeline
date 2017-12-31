# TAD_pipeline

config file editing instruction:
[westgrid]
email = recipient of job status report 
== symlink to programs used in the pipeline == 
bwa = /home/rachelz/.linuxbrew/bin/bwa
python = /home/rachelz/.linuxbrew/bin/python
fastqc = /home/rachelz/.linuxbrew/bin/fastqc
macs2 = /home/ofornes/.linuxbrew/bin/macs2
picard = /home/rachelz/.linuxbrew/bin/picard
samtools = /home/rachelz/.linuxbrew/bin/samtools
trimmomatic = /home/rachelz/.linuxbrew/bin/trimmomatic
hic = /home/rachelz/HiC-Pro
== queue specs == 
queue = orca
memory = 2
walltime = 24
processors = 16
== data file locations ==
indir = /home/rachelz/pipeline/test_data
hg19 = /home/rachelz/pipeline/genomes/hg19_idx/hg19.fa
hg38 = /home/rachelz/pipeline/genomes/hg38_idx/hg38.fa
resfrag = /home/rachelz/pipeline/resfrag/HindIII_resfrag_hg19.bed
chrsize19 = /home/rachelz/pipeline/chrsize/chrsize_19
chrsize38 = /home/rachelz/pipeline/chrsize/chrsize_38
indir = /home/rachelz/pipeline/test_data
template = /home/rachelz/pipeline/hic_template.sh
