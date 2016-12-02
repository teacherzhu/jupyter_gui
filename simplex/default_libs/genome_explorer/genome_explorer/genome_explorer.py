import gzip
from os import environ, remove, rename
from os.path import join, isfile, isdir
from subprocess import run, PIPE

from Bio import bgzf

# ======================================================================================================================
# Parameters
# ======================================================================================================================
PATH_HOME = environ['HOME']

PATH_TOOLS = join(PATH_HOME, 'tools')
PATH_DATA = join(PATH_HOME, 'data')

# Java
PICARD = 'java -Xmx{}g -jar {}'.format(12, join(PATH_TOOLS, 'picard.jar'))
SNPEFF = 'java -Xmx{}g -jar {}'.format(12, join(PATH_TOOLS, 'snpEff', 'snpEff.jar'))
SNPSIFT = 'java -Xmx{}g -jar {}'.format(12, join(PATH_TOOLS, 'snpEff', 'SnpSift.jar'))

# Reference genome assemblies
PATH_HG38 = join(PATH_DATA, 'grch', '38', 'sequence', 'hg', 'hg38.unmasked.fa.gz')
PATH_GRCH38 = join(PATH_DATA, 'grch', '38', 'sequence', 'primary_assembly',
                   'Homo_sapiens.GRCh38.dna.primary_assembly.fa.gz')
PATH_GENOME = PATH_GRCH38

# Genome assembly chains
PATH_CHAIN_HG19_TO_HG38 = join(PATH_DATA, 'grch', 'genomic_assembly_chain', 'hg19ToHg38.over.chain.gz')
PATH_CHAIN_GRCH37_TO_GRCH38 = join(PATH_DATA, 'grch', 'genomic_assembly_chain', 'GRCh37_to_GRCh38.chain.gz')

# ClinVar
PATH_CLINVAR = join(PATH_DATA, 'grch', '38', 'variant', 'clinvar.vcf.gz')

# DBSNP
PATH_DBSNP = join(PATH_DATA, 'grch', '38', 'variant', '00-All.vcf.gz')

# Chromosomes
CHROMOSOMES = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19',
               '20', '21', '22', 'M', 'MT', 'X', 'Y']
CHROMOSOMES_CHR = ['chr' + c for c in CHROMOSOMES]
PATH_CHROMOSOME_MAP = join(PATH_DATA, 'grch', 'grch_chromosome_map.txt')

for p in [PATH_HOME, PATH_TOOLS, PATH_DATA, PATH_HG38, PATH_GRCH38, PATH_CHAIN_HG19_TO_HG38,
          PATH_CHAIN_GRCH37_TO_GRCH38, PATH_CLINVAR, PATH_DBSNP, PATH_CHROMOSOME_MAP]:
    if not (isdir(p) or isfile(p)):
        raise ValueError('File {} doesn\'t exists.'.format(p))

CODON_TO_AMINO_ACID = {'GUC': 'V', 'ACC': 'T', 'GUA': 'V', 'GUG': 'V', 'GUU': 'V', 'AAC': 'N', 'CCU': 'P', 'UGG': 'W',
                       'AGC': 'S', 'auc': 'I', 'CAU': 'H', 'AAU': 'N', 'AGU': 'S', 'ACU': 'T', 'CAC': 'H', 'ACG': 'T',
                       'CCG': 'P', 'CCA': 'P', 'ACA': 'T', 'CCC': 'P', 'GGU': 'G', 'UCU': 'S', 'GCG': 'A', 'UGC': 'C',
                       'CAG': 'Q', 'GAU': 'D', 'UAU': 'Y', 'CGG': 'R', 'UCG': 'S', 'AGG': 'R', 'GGG': 'G', 'UCC': 'S',
                       'UCA': 'S', 'GAG': 'E', 'GGA': 'G', 'UAC': 'Y', 'GAC': 'D', 'GAA': 'E', 'AUA': 'I', 'GCA': 'A',
                       'CUU': 'L', 'GGC': 'G', 'AUG': 'M', 'CUG': 'L', 'CUC': 'L', 'AGA': 'R', 'CUA': 'L', 'GCC': 'A',
                       'AAA': 'K', 'AAG': 'K', 'CAA': 'Q', 'UUU': 'F', 'CGU': 'R', 'CGA': 'R', 'GCU': 'A', 'UGU': 'C',
                       'AUU': 'I', 'UUG': 'L', 'UUA': 'L', 'CGC': 'R', 'UUC': 'F', 'UAA': '*', 'UGA': '*', 'UAG': '*',
                       'AUC': 'I'}


# ======================================================================================================================
# File functions
# ======================================================================================================================
def mark_filename(filename, mark, suffix='.vcf'):
    """

    :param filename: str;
    :param mark: str;
    :param suffix: str;
    :return: str;
    """

    if suffix in filename:
        i = filename.find(suffix)
        filename = filename[:i] + '.' + mark + filename[i:]
        if filename.endswith('.gz'):
            filename = filename[:-len('.gz')]
    else:
        filename = filename + '.' + mark + suffix

    return filename


# ======================================================================================================================
# File operations
# ======================================================================================================================
def bgzip_tabix(fname):
    """
    bgzip and tabix <fname>.
    :param fname:
    :return:
    """

    if fname.endswith('.gz'):
        return fname
    bgzip_output_fname = bgzip(fname)
    tabix(bgzip_output_fname)

    return bgzip_output_fname


def bgzip(fname):
    """
    bgzip <fname>.
    :param fname:
    :return:
    """

    cmd = 'bgzip -f {}'.format(fname)
    print(cmd)
    run(cmd, shell=True, check=True)

    return fname + '.gz'


def tabix(fname):
    """
    tabix <fname>.
    :param fname:
    :return:
    """

    cmd = 'tabix -f {}'.format(fname)
    print(cmd)
    run(cmd, shell=True, check=True)

    return fname + '.tbi'


def convert_gzipped_to_bgzipped(gzipped_filename):
    """

    :param gzipped_filename:
    :return: None
    """

    temp_filename = gzipped_filename + '_temp'
    with gzip.open(gzipped_filename, 'rt') as gzipped_file:
        with bgzf.open(temp_filename, 'wt') as temp_bgzipped_file:
            for line in gzipped_file:
                temp_bgzipped_file.write(line)
    remove(gzipped_filename)
    rename(temp_filename, gzipped_filename)


# ======================================================================================================================
# Sequence functions
# ======================================================================================================================
def dna_to_rna(dna_sequence):
    """

    :param dna_sequence: str;
    :return: str;
    """

    return dna_sequence.replace('T', 'U')


def rna_to_dna(rna_sequence):
    """

    :param rna_sequence: str;
    :return: str;
    """

    return rna_sequence.replace('U', 'T')


def rna_to_aa(rna_sequence, codon_to_aa=CODON_TO_AMINO_ACID):
    """

    :param rna_sequence: str;
    :param codon_to_aa: dict;
    :return: str;
    """

    aa = ''
    for i in range(len(rna_sequence) - 2):
        codon = rna_sequence[i:i + 3]
        aa += codon_to_aa[codon]
    return aa


# ======================================================================================================================
# FASTA operations
# ======================================================================================================================
def load_fasta(filepath):
    """
    Set up genomic filepath.
    :param filepath: str;
    :return: None
    """

    global PATH_GENOME
    PATH_GENOME = filepath


def get_dna_sequence(chromosome, start, end):
    """
    Return genomic sequences from region specified by chromosome:start-stop.
    :param chromosome: int or str; chromosome
    :param start: int or str; start position
    :param end: int or str; end position; must be greater than or equal to start position
    :return: str; genomic sequences from region specified by chromosome:start-stop
    """

    return fasta_get_sequence(PATH_GENOME, chromosome, start, end)


def fasta_get_sequence(filepath, chromosome, start, end):
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
    stdout = run(cmd, shell=True, check=True, stdout=PIPE, universal_newlines=True).stdout

    s = ''.join(stdout.split('\n')[1:])

    return s


# ======================================================================================================================
# VCF operations
# ======================================================================================================================
def vcf_concat_sort(fnames, output_fname):
    """
    Concatenate VCFs <fnames> using BCFTools concat and sort.
    :param fnames:
    :param output_fname:
    :return: str;
    """

    output_fname = mark_filename(output_fname, 'concat_sort')
    fnames = [bgzip_tabix(fn) for fn in fnames]

    cmd = 'bcftools concat -a ' + ' '.join(fnames) + ' > {}'.format(output_fname)
    print(cmd)
    run(cmd, shell=True, check=True)

    return bgzip_tabix(output_fname)


def vcf_remap_37to38(fname):
    """
    Re-map genomic coordinates of <fname> based on GRCh38 using picard LiftoverVcf.
    :param fname:
    :return: None
    """

    mark = '37to38'
    output_fname = mark_filename(fname, mark)
    reject_fname = mark_filename(fname, mark + '_rejected')
    cmd = '{} LiftoverVcf INPUT={} OUTPUT={} REJECT={} CHAIN={} REFERENCE_SEQUENCE={}'.format(PICARD,
                                                                                              fname,
                                                                                              output_fname,
                                                                                              reject_fname,
                                                                                              PATH_CHAIN_HG19_TO_HG38,
                                                                                              PATH_HG38)
    print(cmd)
    run(cmd, shell=True, check=True)

    return bgzip_tabix(output_fname)


def vcf_rename_chr_sort(fname):
    """
    Rename chromosomes.
    :param fname:
    :return:
    """

    output_fname = mark_filename(fname, 'rename_chr_sort')
    fname = bgzip_tabix(fname)

    cmd = 'bcftools annotate --rename-chrs {} {} -o {}'.format(PATH_CHROMOSOME_MAP, fname, output_fname)
    print(cmd)
    run(cmd, shell=True, check=True)

    return bgzip_tabix(output_fname)


def vcf_extract_chr(fname, chromosome_format):
    """
    Extract chromosome 1 to 22, X, Y, and MT from <fname>, and bgzip and tabix the extracted VCF.
    :param fname:
    :param chromosome_format:
    :return:
    """

    output_fname = mark_filename(fname, 'extract_chr')
    fname = bgzip_tabix(fname)

    cmd_template = 'bcftools view -r {} {} -o {}'
    if chromosome_format == 'chr#':
        cmd = cmd_template.format(','.join(CHROMOSOMES_CHR), fname, output_fname)
    elif chromosome_format == '#':
        cmd = cmd_template.format(','.join(CHROMOSOMES), fname, output_fname)
    else:
        raise ValueError('Chromosome format {} not found in (chr#, #)'.format(chromosome_format))
    print(cmd)
    run(cmd, shell=True, check=True)

    return bgzip_tabix(output_fname)


def vcf_snpeff(fname):
    """
    Annotate VCF <fname> using SNPEff.
    :param fname:
    :return:
    """

    output_fname = mark_filename(fname, 'snpeff')

    fname = bgzip_tabix(fname)

    cmd = '{} -noDownload -v -noLog -s {}.html GRCh38.82 {} > {}'.format(SNPEFF,
                                                                         output_fname[:-len('.vcf')],
                                                                         fname,
                                                                         output_fname)
    print(cmd)
    run(cmd, shell=True, check=True)

    return bgzip_tabix(output_fname)


def vcf_snpsift(fname, annotation):
    """
    Annotate VCF <fname> using SNPSift.
    :param fname:
    :param annotation: str; {clinvar, dbsnp}
    :return: str;
    """

    if annotation == 'clinvar':
        mark = 'clinvar'
        path_annotation = PATH_CLINVAR
        flag = ''

    elif annotation == 'dbsnp':
        mark = 'dbsnp'
        path_annotation = PATH_DBSNP
        flag = '-noInfo'

    else:
        raise ValueError('annotation has to be one of {clinvar, dbsnp}.')

    output_fname = mark_filename(fname, mark)

    fname = bgzip_tabix(fname)

    cmd = '{} annotate -noDownload -v -noLog {} {} {} > {}'.format(SNPSIFT, flag, path_annotation, fname, output_fname)
    print(cmd)
    run(cmd, shell=True, check=True)

    return bgzip_tabix(output_fname)


def vcf_annotate(fname, pipeline):
    """
    Annotate <fname> VCF with SNPEff and ClinVar (SNPSift).
    :param fname: str;
    :param pipeline: str;
    :return: None
    """

    if pipeline == 'dbsnp-snpeff-clinvar':
        print('\n**************************************************************************')
        output = vcf_snpsift(fname, 'dbsnp')
        print('\n**************************************************************************')
        output = vcf_snpeff(output)
        print('\n**************************************************************************')
        vcf_snpsift(output, 'clinvar')

    elif pipeline == 'snpeff-clinvar':
        print('\n**************************************************************************')
        output = vcf_snpeff(fname)
        print('\n**************************************************************************')
        vcf_snpsift(output, 'clinvar')

    else:
        raise ValueError('annotation has to be one of {dbsnp-snpeff-clinvar, snpeff-clinvar}.')
