import os
import subprocess as sp

DIR_HOME = os.environ['HOME']
HUMAN = os.path.join(DIR_HOME, 'data', 'grch', '38', 'sequence', 'primary_assembly',
                     'Homo_sapiens.GRCh38.dna.primary_assembly.fa.gz')


def explore_genome(reference_genome, chromosome, start, end):
    """
    Return genomic sequences from region specified by chromosome:start-stop in reference_genome.
    :param reference_genome: str; filepath to a .fasta file
    :param chromosome: int or str; chromosome
    :param start: int or str; start position
    :param end: int or str; end position; must be greater than or equal to start position
    :return: str; genomic sequences from region specified by chromosome:start-stop in reference_genome
    """

    cmd = 'samtools faidx {} {}:{}-{}'.format(reference_genome, chromosome, start, end)
    stdout = sp.run(cmd, shell=True, check=True, stdout=sp.PIPE, universal_newlines=True).stdout

    for line in stdout.split('\n')[1:]:
        print(line)

    return stdout.split('\n')[1:]
