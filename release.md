# ChemMaps - Interpred -Tox21BodyMap V.3
Release version 3 - Scheduled April 2021

## Dependency updates
- OPERA 2.3 -> 2.6
- openbabel 2.3 -> 3.3
- rdkit 2019 -> 2021
- Extract chemical preparation and chemical descriptor computation from original project and develop a pip package (CompDesc) available in the test pip plateform https://test.pypi.org/simple/CompDesc

## Database update
- 

## Develop an interface for update the chemical database
- Compute rdkit based descriptor and opera based descriptor on the fly
- Compute interpred descriptor on the fly
- Compute map coordinates on the fly
- Include function to update the database using csv files
- Clean static files to included all of them in the DB
- Add a count of chemicals included in the database 


## Update in ChemMaps v3
### Major Updates
- Update the internal dsstox database (+100,000 chemicals) using the DSSTOX release 2020
- Update database architecture, added chemicals without a QSAR ready structure and descriptor fail (to be sync with the NTP database effort)
- Add projection of the Tox21 assays results on the Tox21Map (from ICE effort) and combine assay results 
- Merged Tox21 assay results based on assay target available in the Tox21BodyMap
- Develop interactive url with chemicals / assays name and assays target for a cross plateform
- improve DB requests, improve speed and open/close process

### Minor update
- Update help pages and general website design to fit better with the NTP template
- Change map backgrounds and add name on map
- Add ntp logo in the map
- Increase chemicals size in the map
- Change default map descriptors
- Add number of chemicals on the map


## Update in Tox21BodyMap v1.1
- Integrate QC status from ICE effort in the results page
- Process results only if te QC passed
- Add in results page the number of assay tested

## Update in interpred v1.1
- Compute descriptor using the CompDesc packages
- Add in the results page if chemicals are included in the training set
