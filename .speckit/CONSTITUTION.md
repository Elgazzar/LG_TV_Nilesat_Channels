# Project Constitution

## 1. File Synchronization
Any changes made to the LG TV `.TLL` configuration file must automatically be reflected in:
- `README.md`
- `2026_channels_list.md`

This ensures that the project's documentation is always perfectly synchronized with the raw data.

## 2. Channel Grouping
The `README.md` file must contain distinct channel groupings displayed in collapsible sections, specifically organizing channels into logical categories such as Movies, Series, News, and Premium.

## 3. High Quality / Low Quality Segmentation
For the **Movies**, **News**, and **Series** groupings, the lists MUST be internally sorted by Quality:
- **High Quality Tier**: The top of the list must contain High Quality channels.
- **Low Quality Tier**: The bottom of the list contains the remaining Lower Quality channels.

### Quality Criteria
A channel is considered **High Quality** if it meets any of the following criteria:
- The channel name contains `HD`
- The channel belongs to popular networks including: `Alhayat`, `MBC`, `DMC`, `ON`, `CBC`, `Rotana`, `OSN`, `Sky News`, `Al Jazeera`, `Extra News`.
