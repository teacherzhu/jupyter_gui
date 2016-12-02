import subprocess as sp

GENOMES = {}
CODON_TO_AMINO_ACID = {'GUC': 'V', 'ACC': 'T', 'GUA': 'V', 'GUG': 'V', 'GUU': 'V', 'AAC': 'N', 'CCU': 'P', 'UGG': 'W',
                       'AGC': 'S', 'auc': 'I', 'CAU': 'H', 'AAU': 'N', 'AGU': 'S', 'ACU': 'T', 'CAC': 'H', 'ACG': 'T',
                       'CCG': 'P', 'CCA': 'P', 'ACA': 'T', 'CCC': 'P', 'GGU': 'G', 'UCU': 'S', 'GCG': 'A', 'UGC': 'C',
                       'CAG': 'Q', 'GAU': 'D', 'UAU': 'Y', 'CGG': 'R', 'UCG': 'S', 'AGG': 'R', 'GGG': 'G', 'UCC': 'S',
                       'UCA': 'S', 'GAG': 'E', 'GGA': 'G', 'UAC': 'Y', 'GAC': 'D', 'GAA': 'E', 'AUA': 'I', 'GCA': 'A',
                       'CUU': 'L', 'GGC': 'G', 'AUG': 'M', 'CUG': 'L', 'CUC': 'L', 'AGA': 'R', 'CUA': 'L', 'GCC': 'A',
                       'AAA': 'K', 'AAG': 'K', 'CAA': 'Q', 'UUU': 'F', 'CGU': 'R', 'CGA': 'R', 'GCU': 'A', 'UGU': 'C',
                       'AUU': 'I', 'UUG': 'L', 'UUA': 'L', 'CGC': 'R', 'UUC': 'F', 'UAA': '*', 'UGA': '*', 'UAG': '*',
                       'AUC': 'I'}


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


def get_species_dna_sequence(species, chromosome, start, end):
    """
    Return species' genomic sequences from region specified by chromosome:start-stop.
    :param species: str; genome file must alrady be loaded via load_genomic_filepath
    :param chromosome: int or str; chromosome
    :param start: int or str; start position
    :param end: int or str; end position; must be greater than or equal to start position
    :return: str; species' genomic sequences from region specified by chromosome:start-stop
    """

    return get_dna_sequence(GENOMES[species], chromosome, start, end)


def get_dna_sequence(filepath, chromosome, start, end):
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


def dna_to_rna(dna_sequence):
    """

    :param dna_sequence:
    :return:
    """

    return dna_sequence.replace('T', 'U')


def rna_to_dna(rna_sequence):
    """

    :param rna_sequence:
    :return:
    """

    return rna_sequence.replace('U', 'T')


def rna_to_aa(rna_sequence, codon_to_aa=CODON_TO_AMINO_ACID):
    """

    :param rna_sequence:
    :return:
    """

    aa = ''
    for i in range(len(rna_sequence) - 2):
        codon = rna_sequence[i:i + 3]
        aa += codon_to_aa[codon]
    return aa
