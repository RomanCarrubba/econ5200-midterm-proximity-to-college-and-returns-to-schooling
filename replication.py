import ssl
import time
from io import BytesIO
from urllib.request import urlopen

import certifi
import pandas as pd
import statsmodels.api as sm
from linearmodels.iv import IV2SLS

started_at = time.perf_counter()

DATA_URL = "https://raw.githubusercontent.com/scunning1975/mixtape/master/card.dta"
CONTROLS = ["exper", "black", "south", "smsa"]
INSTRUMENT = "nearc4"

print("Downloading Card (1995) data...")
ssl_context = ssl.create_default_context(cafile=certifi.where())
with urlopen(DATA_URL, context=ssl_context) as response:
    card = pd.read_stata(BytesIO(response.read()))

columns = ["lwage", "educ", INSTRUMENT] + CONTROLS
data = card[columns].dropna().astype("float64")

iv_fit = IV2SLS(
    data["lwage"],
    sm.add_constant(data[CONTROLS]),
    data["educ"],
    data[INSTRUMENT],
).fit(cov_type="robust")

ols_fit = sm.OLS(
    data["lwage"],
    sm.add_constant(data[["educ"] + CONTROLS]),
).fit(cov_type="HC1")

first_stage = sm.OLS(
    data["educ"],
    sm.add_constant(data[[INSTRUMENT] + CONTROLS]),
).fit()
first_stage_robust = sm.OLS(
    data["educ"],
    sm.add_constant(data[[INSTRUMENT] + CONTROLS]),
).fit(cov_type="HC1")

print()
print("Table 1. Returns to schooling: OLS and instrumental variables")
print("Outcome: log hourly wage (lwage); treatment: years of schooling (educ)")
print(f"Controls: {', '.join(CONTROLS)}")
print(f"Analysis sample: {len(data):,} complete observations")
print("Standard errors: HC1 for OLS; heteroskedasticity-robust for 2SLS")
print()
print(f"{'Estimator':<12}{'Instrument':<14}{'Coefficient':>14}{'Robust SE':>14}{'N':>9}")
print("-" * 63)
print(
    f"{'OLS':<12}{'N/A':<14}{ols_fit.params['educ']:>14.4f}"
    f"{ols_fit.bse['educ']:>14.4f}{int(ols_fit.nobs):>9,}"
)
print(
    f"{'2SLS':<12}{INSTRUMENT:<14}{iv_fit.params['educ']:>14.4f}"
    f"{iv_fit.std_errors['educ']:>14.4f}{int(iv_fit.nobs):>9,}"
)
print()
print("First stage: schooling regressed on the instrument and controls")
print(f"Instrument coefficient ({INSTRUMENT}): {first_stage.params[INSTRUMENT]:+.4f} years")
print(f"Classical first-stage F: {first_stage.tvalues[INSTRUMENT] ** 2:.2f}")
print(f"HC1-robust first-stage F: {first_stage_robust.tvalues[INSTRUMENT] ** 2:.2f}")
print("The schooling coefficients are log-wage points per additional year of schooling.")
print(f"Data source: {DATA_URL}")
print(f"Runtime after imports (download and analysis): {time.perf_counter() - started_at:.2f} seconds")
