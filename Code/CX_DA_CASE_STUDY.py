import pandas as pd

excel_file = pd.ExcelFile("CX_DA_Case_Study.xlsx")

#Part A - 1. How many tickets are there per week?
tickets = excel_file.parse("Sheet1_Tickets")
tickets["Created_date"] = pd.to_datetime(tickets["Created_date"])

tickets["year_week"] = (
    tickets["Created_date"].dt.isocalendar().year.astype(str) + "-W" +
    tickets["Created_date"].dt.isocalendar().week.astype(str).str.zfill(2)
)

ticket_per_week = (
    tickets.groupby("year_week")["Ticket_id"]
    .count()
    .reset_index()
    .rename(columns={"Ticket_id": "total_tickets"})
    .sort_values("year_week")
)

#Part A - 2. What is the SLA on-time rate? Break down by week and by service.
df = excel_file.parse("Sheet2_SLA")
df["SLA"] = df["SLA"].str.replace(",", "", regex=False).astype(float)
df["Created_datetime"] = pd.to_datetime(df["Created_datetime"])
df["Resolved_datetime"] = pd.to_datetime(df["Resolved_datetime"])

from datetime import timedelta

WORK_START = 9
WORK_END = 18

def calc_business_minutes(start, end):
    # Case1: If created outside the working hours
    def adjust_start(dt):
        # Weekend -> Monday
        while dt.weekday() > 4:
            dt = (dt + timedelta(days=1)).replace(hour=WORK_START, minute=0, second=0)
        # Before 9AM -> 9AM
        if dt.hour < WORK_START:
            dt = dt.replace(hour=WORK_START, minute=0, second=0)
        # After 18PM -> 9AM the next day (except the weekend)
        if dt.hour >= WORK_END:
            dt = (dt + timedelta(days=1)).replace(hour=WORK_START, minute=0, second=0)
            while dt.weekday() > 4:
                dt = (dt + timedelta(days=1)).replace(hour=WORK_START, minute=0, second=0)
        return dt

    # Case1: If resolved outside the working hours
    def adjust_end(dt):
        # Weekend -> Monday
        while dt.weekday() > 4:
            dt = (dt + timedelta(days=1)).replace(hour=WORK_START, minute=0, second=0)
        # Before 9AM -> 9AM
        if dt.hour < WORK_START:
            dt = dt.replace(hour=WORK_START, minute=0, second=0)
        # After 6PM -> 9AM the next day (except the weekend)
        if dt.hour >= WORK_END:
            dt = (dt + timedelta(days=1)).replace(hour=WORK_START, minute=0, second=0)
            while dt.weekday() > 4:
                dt = (dt + timedelta(days=1)).replace(hour=WORK_START, minute=0, second=0)
        return dt

    start = adjust_start(start)
    end = adjust_end(end)

    if end <= start:
        return 0

    # Case2: On the same day
    if start.date() == end.date():
        return int((end - start).seconds / 60)

    total_minutes = 0
    current = start

    while current.date() <= end.date():
        if current.weekday() <= 4:  # Case 2: Exclude the weekend
            if current.date() == start.date():
                # Case3 & 4: First day -> from 9AM to 6PM
                day_end = current.replace(hour=WORK_END, minute=0, second=0)
                total_minutes += int((day_end - current).seconds / 60)

            elif current.date() == end.date():
                # Case3 & 4: Last day -> from 9AM to 6PM
                day_start = current.replace(hour=WORK_START, minute=0, second=0)
                total_minutes += int((end - day_start).seconds / 60)

            else:
                # Case3: In a day = 9 working-hour = 540 minutes
                total_minutes += 540

        current = (current + timedelta(days=1)).replace(hour=0, minute=0, second=0)

    return total_minutes

df["actual_SLA"] = df.apply(
    lambda row: calc_business_minutes(row["Created_datetime"], row["Resolved_datetime"]),
    axis=1
)

df["sla_on_time_rate"] = df["actual_SLA"] / df["SLA"]

tickets = excel_file.parse("Sheet1_Tickets")
tickets["Created_date"] = pd.to_datetime(tickets["Created_date"])

df = df.merge(tickets[["Ticket_id", "Level"]], on="Ticket_id", how="left")

df["year_week"] = (
    df["Created_datetime"].dt.isocalendar().year.astype(str) + "-W" +
    df["Created_datetime"].dt.isocalendar().week.astype(str).str.zfill(2)
)

sla_by_service_week = (
    df.groupby(["year_week", "Level"], as_index=False)
      .agg(
          avg_sla_on_time_rate=("sla_on_time_rate", "mean"),
          ticket_count=("Ticket_id", "count")
      )
      .sort_values(["year_week", "Level"])
)

with pd.ExcelWriter("CX_DA_CASE_STUDY_2.xlsx", engine="openpyxl") as writer:
    # Sheet 1: Tickets per week
    ticket_per_week.to_excel(writer, sheet_name="Tickets per week", index=False)

    # Sheet 2: Detailed ticket-level data
    df.to_excel(writer, sheet_name="Ticket_Details", index=False)

    # Sheet 3: Weekly SLA summary
    sla_by_service_week.to_excel(writer, sheet_name="SLA_By_Week_Service", index=False)
