# TicketWatch



A desktop app that monitors Ticketmaster Canada for ticket availability and sends email alerts when matches are found.

## Download

[![Platform](https://img.shields.io/badge/platform-Windows-blue?style=for-the-badge&logo=windows)](https://github.com/RENOLEVES/TicketMasterBot/releases/tag/Main)

> Windows x64 only

## Requirements

- Windows 10 or later
- [Google Chrome](https://www.google.com/chrome/) installed

## Installation

1. Download the installer from the link above
2. Run `TicketWatch Setup.exe`
3. Launch **TicketWatch** from the desktop shortcut

## Usage
<img width="900" height="680" alt="d1e1a658837a4e03b45965bc73067e28" src="https://github.com/user-attachments/assets/577bbaff-b163-49c6-b855-863cb01b8041" />
<img width="900" height="750" alt="1f9ce262403de02634f63596bc7eef13" src="https://github.com/user-attachments/assets/0a135ee4-fff8-49a7-afa3-f6ac7a3a2638" />

1. Paste a **Ticketmaster Canada event URL** into the URL field
2. Enter your **email address** for alerts
3. Set filters (optional):
   - **Min / Max Price** — only match tickets within this price range
   - **Ticket Type** — Any, Standard, VIP Package, or Verified Resale
   - **Sections** — add specific section names (e.g. `103`, `Floor`, `GA`); leave empty to match all sections
   - **Check Interval** — how often to check for new tickets
4. Click **Start Watching**
5. Switch to the **Results** tab to see a live chart of ticket availability over time
6. You'll receive an email alert when new matching tickets are found

## Notes

- The app runs in the background when minimized — right-click the tray icon to quit
- The first launch may take a few extra seconds while the browser driver initializes
- An active internet connection is required
