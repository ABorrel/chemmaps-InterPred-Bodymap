# Dependancies

## installtion with pip -> computation descriptor RDKIT developed in parrallel
$pip install -i https://test.pypi.org/simple/ CompDesc

## lib and sofwares
Development in python3.6 with
- Django
- RDKit (> 3.1): http://rdkit.org/docs/index.html
- molVS (> 1): https://molvs.readthedocs.io/en/latest/index.html
- Open Babel > 3.0.0 (March 2020): (http://openbabel.org/wiki/Main_Page) (sudo apt install openbabel) or https://open-babel.readthedocs.io/en/latest/Installation/install.html#compiling-open-babel 
(additional some function will not work in case of no install)
- OPERA2.3_CL (https://github.com/kmansouri/OPERA/releases), fix the minor error in the install folder add a "/" at the path beginning
- OPERA will install PADEL in the same folder

## Upade the DSSTOX
Download chemicals from the pubchem
Current download => 866794 chemicals => limited to 500,000 structures
- https://www.ncbi.nlm.nih.gov/pcsubstance?term=%22EPA%20DSSTox%22%5BSourceName%5D%20AND%20hasnohold%5Bfilt%5D
- with the mapping from the pubmed ID


# Keys updates 
- 7-8-19: init ncsu git
- 7-8-19: add gitignore to no include png in chemmaps
- 9-8-19: Error interferences, revert on sandbox version
- 18-8-19: Fix ChemMaps for VM and create git tree
- 22-8-19: Add bodyMap project
- 23-8-19: develop bodyMap
- 17-9-19: Add version 17-9-19 of molecular descriptors computation
- 19-9-19: connect chemmaps on DB
- 20-9-19: Fix case where chemicals uploaded are a mix between in DB and new
- 08-10-19: Update footer and header for interference and chemmaps + connect pfas and tox21 to DB
- 11-10-19: Add Connection to server and optimize the DSSTOX map
- 18-10-19: Update body map and change statics
- 21-10-19: Fix Tox21 map error, add distance in the neighbor download and fix search bar error
- 23-10-19: Fix extraction for DrugMap, optimize the loading in case of pre existing chemical, add DB interactions 
- 5-11-19: Update barplot for AC50 and added chemical informatio
- 20-11-19: Update bodymap results pages
- 01-12-19: Update bodymap
- 16-12-19: connected bodymap to DB
- 18-12-19: Fix error in chemmaps with user DB
- 19-12-19: Fix error meighbor dl + fix NaN in the info panel
- 19-12-19: add help and index pages for bodymap
- 20-12-19: Fix color link bodymap + error upload chemmaps
- 20-12-19: Fix error replicate in chemmaps user DB
- 25-01-20: last update from the NTP
- 26-03-20: fix error bodymap and chemmaps as well as added option in bodymap for interactive network
- 21-04-20: Fix error in case of O division in gene expression
- 21-04-20: Fix spealing errors and add ratio assays tested
- 09-20: add ILS ICE data
- 12-20: update bodymap with the assays results from ICE and QC 
- 18-05-21: fix map navigation bug on color and selection 
- 4-13-22: Fix help page