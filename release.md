# ChemMaps - Interpred -Tox21BodyMap V.3
Release version 3 - Scheduled April 2021

## Dependency updates
- python3.5 -> python 3.9
- django-3.0 -> django-3.2
- OPERA 2.3 -> OPERA 2.6
- openbabel 2.3 -> 3.3
- rdkit 2019.3 -> 2021.3
- marvin - Chemaxon 18.4 -> marvin - Chemaxon 21.4
- R-3.X -> R-4.0.3
- Extract chemical preparation and chemical descriptor computation from original project and develop a pip package (CompDesc) available in the test pip plateform https://test.pypi.org/simple/CompDesc


## Database updates
- add ICE tox21 assays results cleaned (ice_tox21)
- reorganize bodymap tables to remove statics files (bodymap_*)
- update list of OPERA's descriptors to include not physico-chemical prediction available in OPERA2.6 (CERRAP, CATMOS, ...) (chem_descriptor_opera_name)
- redefine materialized views to catch OPERA descriptor
- new tables with only experimental tox value and drugbank properties (chem_toxexp_value and chem_toxexp_name) and drugbank prop values (chem_prop_drugbank_value and chem_prop_drugbank_name)
- Add chemicals excluded in the first chemmaps version and missing chemicals

## Develop an interface for update the chemical database
- compute a database summary 
- Compute rdkit based descriptor and opera based descriptor on the fly
- Compute interpred descriptor on the fly
- Compute map coordinates on the fly
- compute map neighbors on the fly
- Include function to update the database using csv files
- Add a count of chemicals included in the database 


## Update in ChemMaps v3
### Major Updates
- Update the internal dsstox database (+100,000 chemicals) using the DSSTOX release 2020
- Update database architecture, added chemicals without a QSAR ready structure and descriptor fail (to be sync with the NTP database effort)
- Add projection of the Tox21 assays results on the Tox21Map (from ICE effort) and combine target based assays 
- Merged Tox21 assay results based on assay target available in the Tox21BodyMap
- Develop interactive url with chemicals / assays name and assays target for a cross plateform
- improve DB requests, improve speed with optimize open/close database and a better definition of the materialized view

### Minor update
- Update help pages and general website design to fit better with the NTP template
- Change map backgrounds and add map name on the map and number of chemicals projected
- Add ntp logo in the map
- Increase stars size on the map
- Change default map descriptors


## Update in Tox21BodyMap v2
- Integrate QC status from ICE in the results page
- Process results only if the QC passed
- Add in results page the number of assay tested
- Use ICE tox21 assay results instead of invitroDB

## Update in interpred v2
- Compute descriptor using the CompDesc packages and OPERA 2.6
- Add in the results page if a chemical is included in the training set


## TO CHECK IN PRODUCTION
- link to the png folder and case where chemicals are added => link to static/png (search text "// TO CHECK IN PRODUCTION" )