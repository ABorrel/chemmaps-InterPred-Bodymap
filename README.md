# To do list

### For all projects
- ~~Update the MD directory => created an alternative branch~~

### ChemMaps
#### Urgent 
- ~~Fix JS connect neighbor error when it is a uploaded chemicals -> done~~
- ~~Add DSSTOX in the DB and split map -> done use DB request and not split~~
- ~~Add command to upload a new chemical on the fly in the DB -> done~~
- ~~fix check in input and QSAR ready (09-20) -> done~~
- 508 html for all pages
- ~~fix table in case of very long chemical and size of the check figure -> done~~
- Add option to load characteristic on the map
- Fix the help page
- ~~For 508 change font tab~~
- ~~NaN in the panel tab~~
- ~~DrugMap png missing~~
- ~~508 add logo NTP on the map~~
- ~~07-11: error in load DSSTOXMAP~~ 
- change contact information
- ~~Fix error with connect neighboor => change intersect JS~~
- ~~check case of chemical on drugmap and other map~~
- ~~Fix error with metal~~


#### Improvement
- ~~Add distance in the neighbor file to download -> done~~
- Compute the 3D plan with several different plan
- change background in function of the map
- develop a carciMap choose on the 1600 chemicals and 1600 chemicals on the DSSTOX 
- Change color when chemicals are uploaded and rocket size


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
- Add in the table if the chemical is included in the trainning set
- Add a cross link with chemmaps and add an option


### BodyMap
#### Urgent
- ~~Add footer and header on each page -> done~~
- ~~Update the mapping with the assays mapping -> done~~
- ~~Fix a mapping on a body -> done~~
- ~~develop network mapping~~
- ~~fix the results page to generalize table~~
- check the 508 -> email to beth
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


#### Improvement
- ~~Develop a new scrolling bar~~

# Updates 
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
- 15-01-20: Kyle committed docker related commits to Gitlab. Still WIP after receving QA feedback from Beth + Alex

# Deployment Strategy
- Replace dot files ".env.example" and ".env.db.example" with ".env" and ".env.db"
- Fill in new dot file environment variables with db creds and app specific values (Do not add track with Git!)
- Files not included (but are necessary) in repository:
    * marvin_linux_20.1_openjdk11.deb
    * OPERA2.4_CL_mcr.tar.gz
    * ChemMap_Dec.dump
- The aforementioned files can be found via Github and/or by emailing Kyle Johnson (johnson.kyle272@gmail.com)
- Docker related components created before docker-compose execution:
    * Volume: `docker volume create chem_db_vol`
- After building postgres image, if the database volume is empty, two steps are needed:
    * Create roles and import data
    * (Use psql within postgres container to feed .sql file containing DDL to database)
- Build images and run containers in the background
    * `docker-compose up -d --build`
- Check their status:
    * `docker-compose ps`
- Note: The source code is mounted into the container for development purposes only
