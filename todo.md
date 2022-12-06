# TO DO

## TO PUSH IN PRODUCTION
- update python 
- update compdes
- add version in help page

## URGENT
- check source id pull from the drugbank value
- ~~1-25-2022: update link to dsstox from the map~~
- ~~fix static file and check with docker version~~
- ~~fix duplicate code for DB interaction~~
- ~~Add QC data in bodymap~~
- ~~Integrate tox21 assays results in chemmaps~~
- ~~connection / close DB change in all of the project!!!~~
- ~~Error in the name map for user page~~
- ~~check adding in DB for descriptor user computation~~
- ~~add new descriptor from OPERA 2.6 in the opera desc list +> integrated in CompDesc~~
- load only once OPERA model
- ~~add -999 value in case of descriptor NA~~
- ~~remove descriptors in interpred~~
- ~~create random int for folder for update in descriptor~~
- ~~clean update folder~~ 
- ~~check error in line 48 of interpred R script~~
- ~~add error page in the project to hide sources~~
- add when upload chemical add log
- ~~add descriptor scaling in a table => keep with static~~
- protect page admin with a password
- Add option to not upload chemical in the DB as interpred
- merge VM_prod and check path server
- change page head to have the name of the tool in it
- ~~check PNG and color and size on the map when draw chemical~~
- centralize all DB requests on a class - currently many duplicate


### ChemMaps
#### Urgent 
- ~~Fix JS connect neighbor error when it is a uploaded chemicals -> done~~
- ~~Add DSSTOX in the DB and split map -> done use DB request and not split~~
- ~~Add command to upload a new chemical on the fly in the DB -> done~~
- ~~fix check in input and QSAR ready (09-20) -> done~~
- ~~fix table in case of very long chemical and size of the check figure -> done~~
- ~~Add option to load characteristic on the map~~
- ~~Fix the help page~~
- ~~For 508 change font tab~~
- ~~NaN in the panel tab~~
- ~~DrugMap png missing~~
- ~~508 add logo NTP on the map~~
- ~~07-11: error in load DSSTOXMAP~~ 
- ~~change contact information~~
- ~~Fix error with connect neighboor => change intersect JS~~
- ~~check case of chemical on drugmap and other map~~
- ~~Fix error with metal~~
- ~~downloadDescFromDB, line 223 ERROR in coordinate run ==> need to check it is working~~
- Add option to not load in the DB the new chemicals as interferences
- ~~fix error on map in case of GHS is empty~~
- ~~check range color~~
- ~~check in assay results if new_hitc is checked~~ 
- check double computer function call in views chemmaps
- fix error with draw - not the good chemicals is draw
- remove all links with the png folder

#### Improvement
- ~~Add distance in the neighbor file to download -> done~~
- Compute the 3D plan with several different plan
- ~~change background in function of the map~~
- develop a carciMap choose on the 1600 chemicals and 1600 chemicals on the DSSTOX 
- ~~Change color when chemicals are uploaded and rocket size~~
- ~~italic for the article hyperlink + color blue~~
- Change the center of the map for the tox21map


### Interferences
#### Urgent
- ~~Connect to a DB to increase speed~~
- ~~Update the descriptor computation and add a table of name from previous / new version (or reload model)~~
- ~~add header and footer for all of the page -> done~~
- ~~proof read page~~
- ~~check the 508~~
- ~~redo table for contrast and connect to the DB to save time of computation~~
- ~~remove MD compute inside the interferences code and make a table of connect for version 2.7 descriptor name and 3.6~~
- ~~Fix error reach several time the DB~~
- ~~case of name in input => add a regex before reach the DB~~
- ~~Add pop up for revision~~
- ~~Add link to Rmodel compressed and script R~~ 
- ~~Fix upload file path fail~~

#### Improvement
- ~~Add in the table if the chemical is included in the trainning set~~
- Add a cross link with chemmaps and add an option


### BodyMap
#### Urgent
- ~~Add footer and header on each page -> done~~
- ~~Update the mapping with the assays mapping -> done~~
- ~~Fix a mapping on a body -> done~~
- ~~develop network mapping~~
- ~~fix the results page to generalize table~~
- ~~Add the body mapping~~ 
- ~~fix legend barplot and inspect color => no real solution~~
- ~~change body pictures~~
- ~~fix highlight tab opened~~
- ~~fix download table~~
- ~~color dot on mapping gene map vs tissue map~~
- ~~add gene expression on table~~
- ~~add legend for network and bodymap dot~~
- ~~add link to chemmaps~~
- ~~add a tool tip: <em>"Ratio of specific tissue expression to all tissues for assay gene target. Higher cutoff = greater specificity"</em>~~
- ~~make a autocomplete form~~
- ~~write home and help pages~~
- ~~label organs directly on the png~~
- ~~add name of the chemical on the network => added name in the autocompletion form~~
- ~~correct the chemical selection to chose a chemical by name, repetition, alphabetic order~~
- ~~add one color for the mapping in case of mapping using both tissues and gene~~
- ~~correct the barplot~~
- ~~improve the network by adding some cutoff on the AC50 and gene expression.~~


### Development of a admin toolbox
- ~~update chemical DB~~  
- ~~update coordinates for the all map~~ 
- ~~control DB with entries and quality~~
- ~~compute on the fly descriptor and OPERA prediction~~

