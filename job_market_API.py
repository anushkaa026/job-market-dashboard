"""
job_market_API.py
-----------------
Data layer for the Job Market Dashboard.
Handles loading, cleaning, and filtering BLS Employment & Wages data (Q2 2025).

All data access in the dashboard goes through this file.
The UI never touches the dataframe directly.
"""

import pandas as pd

DATA_FILE_PATH = "10.csv"

AREA_FIPS_COL     = "area_fips"
AVG_WAGE_COL      = "avg_wkly_wage"
EMPLOYMENT_COL    = "month1_emplvl"
ESTABLISHMENTS_COL = "qtrly_estabs"
WAGE_CHANGE_COL   = "oty_avg_wkly_wage_pct_chg"
EMP_CHANGE_COL    = "oty_month1_emplvl_pct_chg"

STATE_AGGLVL  = 50
COUNTY_AGGLVL = 70

METRICS = {
    "Avg Weekly Wage ($)"        : AVG_WAGE_COL,
    "Employment Level"           : EMPLOYMENT_COL,
    "Number of Establishments"   : ESTABLISHMENTS_COL,
    "Wage Change YoY (%)"        : WAGE_CHANGE_COL,
    "Employment Change YoY (%)"  : EMP_CHANGE_COL,
}

FIPS_TO_STATE = {
    "01": "Alabama",              "02": "Alaska",
    "04": "Arizona",              "05": "Arkansas",
    "06": "California",           "08": "Colorado",
    "09": "Connecticut",          "10": "Delaware",
    "11": "District of Columbia", "12": "Florida",
    "13": "Georgia",              "15": "Hawaii",
    "16": "Idaho",                "17": "Illinois",
    "18": "Indiana",              "19": "Iowa",
    "20": "Kansas",               "21": "Kentucky",
    "22": "Louisiana",            "23": "Maine",
    "24": "Maryland",             "25": "Massachusetts",
    "26": "Michigan",             "27": "Minnesota",
    "28": "Mississippi",          "29": "Missouri",
    "30": "Montana",              "31": "Nebraska",
    "32": "Nevada",               "33": "New Hampshire",
    "34": "New Jersey",           "35": "New Mexico",
    "36": "New York",             "37": "North Carolina",
    "38": "North Dakota",         "39": "Ohio",
    "40": "Oklahoma",             "41": "Oregon",
    "42": "Pennsylvania",         "44": "Rhode Island",
    "45": "South Carolina",       "46": "South Dakota",
    "47": "Tennessee",            "48": "Texas",
    "49": "Utah",                 "50": "Vermont",
    "51": "Virginia",             "53": "Washington",
    "54": "West Virginia",        "55": "Wisconsin",
    "56": "Wyoming",              "72": "Puerto Rico",
    "78": "Virgin Islands",
}

STATE_TO_REGION = {
    "Maine": "Northeast", "New Hampshire": "Northeast", "Vermont": "Northeast",
    "Massachusetts": "Northeast", "Rhode Island": "Northeast", "Connecticut": "Northeast",
    "New York": "Northeast", "New Jersey": "Northeast", "Pennsylvania": "Northeast",

    "Wisconsin": "Midwest", "Michigan": "Midwest", "Illinois": "Midwest",
    "Indiana": "Midwest", "Ohio": "Midwest", "North Dakota": "Midwest",
    "South Dakota": "Midwest", "Nebraska": "Midwest", "Kansas": "Midwest",
    "Minnesota": "Midwest", "Iowa": "Midwest", "Missouri": "Midwest",

    "Delaware": "South", "Maryland": "South", "District of Columbia": "South",
    "Virginia": "South", "West Virginia": "South", "North Carolina": "South",
    "South Carolina": "South", "Georgia": "South", "Florida": "South",
    "Kentucky": "South", "Tennessee": "South", "Mississippi": "South",
    "Alabama": "South", "Oklahoma": "South", "Texas": "South",
    "Arkansas": "South", "Louisiana": "South",

    "Idaho": "West", "Montana": "West", "Wyoming": "West", "Nevada": "West",
    "Utah": "West", "Colorado": "West", "Arizona": "West", "New Mexico": "West",
    "Alaska": "West", "Washington": "West", "Oregon": "West", "California": "West",
    "Hawaii": "West",
}

class JobMarketAPI:
    def __init__(self, filename=DATA_FILE_PATH):
        self.df = pd.read_csv(filename, dtype={AREA_FIPS_COL: str})
        self._add_state_column()

    def _add_state_column(self):
        self.df["state_fips"] = self.df[AREA_FIPS_COL].str[:2]
        self.df["state"] = self.df["state_fips"].map(FIPS_TO_STATE)

    def get_states(self):
        states = sorted(self.df["state"].dropna().unique().tolist())
        return ["All States"] + states

    def get_state_summary(self, metric_col=AVG_WAGE_COL):
        df = self.df[
            (self.df["agglvl_code"] == STATE_AGGLVL) &
            (self.df["own_code"] == 0)
        ].copy()

        all_metric_cols = list(METRICS.values())
        df = df.dropna(subset=[metric_col, "state"])
        df = df[df[metric_col] > 0]
        df["region"] = df["state"].map(STATE_TO_REGION)

        cols = ["state", "state_fips", AREA_FIPS_COL, "region"] + all_metric_cols
        return df[cols].reset_index(drop=True)


    def get_county_data(self, state="All States", metric_col=AVG_WAGE_COL, top_n=15):
        df = self.df[
            (self.df["agglvl_code"] == COUNTY_AGGLVL) &
            (self.df["own_code"] == 0)
        ].copy()

        if state != "All States":
            df = df[df["state"] == state]

        df = df.dropna(subset=[metric_col])
        df = df[df[metric_col] > 0]

        df["county_label"] = df[AREA_FIPS_COL]

        df = df.sort_values(metric_col, ascending=False).head(top_n)

        return df[["county_label", "state", AREA_FIPS_COL, metric_col]].reset_index(drop=True)

    def get_table(self, state="All States"):
        df = self.df[
            (self.df["agglvl_code"] == STATE_AGGLVL) &
            (self.df["own_code"] == 0)
        ].copy()

        if state != "All States":
            df = df[df["state"] == state]

        df = df.dropna(subset=["state"])

        rename = {
            "state"          : "State",
            AVG_WAGE_COL     : "Avg Weekly Wage ($)",
            EMPLOYMENT_COL   : "Employment",
            ESTABLISHMENTS_COL: "Establishments",
            WAGE_CHANGE_COL  : "Wage Change YoY (%)",
            EMP_CHANGE_COL   : "Employment Change YoY (%)",
        }

        return df[list(rename.keys())].rename(columns=rename).reset_index(drop=True)


def main():
    api = JobMarketAPI(DATA_FILE_PATH)
    print("States sample:", api.get_states()[:5])
    print("\nState summary (3 rows):")
    print(api.get_state_summary().head(3))
    print("\nTop counties in Texas:")
    print(api.get_county_data(state="Texas", top_n=5))
    print("\nData table (3 rows):")
    print(api.get_table().head(3))


if __name__ == "__main__":
    main()