# Card (1995) Returns to Schooling: Replication

A Python replication of the relationship between college proximity, schooling, and wages in David Card's (1995) study. The script compares an OLS estimate with a 2SLS estimate using proximity to a four-year college as an instrument for years of schooling.

## Data and variables

The script downloads `card.dta` from [Scunning's Mixtape repository](https://raw.githubusercontent.com/scunning1975/mixtape/master/card.dta), which hosts the Card dataset based on the National Longitudinal Survey of Young Men. It downloads the public data at run time rather than storing another copy in this repository. An internet connection is required.

| Variable | Role | Description |
|----------|------|-------------|
| `lwage` | Dependent variable | Log hourly wage |
| `educ` | Endogenous regressor | Years of schooling |
| `nearc4` | Instrument | Indicator for growing up near a four-year college |
| `exper` | Control | Years of labor market experience |
| `black` | Control | Indicator for Black |
| `south` | Control | Indicator for living in the South |
| `smsa` | Control | Indicator for living in a metropolitan area |

## Methods

The OLS model regresses log wages on years of schooling and the four controls. The 2SLS model instruments schooling with `nearc4`, using the same controls. The script reports heteroskedasticity-robust standard errors for both estimates and classical and HC1-robust first-stage F statistics.

The instrument must predict schooling (relevance) and affect wages only through schooling (the exclusion restriction).

## Requirements and setup

Use Python 3.12. The exact package versions are pinned in [`requirements.txt`](requirements.txt).

From the repository root, create and activate a virtual environment and install the dependencies:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

In Windows PowerShell, create the environment with `py -3.12 -m venv .venv` and activate it with `.\.venv\Scripts\Activate.ps1`.

## Reproduce Table 1

With the virtual environment active, run this single command from the repository root:

```bash
python replication.py
```

The script prints the OLS and 2SLS schooling coefficients and robust standard errors, analysis sample size, first-stage coefficient and F statistics, data source, and runtime. In this environment, the complete command took about **1.05 seconds**, including Python startup and downloading the data; actual runtime varies with network speed.

## Project files

```text
.
├── .gitignore
├── README.md
├── ai-appendix.md
├── replication.py
├── replication_starter_card1995.ipynb
├── requirements.txt
└── report/
    └── report.pdf
```

## References

- Card, D. (1995). “Using Geographic Variation in College Proximity to Estimate the Return to Schooling.” In *Aspects of Labour Market Behaviour: Essays in Honour of John Vanderkamp*. University of Toronto Press.
- Carneiro, P., & Heckman, J. J. (2002). “The Evidence on Credit Constraints in Post-Secondary Schooling.”
- Cameron, S. V., & Taber, C. (2004). “Estimation of Educational Borrowing Constraints Using Returns to Schooling.”
- Kling, J. R. (2001). “Interpreting Instrumental Variables Estimates of the Returns to Schooling.”
