#!/usr/bin/env python2.7
import os, sys, re, io
import ConfigParser
import argparse
import shutil
import socket
from subprocess import call

# Read configuration file #
config = ConfigParser.ConfigParser()
config_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), "config.ini")
config.read(config_file)

#-------------#
# Options     #
#-------------#

def parse_options():
	"""
	This function parses the command line arguments and returns an optparse
	object.

	"""
	parser = argparse.ArgumentParser(description='pipeline for bwa mem alignmnet and hi-c')
	parser.add_argument('-r1', action='store', dest='r1', help="Replicate 1 (fastq file)", required=True, metavar='<R1.fastq>')
	parser.add_argument('-r2', action='store', dest='r2', help="Replicate 1 (fastq file)", required=True, metavar='<R2.fastq>')
	parser.add_argument('-e', action='store', default='', dest='experiment', help='experiment type', metavar='<experiment>')
	parser.add_argument('-g', default='hg38', action='store', dest='genome', help="Genome assembly (hg19 or hg38; default = hg38)", metavar='<genome>')
	parser.add_argument("-o", "--output-dir", default="./", action="store", dest="output_dir", help="Output directory will be pwd/output (default = ./)", metavar="<output_dir>")
	parser.add_argument("-p", action="store", dest="prefix", required=True, help="Prefix (identifies output dir/files)", metavar="<prefix>")
	'''
	parser.add_argument("-q", "--qsub", default=False, action="store_true", dest="submit", help="Submit PBS script to queue (default = False)")
	parser.add_argument("-w", "--walltime", default=168, action="store", type=int, dest="walltime", help="Walltime (in hours; default = 168; i.e. one week)", metavar="<walltime>")
	'''
	options = parser.parse_args()
	return options

def ConfigSectionMap(section):
	dict1 = {}
	options = config.options(section)
	for option in options:
		try:
			dict1[option] = config.get(section, option)
			if dict1[option] == -1:
				DebugPrint("skip: %s" % option)
		except:
			print("exception on %s!" % option)
			dict1[option] = None
	return dict1


def main (outdir, genome, genome_size):
	# Read template PBS script #
	in_file = open(template, 'r')
	file_data = in_file.read()
        if not in_file.closed:
                in_file.close()
    
    # Replace arguments #
    	file_data = file_data.replace('[[bwa]]', bwa)
    	file_data = file_data.replace('[[python]]', python)
	file_data = file_data.replace('[[email]]', email)
    	file_data = file_data.replace('[[fastqc]]', fastqc)
    	file_data = file_data.replace('[[genome]]', genome)
   	file_data = file_data.replace('[[hours]]', walltime)
    #	file_data = file_data.replace('[[macs2]]', config.get(section, "macs2"))
    	file_data = file_data.replace('[[memory]]', memory)
    	file_data = file_data.replace('[[output_dir]]', outdir)
	file_data = file_data.replace('[[input_dir]]',indir)
	file_data = file_data.replace('[[picard]]', picard)
	file_data = file_data.replace('[[prefix]]', options.prefix)
    	file_data = file_data.replace('[[processors]]', processors)
    	file_data = file_data.replace('[[queue]]', queue)
    	file_data = file_data.replace('[[r1]]', options.r1)
    	file_data = file_data.replace('[[r2]]', options.r2)
    	file_data = file_data.replace('[[samtools]]', samtools)
    	file_data = file_data.replace('[[trimmomatic]]', trimmomatic)
	file_data = file_data.replace('[[hicpro_dir]]', hic)
	file_data = file_data.replace('[[resfrag]]', resfrag)
	file_data = file_data.replace('[[chrsize]]', genome_size)
	file_data = file_data.replace('[[binsize]]', binsize)

    # Write PBS script #
	outfile = outdir + '/' + options.prefix + '.pbs'
    	with open(outfile, 'w') as out_file:
        	out_file.write(file_data)
	if not out_file.closed:
		out_file.close()
#-------------#
# Main        #
#-------------#

if __name__ == "__main__":

    # Arguments & Options #
	options = parse_options()
    # Get hostname #
	hostname = socket.gethostname()
    	westgrid_config = ConfigSectionMap(config.sections()[0])
	samtools = westgrid_config['samtools']
	processors = westgrid_config['processors']
	fastqc = westgrid_config['fastqc']
	picard = westgrid_config['picard']
	memory = westgrid_config['memory']
	walltime = westgrid_config['walltime']
	trimmomatic = westgrid_config['trimmomatic']
	queue = westgrid_config['queue']
	bwa = westgrid_config['bwa']
	hg38 = westgrid_config['hg38']
	hg19 = westgrid_config['hg19']
	email = westgrid_config['email']
	python = westgrid_config['python']
	hic = westgrid_config['hic']
	resfrag = westgrid_config['resfrag']
	binsize = westgrid_config['binsize']
	chrsize_19 = westgrid_config['chrsize19']
	chrsize_38 = westgrid_config['chrsize38']
	indir = westgrid_config['indir']
	template = westgrid_config['template']

    	# Create output directories #
	if not os.path.exists(os.path.abspath(options.output_dir)):
		os.makedirs(os.path.abspath(options.output_dir))

	if options.genome != "hg19" and options.genome != "hg38":
		parser.error('invalid genome')
	else:	
		if options.genome == "hg19": 
			genome = hg19
			genome_size = chrsize_19
		if options.genome == "hg38":
			genome = hg38
			genome_size = chrsize_38
		outdir = os.path.abspath(options.output_dir)
		
		main(outdir,genome,genome_size)
        '''
	if options.submit:
        	if system == "qsub":
            	os.system("qsub %s" % os.path.join(os.path.abspath(options.output_dir), options.prefix, "%s.pbs" % options.prefix))
        	else: pass
	'''


