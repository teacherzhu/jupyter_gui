import subprocess as sp

GENOME_FILEPATH = None
CODON_TO_AMINO_ACID = {'GUC': 'V', 'ACC': 'T', 'GUA': 'V', 'GUG': 'V', 'GUU': 'V', 'AAC': 'N', 'CCU': 'P', 'UGG': 'W',
                       'AGC': 'S', 'auc': 'I', 'CAU': 'H', 'AAU': 'N', 'AGU': 'S', 'ACU': 'T', 'CAC': 'H', 'ACG': 'T',
                       'CCG': 'P', 'CCA': 'P', 'ACA': 'T', 'CCC': 'P', 'GGU': 'G', 'UCU': 'S', 'GCG': 'A', 'UGC': 'C',
                       'CAG': 'Q', 'GAU': 'D', 'UAU': 'Y', 'CGG': 'R', 'UCG': 'S', 'AGG': 'R', 'GGG': 'G', 'UCC': 'S',
                       'UCA': 'S', 'GAG': 'E', 'GGA': 'G', 'UAC': 'Y', 'GAC': 'D', 'GAA': 'E', 'AUA': 'I', 'GCA': 'A',
                       'CUU': 'L', 'GGC': 'G', 'AUG': 'M', 'CUG': 'L', 'CUC': 'L', 'AGA': 'R', 'CUA': 'L', 'GCC': 'A',
                       'AAA': 'K', 'AAG': 'K', 'CAA': 'Q', 'UUU': 'F', 'CGU': 'R', 'CGA': 'R', 'GCU': 'A', 'UGU': 'C',
                       'AUU': 'I', 'UUG': 'L', 'UUA': 'L', 'CGC': 'R', 'UUC': 'F', 'UAA': '*', 'UGA': '*', 'UAG': '*',
                       'AUC': 'I'}


def load_genome_filepath(filepath):
    """
    Set up genomic filepath.
    :param filepath: str;
    :return: None
    """

    global GENOME_FILEPATH
    GENOME_FILEPATH = filepath


def list_available_contigs():
    """
    List contigs in the genome.
    :return: list; list of contig
    """
    pass


def get_dna_sequence(chromosome, start, end):
    """
    Return genomic sequences from region specified by chromosome:start-stop.
    :param chromosome: int or str; chromosome
    :param start: int or str; start position
    :param end: int or str; end position; must be greater than or equal to start position
    :return: str; genomic sequences from region specified by chromosome:start-stop
    """

    return query_genome(GENOME_FILEPATH, chromosome, start, end)


def query_genome(filepath, chromosome, start, end):
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
