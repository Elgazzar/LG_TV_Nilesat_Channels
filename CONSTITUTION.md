# Project Constitution

## 1. File Synchronization
Any changes made to the LG TV `.TLL` configuration file must automatically be reflected in:
- `README.md`
- `2026_channels_list.md`

This ensures that the project's documentation is always perfectly synchronized with the raw data.

## 2. Channel Grouping
The `README.md` file must contain distinct channel groupings displayed in collapsible sections. The standard structural order uses a two-pass layout system:

**Phase 1: High Quality & Unsplit Categories**
1. Religion & Quran (Unsplit)
2. Premium & General (Unsplit)
3. English Movies (High Quality)
4. Arabic Movies & Cinema (High Quality)
5. Series & Drama (High Quality)
6. Music (Unsplit)
7. News (High Quality)
8. Sports (High Quality)
9. Kids & Family (High Quality)
10. Cooking (Unsplit)

**Phase 2: Low Quality Categories**
11. English Movies (Low Quality)
12. Arabic Movies & Cinema (Low Quality)
13. Series & Drama (Low Quality)
14. News (Low Quality)
15. Sports (Low Quality)
16. Kids & Family (Low Quality)

**Phase 3: Uncategorized**
17. Regional & Uncategorized

## 3. High Quality / Low Quality Segmentation
For the **Movies**, **News**, **Series**, **Sports**, and **Kids & Family** groupings, the lists MUST be segregated into two separate passes across the entire channel list:
- **Phase 1 (High Quality Tier)**: Contains only High Quality channels grouped sequentially.
- **Phase 2 (Low Quality Tier)**: Follows Phase 1, containing the remaining Lower Quality channels grouped in the same sequence.

### Quality Criteria
A channel is considered **High Quality** if it meets any of the following criteria:
- **Explicit High Quality**: `Al Qahera News`, `beIN SPORTS`, `beIN SPORTS NEWS`, `ON SPORT HD`, `ON SPORT MAX HD`, `ON SPORT PLUS HD`, `AD Sport 1 HD`, `AD Sport 2 HD`.
- The channel name contains `HD`
- The channel belongs to popular networks including: `Alhayat`, `MBC`, `DMC`, `ON`, `CBC`, `Rotana`, `OSN`, `Sky News`, `Al Jazeera`, `Extra News`.

**Explicit Low Quality Exceptions**:
- `Hawa Baghdad Drama` is strictly Low Quality regardless of other keywords.
