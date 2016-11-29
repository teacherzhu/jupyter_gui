import subprocess as sp

FASTAS = {}


# SPECIES = ('human')


def load_fasta(species, filepath):
    """
    Set up .fasta filepath for species.
    :param species: str;
    :param filepath: str; .fasta or compressed .fasta
    :return: None
    """

    # if species not in SPECIES:
    #     raise ValueError('Unknown species {}; valid species are {}'.format(species, SPECIES))

    FASTAS[species] = filepath
    print('Loaded {} genome from {}'.format(species, filepath))


def explore_human_genome(chromosome, start, end):
    """
    Return human genomic sequences from region specified by chromosome:start-stop.
    :param chromosome: int or str; chromosome
    :param start: int or str; start position
    :param end: int or str; end position; must be greater than or equal to start position
    :return: str; genomic sequences from region specified by chromosome:start-stop in reference_genome
    """
    explore_genome(FASTAS['human'], chromosome, start, end)


def explore_genome(filepath, chromosome, start, end):
    """
    Return genomic sequences from region specified by chromosome:start-stop in reference_genome.
    :param filepath: str; filepath to a .fasta or compressed .fasta
    :param chromosome: int or str; chromosome
    :param start: int or str; start position
    :param end: int or str; end position; must be greater than or equal to start position
    :return: str; genomic sequences from region specified by chromosome:start-stop in reference_genome
    """

    cmd = 'samtools faidx {} {}:{}-{}'.format(filepath, chromosome, start, end)
    stdout = sp.run(cmd, shell=True, check=True, stdout=sp.PIPE, universal_newlines=True).stdout

    for line in stdout.split('\n')[1:]:
        print(line)

    return stdout.split('\n')[1:]
