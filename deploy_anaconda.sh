# NOTE: DO NOT RUN. ONLY USE AS REFERENCE.
# Anaconda Deploy
conda install conda-build
conda upgrade conda
conda upgrade conda-build

# Build conda package from pypi package
conda skeleton pypi simpli
conda build simpli # inside conda recipe folder

anaconda login
anaconda upload ~/anaconda3/conda-bld/src_cache/simpli-1.0.0a2.tar.gz