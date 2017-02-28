<h1><center>Notebook Package (NbPackage) Template</center></h1>
<h3><center>This repository is a NbPackage template, ready to be downloaded/cloned and used to develop your own project or analysis!</center></h3>
<h2>What is an NbPackage?</h2>

An NbPackage is an organizational unit built around Jupyter Notebooks. The purpose of an NbPackage is to enable __developers__ to quickly create, share, and publish their work while allowing __users__ to run Jupyter notebooks seconds after they download/clone them. 

<center> <img align="center" width="500" alt="screen shot" src="https://cloud.githubusercontent.com/assets/20215501/22957136/39197c02-f2db-11e6-8549-ecf21c054dad.png">

But, how is this possible? NbPackages come with all the data, tools, and media needed to run the Jupyter notebooks they contain, so users dont need to download any data or install any software to run the notebooks. NbPackages also use relative paths, so users dont have to change any code to get the notebooks to run.

<h2>How to build an NbPackage for your own project</h2>

1) Continue reading below about the NbPackage if you haven't used it before.

2) Download or clone this repository. (Where you download/clone it does not matter)

3) Rename the notebook package template to the name of your project.

4) If __you already have one or more Jupyter notebooks for this project__, move it/them into the notebooks folder of your NbPackage. If you're starting from scratch, use Notebook_1 in the notebooks folder to begin your project.

5) Move materials you'll want to use in this project into their corresponding folders. All of these materials should be used by the Jupyter notebooks that are developed in the notebooks folder of this NbPackage. Move the data you want to use for your project into the data folder. Move any images, videos, .css files, or any other design related files into the media folder. Finally, move any libraries, executables, or other software tools into the tools folder. 

6) Take a look at environment.py in the notebooks folder. As you can see in Notebook_1, you can easily import environment.py into all your Jupyter notebooks in the notebooks folder. Therefore, if there are specific tools or packages you would like imported into each notebook, add them to the project-specific parameters section in the environment.py file in the notebooks folder.

7) Take a look at how Notebook_1 in the notebooks folder uses vairables like DIR_DATA and DIR_RESULTS to import data and set result filepaths. Use this style in your existing Jupyter notebooks for this project.

8) The fun part: customize notebook header and footer. If you use the markdown code thats used to display the header and footer in Notebook_1 in your Jupyter notebooks in the notebooks folder, you can simply change the names of the images in the media folder to.

9) Enjoy the NbPackage structure and change the world with the analysis you develop!


<h2>Terminology</h2>
* [Simpli](https://github.com/UCSD-CCAL/simpli)
    * Simpli is a Jupyter Notebooks extension that makes computational biology and bioinformatics simple. If you use a Jupyter notebook that's within an NbPackage, Simpli will work with the NbPackage structure to improve your experience. \
* NbPackage Manager
    * An application that organizes NbPackages and allows users to search for the NbPackages they want.
* How-to NbPackage
    * A notebook package that teaches and provides templates for a given bioinformatics or computational biology task like finding differential gene expression. See the [how_to_differential_gene_expression](https://github.com/UCSD-CCAL/how_to_differential_gene_expression) for an example of a How-to NbPackage.
* Publication NbPackage
    * A notebook package that performs the analysis of a research project or research paper. See the [discover](https://github.com/UCSD-CCAL/discover) NbPackage, which details the analysis performed in the [DiSCoVER](http://clincancerres.aacrjournals.org/content/early/2016/03/24/1078-0432.CCR-15-3011) method paper, for an example of a Publication NbPackage.

<h2>NbPackage structure</h2>
The NbPackage is a folder that contains the following five folders: notebooks, data, media, tools, and results. Below the contents and function of each is explained.The italicized files aren't included in the Notebook Package Template, but represent other files commonly used in NbPackages.

<h3>notebooks</h3>
* Notebook_1.ipynb
* *Notebook_2.ipynb*
* environment.py

The notebooks folder contains the Jupyter notebooks that perform the analysis of the NbPackage. There may be one or many Jupyter notebooks here. The notebooks folder also contains an environment.py file, which contains code that sets up the Jupyter notebooks in the notebooks folder. If you have [Simpli](https://github.com/UCSD-CCAL/simpli) installed, it will atuomatically import environment.py when you open a Jupyter notebook in the notebooks folder.

<h3>data</h3>
* *data_1.gct*
* *data_2.xlsx*
* *data_3.txt*

The data folder contains the data used by the Jupyter notebooks in the notebooks folder. If the data is very large, a data importer can be added to the data folder.

<h3>media</h3>
* header_banner.png  
* header_logo_1.png
* header_logo_2.png
* header_logo_3.png
* header_logo_4.png
* *diagram.png*
* *unique.css*
* footer_banner.png

The media folder contains  images, logos, videos, custom.css, or other design related files that can improve the look and usability of the Jupyter notebooks in the notebooks folder. The Notebook Package Template provides default banners and logos that Simpli, if installed, will automatically display in the Jupyter notebooks in the notebooks folder. Simpli looks looks into the media folder of an NbPackage and displays the files named header_banner, header_logo_1, header_logo_2, header_logo_3, and header_logo_4 like so at the top of the page. 

Simpli also looks for a file named footer_banner in the media folder, which it displays at the bottom of the Jupyter notebooks in the notebooks folder. 

<h3>tools</h3>
* ccal
* *library_2*
* *tool.py*
* *executable_file*

The tools folder contains the software (libraries, .py files, executables) used by the Jupyter notebooks in the notebooks folder. The Notebook Package Template contains the [CCAL](https://github.com/UCSD-CCAL/ccal), or the Computational Cancer Analysis Library, for convenience.  

<h3>results</h3>
* *results_1.pdf*
* *results_2.gct*

The results folder contains the results produced by the Jupyter notebooks in the notebooks folder.
