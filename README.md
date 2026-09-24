# Fund Liquidity Mismatch Stress Engine

## Asset-Side Liquidity, Redemption Pressure, Fire-Sale Costs and Escalation Outcomes

This project simulates a **fund liquidity mismatch stress engine** for an open-ended multi-asset fund.

The engine compares:

- **asset-side liquidity** — how quickly the fund can turn holdings into cash
- **liability-side liquidity** — how quickly investors can redeem
- **redemption shocks** — what happens when investors request cash under stress
- **fire-sale costs** — value lost when assets must be sold quickly
- **remaining portfolio liquidity** — how liquid the fund is after meeting redemptions
- **model-suggested escalation outcomes** — whether the fund can meet redemptions cleanly or needs liquidity committee review

The project extends a fund operations portfolio from:

> Is the NAV accurate?

to:

> Can the fund survive investor redemptions under stress?

---

## Project Motivation

Open-ended funds often offer daily or short-notice redemption terms, but their assets are not always equally liquid.

A fund may hold:

- cash
- Treasury bills
- money market funds
- large-cap equities
- mid-cap equities
- investment-grade bonds
- high-yield bonds
- small-cap stocks
- private credit
- property
- private equity
- side-pocket or hard-to-sell assets

Some assets can be sold quickly with little price impact. Others may take weeks or months to liquidate without a large discount.

This creates a **liquidity mismatch**:

> Investors can ask for their money back quickly, but the fund may not be able to sell assets quickly without damaging the portfolio.

This project models that mismatch under several redemption shocks.

---

## What the Engine Does

The engine simulates a liquidity stress workflow:

    Fund Holdings + Investor Base
              ↓
    Liquidity Classification
              ↓
    Market Depth and Fire-Sale Assumptions
              ↓
    Redemption Shock Scenarios
              ↓
    Liquidation Waterfall
              ↓
    Cash Raised and Fire-Sale Cost
              ↓
    Liquidity Coverage Ratio
              ↓
    Remaining Portfolio Liquidity
              ↓
    Model-Suggested Escalation Outcome
              ↓
    Excel Report + Streamlit Dashboard

The goal is not to predict when redemptions happen.

The goal is to answer:

> If redemptions happen, can the fund meet them, what does it cost, and what liquidity action should be reviewed?

---

## Fund Universe

The simulated fund is:

| Item | Value |
|---|---|
| Fund name | Global Income Opportunities Fund |
| Fund type | Open-Ended Multi-Asset Fund |
| Base currency | GBP |
| Dealing frequency | Daily |
| Redemption notice period | 1 day |
| Fund NAV | £1,000,000,000 |
| Number of holdings | 26 |

The fund is intentionally built with a mix of liquid and illiquid assets.

---

## Initial Liquidity Profile

| Liquidity Bucket | Market Value | Portfolio Weight |
|---|---:|---:|
| T+0 | £100,000,000 | 10.0% |
| T+1 | £350,000,000 | 35.0% |
| T+3 | £150,000,000 | 15.0% |
| T+7 | £145,000,000 | 14.5% |
| T+30 | £150,000,000 | 15.0% |
| T+90+ | £105,000,000 | 10.5% |

The portfolio has enough short-term liquidity for normal conditions, but also contains a meaningful allocation to slower-to-sell assets.

---

## Asset-Side Liquidity

Each holding is assigned to a liquidity bucket:

| Bucket | Meaning |
|---|---|
| T+0 | Cash or immediately available liquidity |
| T+1 | Highly liquid cash equivalents, large-cap equities and liquid ETFs |
| T+3 | Moderately liquid listed assets |
| T+7 | Investment-grade credit and less liquid fixed income |
| T+30 | High-yield credit, small-cap exposure and stressed liquidity assets |
| T+90+ | Property, private markets and hard-to-sell assets |

Each holding includes:

- holding ID
- ticker
- asset name
- asset class
- sector
- currency
- market value
- liquidity bucket
- bucket days
- average daily volume
- percentage of ADV held
- bid-ask spread
- issue size or free float
- listed / daily traded flag
- portfolio weight

---

## Liability-Side Liquidity

The engine also models the investor base.

Investor types include:

| Investor Type | AUM Share | Notice Period |
|---|---:|---:|
| Retail Direct | 30% | 1 day |
| Platform Aggregated Retail | 35% | 1 day |
| Wealth Managers | 15% | 2 days |
| Institutional Seed Investor | 12% | 5 days |
| Pension / Consultant Channel | 8% | 5 days |

This matters because not all investors behave the same way.

For example:

- platform flows can move together quickly
- retail flows can be numerous and sentiment-driven
- institutional investors may redeem less often but in larger blocks
- pension or consultant flows may be more stable but governance-driven

The engine allocates redemption shocks across investor types using stress multipliers, redemption volatility, notice period and stickiness assumptions.

---

## Redemption Scenarios

The engine tests five redemption shock scenarios:

| Scenario | Redemption % of NAV | Redemption Amount | Horizon | Materiality |
|---|---:|---:|---:|---|
| Mild Outflow | 5% | £50,000,000 | 3 days | Mild |
| Elevated Outflow | 10% | £100,000,000 | 7 days | Elevated |
| Stress Redemption | 20% | £200,000,000 | 7 days | Stress |
| Crisis Redemption | 30% | £300,000,000 | 7 days | Crisis |
| Systemic Liquidity Run | 45% | £450,000,000 | 7 days | Systemic |

---

## Liquidity Assumptions

The engine defines market-depth and transaction-cost assumptions by liquidity bucket.

Each bucket has:

- normal transaction cost
- stressed transaction cost
- severe transaction cost
- maximum percentage of ADV sellable per day
- liquidity quality score
- qualitative description

This matters because selling fast is not free.

The same holding may be cheap to sell in normal conditions but expensive to sell in stressed conditions.

---

## Validation Layer

Before running the stress test, the engine validates the liquidity data.

Validation checks include:

| Control | Purpose |
|---|---|
| Valid liquidity buckets | Ensures every holding has a recognised bucket |
| Positive market value | Flags invalid or missing market values |
| ADV data for traded assets | Checks market-depth inputs |
| Investor base sums to 100% | Checks liability-side completeness |
| Positive redemption scenarios | Ensures scenarios are usable |
| Tail stress scenario included | Confirms systemic scenario is present |

Validation result:

| Metric | Result |
|---|---:|
| Holdings validated | 26 |
| Invalid holdings | 0 |
| Watchlist holdings | 8 |
| Redemption scenarios | 5 |

Watchlist holdings include high-yield credit, private credit, property, small-cap exposure and T+90+ assets.

---

## Liquidation Waterfall

The liquidation waterfall simulates how the fund raises cash under each redemption shock.

The engine sells assets in liquidity order:

    T+0 → T+1 → T+3 → T+7 → T+30 → T+90+

For each sale, the engine calculates:

- gross sale amount
- transaction cost in basis points
- fire-sale cost
- cash raised
- remaining holding value
- cumulative cash raised
- remaining redemption need

This produces a scenario-by-scenario sell-down table.

---

## Liquidity Coverage Ratio

The project calculates a fund-style liquidity coverage ratio:

    Liquidity Coverage Ratio = Net Liquidation Capacity / Redemption Amount

A ratio above 1.0 means the fund can theoretically raise enough cash within the tested horizon.

A ratio close to 1.0 means the fund has limited buffer.

A ratio below 1.0 would indicate a cash shortfall.

---

## Main Results

The engine produced the following stress results:

| Metric | Result |
|---|---:|
| Scenarios tested | 5 |
| Scenarios met in full | 2 |
| Scenarios requiring escalation | 3 |
| High / critical liquidity scenarios | 2 |
| Minimum LCR | 1.23x |
| Worst LCR scenario | Systemic Liquidity Run |
| Maximum fire-sale cost | £6,513,019.36 |
| Worst fire-sale scenario | Systemic Liquidity Run |
| Weakest remaining liquidity ratio | 53.08% |
| Systemic run outcome | PARTIAL_GATE_ESCALATION_REVIEW |

---

## Scenario Outcomes

| Scenario | LCR | Fire-Sale Cost | Remaining Liquidity Ratio | Model-Suggested Outcome |
|---|---:|---:|---:|---|
| Mild Outflow | 11.98x | £0 | 73% | MEET_IN_FULL |
| Elevated Outflow | 6.16x | £0 | 72% | MEET_IN_FULL |
| Stress Redemption | 3.08x | £389,393.64 | 68% | SWING_PRICING_REVIEW |
| Crisis Redemption | 1.84x | £2,040,030.31 | 63% | SWING_PRICING_TRIGGERED |
| Systemic Liquidity Run | 1.23x | £6,513,019.36 | 53% | PARTIAL_GATE_ESCALATION_REVIEW |

---

## Model-Suggested Escalation Framework

The engine does not make a legal or governance decision.

Instead, it produces a **model-suggested escalation outcome**.

Possible outcomes:

| Outcome | Meaning |
|---|---|
| MEET_IN_FULL | Redemption can be met without material liquidity deterioration |
| SWING_PRICING_REVIEW | Redemption can be met but anti-dilution pricing should be reviewed |
| SWING_PRICING_TRIGGERED | Fire-sale cost or redemption size makes swing pricing / dilution levy review necessary |
| PARTIAL_GATE_ESCALATION_REVIEW | Redemption can be met but remaining liquidity is materially weakened |
| PARTIAL_GATE_ESCALATION | Redemption cannot be fully met without staged redemption or gating review |
| SUSPENSION_ESCALATION | Severe unresolved shortfall may require dealing suspension governance review |

The project uses careful language: the model suggests escalation, but actual gating or suspension would require governance, fund documents, regulatory obligations and board / depositary procedures.

---

## Fire-Sale Cost Analysis

The engine estimates value lost when assets must be sold quickly.

Fire-sale cost increases as:

- redemption size increases
- asset liquidity worsens
- bid-ask spreads widen
- position size is large relative to ADV
- severe market conditions reduce sellable capacity

Main fire-sale result:

| Scenario | Fire-Sale Cost |
|---|---:|
| Mild Outflow | £0 |
| Elevated Outflow | £0 |
| Stress Redemption | £389,393.64 |
| Crisis Redemption | £2,040,030.31 |
| Systemic Liquidity Run | £6,513,019.36 |

---

## Remaining Portfolio Liquidity

The project does not only ask:

> Can the fund pay redeeming investors today?

It also asks:

> What liquidity profile is left for the remaining investors?

This is important because a fund may meet the first redemption wave by selling liquid assets first, leaving the remaining portfolio more concentrated in illiquid assets.

The systemic run result shows this clearly:

| Metric | Systemic Liquidity Run |
|---|---:|
| Redemption amount | £450,000,000 |
| Liquidity coverage ratio | 1.23x |
| Fire-sale cost | £6,513,019.36 |
| Remaining liquidity ratio | 53.08% |
| Remaining illiquid ratio | 46.92% |
| Model-suggested outcome | PARTIAL_GATE_ESCALATION_REVIEW |

The fund meets the redemption, but the residual fund becomes materially less liquid.

---

## Streamlit Dashboard

The project includes an interactive Streamlit dashboard:

    app.py

Dashboard pages:

1. **Executive Overview**  
   Headline liquidity coverage, fire-sale cost, escalation outcome and residual liquidity.

2. **Scenario Comparison**  
   Side-by-side comparison of redemption shocks, cash raised, LCR and fire-sale cost.

3. **Liquidation Waterfall**  
   Holding-level sell-down simulation for each scenario.

4. **Holdings Liquidity Map**  
   Portfolio composition, market-depth concentration and watchlist holdings.

5. **Fire-Sale Cost Analysis**  
   Fire-sale cost by scenario and liquidity bucket.

6. **Liability-Side Flows**  
   Investor-type redemption allocation under each scenario.

7. **Controls & Escalation**  
   Stress-test control status and model-suggested escalation outcomes.

8. **Data Explorer**  
   Inspect and download any exported workbook table.

---

## Excel Reporting Pack

The notebook exports:

    outputs/liquidity_stress_report.xlsx

The workbook contains 27 sheets, including:

| Sheet | Description |
|---|---|
| Executive_KPIs | Long-form executive KPI table |
| Executive_KPIs_Wide | One-row KPI table for dashboard use |
| Stress_Test_Controls | Control checklist for liquidity stress testing |
| Risk_Diagnostics | Scenario-level liquidity diagnostics |
| Risk_Band_Summary | Summary by liquidity risk band |
| Escalation_Summary | Summary by escalation outcome |
| Fund_Master | Fund metadata |
| Holdings | Original holdings data |
| Holdings_Enriched | Holdings with assumptions, validation flags and capacity estimates |
| Investor_Base | Investor type and redemption behaviour assumptions |
| Redemption_Scenarios | Stress scenario definitions |
| Liquidity_Assumptions | Liquidity bucket assumptions |
| Validation_Controls | Data-quality control checks |
| Liquidity_Bucket_Summary | Portfolio value by liquidity bucket |
| Asset_Class_Summary | Portfolio value by asset class |
| Market_Depth_Summary | ADV and sale capacity by bucket |
| Liquidity_Horizon_Capacity | Liquidity capacity by horizon |
| Liquidation_Waterfall | Holding-level sell-down simulation |
| Scenario_Liquidity_Summary | Scenario-level cash raised, shortfall and fire-sale cost |
| Scenario_Decision_Summary | Scenario-level final outcome |
| LCR_Scenario_Horizon | LCR by scenario and horizon |
| Fire_Sale_By_Bucket | Fire-sale cost by liquidity bucket |
| Remaining_Liquidity | Remaining portfolio liquidity after redemption |
| Investor_Redemption | Liability-side investor redemption allocation |
| Liability_Side_Summary | Investor flow summary |
| Chart_Inventory | List of exported visual outputs |

---

## Visual Outputs

The notebook exports 9 charts:

    outputs/lcr_by_scenario.png
    outputs/redemption_vs_cash_raised.png
    outputs/fire_sale_cost_by_scenario.png
    outputs/remaining_liquidity_profile.png
    outputs/fire_sale_cost_by_bucket.png
    outputs/investor_redemption_allocation.png
    outputs/liquidity_bucket_composition.png
    outputs/stress_test_control_status.png
    outputs/escalation_outcomes.png

---

## Project Structure

    fund-liquidity-stress-engine/
    │
    ├── Fund_Liquidity_Stress_Engine.ipynb
    ├── app.py
    ├── README.md
    ├── requirements.txt
    ├── .gitignore
    │
    ├── .streamlit/
    │   └── config.toml
    │
    └── outputs/
        ├── liquidity_stress_report.xlsx
        ├── liquidity_stress_executive_summary.txt
        ├── lcr_by_scenario.png
        ├── redemption_vs_cash_raised.png
        ├── fire_sale_cost_by_scenario.png
        ├── remaining_liquidity_profile.png
        ├── fire_sale_cost_by_bucket.png
        ├── investor_redemption_allocation.png
        ├── liquidity_bucket_composition.png
        ├── stress_test_control_status.png
        └── escalation_outcomes.png

---

## How to Run the Project

Clone the repository:

    git clone https://github.com/ludmila-abd/fund-liquidity-stress-engine.git
    cd fund-liquidity-stress-engine

Create and activate a virtual environment:

    python3 -m venv .venv
    source .venv/bin/activate

Install dependencies:

    pip install -r requirements.txt

Open the notebook:

    jupyter notebook Fund_Liquidity_Stress_Engine.ipynb

Run all cells:

    Kernel → Restart Kernel and Run All Cells

---

## How to Run the Streamlit App

From the project folder:

    streamlit run app.py

The dashboard will open in your browser.

If it does not open automatically, Streamlit will show a local URL such as:

    http://localhost:8501

---

## Requirements

    pandas
    numpy
    matplotlib
    plotly
    streamlit
    openpyxl
    jupyter
    ipykernel
    nbformat

---

## Skills Demonstrated

- Python data analysis
- pandas workflow design
- liquidity risk modelling
- fund redemption stress testing
- liquidation waterfall simulation
- market-depth constraint modelling
- fire-sale cost estimation
- liquidity coverage ratio calculation
- residual portfolio liquidity analysis
- investor redemption allocation
- stress-test control design
- model-suggested escalation framework
- Excel reporting automation
- Streamlit dashboard development
- Plotly visualisation
- fund risk management workflow design
- asset management operations analytics

---

## Why This Project Matters

Many finance projects focus on predicting asset prices.

This project focuses on something different:

> whether a fund can actually meet investor redemptions under stress.

That question matters because liquidity risk can affect:

- investor fairness
- fund dealing
- NAV dilution
- portfolio construction
- liquidity governance
- redemption management
- regulatory oversight
- remaining investors

The engine shows that a fund can sometimes meet a redemption today while still leaving the remaining portfolio weaker tomorrow.

That is the key liquidity mismatch insight.

---

## Portfolio Context

This project complements a broader financial operations portfolio:

- Corporate Actions Processing Engine
- Settlement Fail Risk Engine
- Fund NAV Reconciliation Engine
- Financial Operations Control Tower
- Fund Liquidity Mismatch Stress Engine

The progression is:

    Is the event processed correctly?
    Can the trade settle?
    Is the NAV correct?
    Can the fund survive redemptions?

This project moves the portfolio from operations control into fund risk and liquidity resilience.

---

## Possible Extensions

Future improvements could include:

- multi-fund stress testing
- daily liquidity trend history
- stochastic redemption simulation
- Monte Carlo investor run scenarios
- real market volume ingestion
- multi-currency liquidity modelling
- stress correlation between asset classes
- side-pocket treatment
- swing pricing calculation module
- investor dilution analysis
- liquidity ladder reports
- governance workflow tracker
- Streamlit Cloud deployment
- direct integration with the Financial Operations Control Tower

---

## Tech Stack

- Python
- pandas
- NumPy
- Matplotlib
- Plotly
- Streamlit
- OpenPyXL
- Jupyter Notebook

---

## Disclaimer

This project is an educational simulation.

It is not connected to live funds, client accounts, custodians, administrators, trading systems, accounting platforms or market data vendors.

The model-suggested escalation outcomes are illustrative and should not be interpreted as legal, regulatory or investment advice.

Actual liquidity management actions such as swing pricing, gating or dealing suspension would depend on fund documents, governance procedures, regulatory obligations and professional judgement.

---

## Author

**Ludmila Aboud**  
MSc Economics, Banking & Finance  
MSc Applied Mathematics for Finance
