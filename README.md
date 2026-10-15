# CRESCENT-CPAL

[![License: BSD-3-Clause](https://img.shields.io/badge/License-BSD_3--Clause-blue.svg)](LICENSE)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC_BY_4.0-lightgrey.svg)](LICENSE-CC4.0)

Data and scripts for the Cascadia Paleoseismology Working Group ([CPAL](https://cascadiaquakes.org/cpal/)) compilation within [CRESCENT](https://cascadiaquakes.org/). They feed the CPAL viewer and book.

**Viewer:** https://cpal.cascadiaquakes.org

**Documentation:** https://cascadiaquakes.github.io/cpal-book/

---

## Features

### Data Files

- The original data files are in Microsoft Excel format and are stored in the `excel/` folder.
- These files are converted to GeoJSON format for web-based visualization and are stored in the `geojson/` folder.
- Corresponding JSON files that provide field descriptions and column display controls for the web interface are stored in the `json/` folder.
- Raw data are available from Staisch, L.M., Witter, R.C., Watt, J.T., Grant, A.R., Walton, M.A., Brothers, D., Davis, E., Dura, C., Engelhart, S., Enkin, R., Garrison-Laney, C.E, Goldfinger, C., Hamilton, T., Hawkes, A., Hill, J.C., Hong, I.J., Jaffe, B.E., Kelsey, H., Lahusen, S.R, La Selle, S.M, Nelson, A.R, Nieminski, N.M, Padgett, J.S, Patton, J., Pearl, J.K, Pilarczyk, J., Sherrod, B., and Stanton, K., 2024, Compiled onshore and offshore paleoseismic data along the Cascadia Subduction zone: U.S. Geological Survey data release, [https://doi.org/10.5066/P13OJQYW](https://doi.org/10.5066/P13OJQYW).

- Coastal flooding polygons from Dura et al. (2025), [https://doi.org/10.1073/pnas.2424659122](https://doi.org/10.1073/pnas.2424659122), are in `geojson/subsidence/`. See its [README](data/geojson/subsidence/README.md) for sources and terms.

All files located in the /data directory, except `geojson/subsidence/`, are licensed under the Creative Commons Attribution 4.0 International (CC-BY-4.0) license.

### Scripts

Under the `scripts` directory, two `Python` helper tools are provided to convert the data and description files to the corresponding `GeoJSON` and `JSON` files respectively. For information on how to use these scripts, see the guides under the scripts directory.

All software scripts in this repository are licensed under the BSD 3-Clause License.

---

## License

Files in `data/` are licensed under the Creative Commons Attribution 4.0 International License (CC BY 4.0), see [LICENSE-CC4.0](LICENSE-CC4.0), except `data/geojson/subsidence/`, which follows its original authors' terms. The scripts are licensed under the BSD 3-Clause License, see [LICENSE-BSD3](LICENSE-BSD3).

---

## Contacts

**Software:**
- **Amanda M. Thomas**, University of California, Davis: [amthom@ucdavis.edu](mailto:amthom@ucdavis.edu)
- **William Marfo**, University of California, Davis: [wmarfo@ucdavis.edu](mailto:wmarfo@ucdavis.edu)
- **Loïc Bachelot**, University of Oregon: [lbachelo@uoregon.edu](mailto:lbachelo@uoregon.edu)

**Data:**
- **Tina Dura**, Virginia Tech: [tinadura@vt.edu](mailto:tinadura@vt.edu)
- **Lydia Staisch**, U.S. Geological Survey: [lstaisch@usgs.gov](mailto:lstaisch@usgs.gov)

For bugs or questions, please [open an issue](https://github.com/cascadiaquakes/CRESCENT-CPAL/issues).

---

## Acknowledgments

<table>
  <tr>
    <td align="center" valign="middle">
      <img src="https://raw.githubusercontent.com/cascadiaquakes/.github/main/assets/crescent-circle.png" alt="CRESCENT Logo" width="150" />
    </td>
    <td align="center" valign="middle">
      <img src="https://raw.githubusercontent.com/cascadiaquakes/.github/main/assets/nsf-logo.png" alt="NSF Logo" width="450" />
    </td>
  </tr>
</table>

This project is supported by the National Science Foundation through the Cascadia Region Earthquake Science Center (CRESCENT), Cooperative Agreement EAR-2225286.

---

## Disclaimers

**USGS Data Disclaimer**:  
Unless otherwise stated, all data, metadata, and related materials are considered to satisfy the quality standards relative to the purpose for which the data were collected. Although these data and associated metadata have been reviewed for accuracy and completeness and approved for release by the U.S. Geological Survey (USGS), no warranty expressed or implied is made regarding the display or utility of the data for other purposes, nor on all computer systems, nor shall the act of distribution constitute any such warranty.

**USGS Nonendorsement Disclaimer**:  
Any use of trade, firm, or product names is for descriptive purposes only and does not imply endorsement by the U.S. Government.
