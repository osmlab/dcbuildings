# DC building and address import

*Proposal to finalize DC building and address import*

- Supporter 1
- @andinocl
- @mikelmaron
- Alex Barth

## Introduction

The DC building import was started in 2008. The effort trailed off in 2010 
leaving the DC map with a third of the buildings unimported. This proposal
aims to finalize the import in a manual, community based fashion.

![](http://www.sixpica.com/osm/wp-content/uploads/2013/05/Screen-Shot-2013-05-19-at-11.08.44-PM-1024x640.png)

*Remaining, unimported buildings in Washington DC (Map: [Chris Andino](http://www.sixpica.com/osm/2013/05/19/scope-of-work-cool-new-tools/))*

## Review

Please review:

- Data conflation
- Upload process
- OSM file quality

## Data

- [Address Points](http://data.dc.gov/Metadata.aspx?id=190)
- [Buildings](http://data.dc.gov/Metadata.aspx?id=59)
- [Terms of Use](http://data.octo.dc.gov/TermsOfUse.aspx)
- [Explicit import permission](http://lists.openstreetmap.org/pipermail/talk-us/2008-October/000388.html)

[![](http://cl.ly/image/3b1j2P3E0r1r/Screen%20Shot%202013-08-04%20at%203.08.51%20PM.png)](http://a.tiles.mapbox.com/v3/lxbarth.map-luuf96x5/page.html)

*Highly accurate DC building data [(slippy map)](http://a.tiles.mapbox.com/v3/lxbarth.map-luuf96x5/page.html)*

## Process

- Process DC shapefiles into census tract size OSM files
- Review by local DC community and import-us working group
- Upload data in a community based process, kicking off with a session at the
  OSM birthday sprint.

## Timeline

- Proposal review July 29 - Aug 9 2013
- Test imports Aug 10 2013 (OSM birthday sprint)
- Import period Mid Aug - End of October 2013 (Fall editathon)

## Conversion code

We have created scripts that process DC building and address shapefiles into
small chunks of OSM files. They relate addresses to buildings, concatenate
and clean up addresses and export addresses separate from buildings where
more than one address relates to a building. The script simplifies building
polygons and handles multipolygons.

- See all details in the script's [README](https://github.com/osmlab/dcbuildings).
- Sample: Building and address OSM file ready for manual review and upload for
  census tract 000100: http://cl.ly/463r3N0B1q0a
- Sample: Full export of all cleaned and concatenated addresses:
  http://cl.ly/3U1z101F1e1k

## Known issues

- [Duplicate nodes](https://github.com/osmlab/dcbuildings/issues/11)
- [Import ids?](https://github.com/osmlab/dcbuildings/issues/10)
