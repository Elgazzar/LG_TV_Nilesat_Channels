# Known LG TV Channel List Issues

When creating or modifying LG TV channel lists (`.TLL` files), certain configuration properties must be handled carefully to avoid bugs in the TV's firmware when parsing the channels.

## 1. Channels Misclassified as Radio
LG TVs group channels based on their `serviceType` (e.g., `1` for SD TV, `2` for Digital Radio, `25` for HD TV). However, a known bug causes the TV to incorrectly classify a valid HD TV channel (`serviceType: 25`) as a Radio channel if the `userSelCHNo` property is set to `False`. 

**Fix/Validation**: Ensure that any active HD channel has `userSelCHNo: True`. If it must remain `False` for some reason, the `serviceType` must be forced to `1` to avoid the Radio misclassification.

## 2. Channels Automatically Skipping
LG TVs utilize the `minorNumber` property to group sub-channels or hidden channels. If a channel has a non-zero `minorNumber` (e.g., `279`, `280`), the TV will often treat it as a hidden sub-channel. This results in the channel being silently skipped when the user surfs using the CH +/- buttons.

**Fix/Validation**: Ensure that `minorNumber` is set to `0` for all active, primary channels.
