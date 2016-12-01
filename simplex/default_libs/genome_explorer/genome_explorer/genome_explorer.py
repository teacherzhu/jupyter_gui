import subprocess as sp

GENOMES = {}


def load_genomic_filepath(species, filepath):
    """
    Set up species' filepath.
    :param species: str;
    :param filepath: str;
    :return: None
    """

    GENOMES[species] = filepath
    print('Loaded {} genome from: {}.'.format(species, filepath))


def list_available_contigs():
    """
    List contigs for each species.
    :return: dict; {species1:[contig1, contig2, ...], species2:[...], ...}
    """
    pass


def explore_species_genome(species, chromosome, start, end):
    """
    Return species' genomic sequences from region specified by chromosome:start-stop.
    :param species: str; genome file must alrady be loaded via load_genomic_filepath
    :param chromosome: int or str; chromosome
    :param start: int or str; start position
    :param end: int or str; end position; must be greater than or equal to start position
    :return: str; species' genomic sequences from region specified by chromosome:start-stop
    """

    return explore_genome(GENOMES[species], chromosome, start, end)


def explore_genome(filepath, chromosome, start, end):
    """
    Return genomic sequences from region specified by chromosome:start-stop in filepath.
    :param filepath: str;
    :param chromosome: int or str; chromosome
    :param start: int or str; start position
    :param end: int or str; end position; must be greater than or equal to start position
    :return: str; genomic sequences from region specified by chromosome:start-stop in filepath
    """

    if start >= end:
        raise ValueError('Starting genomic position must be greater than the ending genomic position.')

    cmd = 'samtools faidx {} {}:{}-{}'.format(filepath, chromosome, start, end)
    stdout = sp.run(cmd, shell=True, check=True, stdout=sp.PIPE, universal_newlines=True).stdout

    s = ''.join(stdout.split('\n')[1:])

    return s
