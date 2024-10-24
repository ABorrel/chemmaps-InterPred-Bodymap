# TO DO
- readme --> add sources of chemical Tox21 - https://tripod.nih.gov//tox21/pubdata/
- release version readme file
## TO PUSH IN PRODUCTION
- update python 
- update compdes
- add version in help page
- Update help page with the chemical map
- cookie form - not checking cookie but ask for autorisation 
- update OPERA with 2.8 - check the current version
> install with 
pip install git+https://github.com/jazzband/django-cookie-consent@master#egg=django-cookie-consent


## Overhall: Priority high
- check source id pull from the drugbank value
- load only once OPERA model
- add when upload chemical add log
- protect page admin 
- Add option to not upload chemical in the DB as interpred
- change page head to have the name of the tool in it
- centralize all DB requests on a class - currently many duplicate


### ChemMaps
#### Priority high
- Add option to not load in the DB the new chemicals as interferences
- check double computer function call in views chemmaps
- fix error with draw - not the good chemicals is draw
- remove all links with the png folder

#### Priority low
- Compute the 3D plan with several different plan
- Change the center of the map for the tox21map


### Interferences
#### Priority high
- Add Applicability domain in prediction
#### Priority low
- Add a cross link with chemmaps and add an option


### BodyMap
#### Priority high
- redone chemsum with proper chemical name


### Priority low

