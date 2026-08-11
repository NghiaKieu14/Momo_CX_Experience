# CX Performance Dashboard

A Power BI dashboard tracking customer support (ticket/SLA) performance — resolution volume, SLA compliance, and agent-level performance.

---

## Project Overview

This project uses a ticketing dataset to monitor customer experience (CX) support operations in Power BI. The focus is on SLA (Service Level Agreement) compliance, ticket resolution volume over time, and performance breakdowns by agent and support level.

---

## Data Model

The report's data model (`CX_Performance_Dashboard.pbix`) is built around the following tables:

| Table | Description |
|---|---|
| `Ticket_Details` | Core ticket-level fact table — holds SLA measures (SLA Delay Rate, Avg SLA Ratio, SLA On-Time Rate) and the weekly time grain (`year_week`) |
| `Sheet1_Tickets` | Ticket/agent source table — includes `Agent_tiep_nhan` (assigned agent), ticket counts, and active agent count |
| `Sheet2_SLA` | Supporting SLA reference/lookup table |
| `SLA_By_Week_Service` | Weekly SLA data broken out by service |
| `Tickets per week` | Weekly ticket volume aggregation table |
| `Level Display` | Support level (tier) lookup table used for level-based breakdowns |

---

## Dashboard Structure

**Page 1 — CX Performance Dashboard**

- **KPI cards:** SLA Delay Rate, Avg SLA Ratio, SLA On-Time Rate, Active Agents, Tickets
- **Slicers:** Week (`year_week`), Agent (`Agent_tiep_nhan`)
- **Total Ticket Resolved and SLA Delay Rate by Week** — combo chart (line + clustered column) showing weekly resolved ticket volume against SLA delay rate
- **Agents performance** — table breaking down total tickets and SLA delay rate by agent
- **SLA Delay Rate by Level** — clustered bar chart comparing SLA delay rate across support levels
- **Tickets by Level** — donut chart showing ticket share by support level

---

## Key Metrics Tracked

- **SLA Delay Rate** — share of tickets that breached their SLA
- **Avg SLA Ratio** — average ratio of actual resolution time to SLA target time
- **SLA On-Time Rate** — share of tickets resolved within SLA
- **Total Tickets / Total Ticket Resolved** — ticket volume, overall and per week
- **Active Agents** — count of agents handling tickets in the selected period

---

## Tools Used

- Microsoft Power BI Desktop

---

## How to Use

1. Open `CX_Performance_Dashboard.pbix` in Power BI Desktop
2. If prompted, update the data source path to point to your local copy of the underlying ticket data source
3. Refresh the data and explore the dashboard
4. Use the Week and Agent slicers to filter the view
