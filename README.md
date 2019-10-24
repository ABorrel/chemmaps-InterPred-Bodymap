# To do list
### ChemMaps
#### Urgent 
- Fix JS connect neighbor error when it is a uploaded chemicals -> done
- Add DSSTOX in the DB and split map -> done use DB request and not split
- Add command to upload a new chemical on the fly in the DB -> 50%
- develop a carciMap choose on the 1600 chemicals and 1600 chemicals on the DSSTOX 
- fix check in input and QSAR ready (09-20)
- 508 html
- fix table in case of very long chemical and size of the check figure

#### Improvement
- Add distance in the neighbor file to download -> done
- Compute the 3D plan with several different plan
- Connect the DB with the JS to improve speed
- change background in function of the map


### Interferences
#### Urgent
- Connect to a DB to increase spead
- Update the descriptor computation and add a table of name from previous / new version (or reload model)
- add header and footer for all of the page

#### Improvement
- Add in the table if the chemical is included in the trainning set
- Add a cross link with chemmaps and add an option


### BodyMap
#### Urgent
- Add footer and header on each page -> done
- Update the mapping with the assays mapping -> done
- Fix a mapping on a body -> done
- develop the chemical mapping
- fix the results page
- check the 508


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

