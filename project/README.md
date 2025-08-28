# Trade Strategy tester + SPY price predictor
## Problem Statement
A casual human trader is susceptable to clouded judgement due to emotions. This may cause them to execute and lose out on trades, which is completely avoidable had they stuck to their strategies. This is why it can be beneficial to create a trading bot equipped with a profitable strategy. 

The goal of this project is to test trading strategies and be able to slowly perfect them. This thus eliminating human error from trade execution. This then allows us to pick and choose strategies to adapt to different market conditions.
In order to achieve success in this project, trading strategies will be backtested and compared to the growth of the SPY. Should a strategy score higher returns than the SPY, project sucess is achieved.

## Stakeholder & User
This project is academic and self driven. Depending on the results of algorithmic paper trading, I may personally deploy with my own IB account. I am both the stakeholder and the user.

Stakeholder artifacts of this project will be graphic representations of different strategy's P/L over time.
A final google slide will be included in the reports folder that explains my findings.

## Useful Answer & Decision
Useful extractions from the project are the strategies which are shown (not proven) to be profitable using historic data. Therefore, these strategies are predictive. 
As deliverables, both metrics (profits) and artifacts (performance charts).

## Assumptions & Constraints
Assumptions:
Accurate and reliable historical pricing

Constaints:
Since the project is set to be complete at the end of the 2 week bootcamp, the project is confined to the usage of historical data, rather than live testing, as there is would be a strong lack of sample with only 2 weeks to test. 


## Known Unknowns / Risks
One of the risks is that due to the limitations of historical data, there is no guarentee that the strategies tested will produce profits. The project can only showcase strategies that are historically profitable, and cannot guarentee future profits.

## Lifecycle Mapping
Goal → Stage → Deliverable
- import data → data loading/prepocessing → code in load_data.py
- 30 day SMA and volatiliy → feature engineering → code in main.py
- flag outliers → outlier testing → code in main.py
- Make Strategies → modeling → code in strategies.py
- Test strategies → modeling → backtesting.py, artifact.py
- Filter Strategies → modeling / exploratory data analysis→ artifact.py comparison
- Prediction algorithm → linear regression → linear_model.pkl, regression.py
- Flask API → productization → app.py and running app
- freeze requirements → tooling setup → requirements.txt
- Documentations → shareholder communication → reports folder/readme

## Repo Plan
/data/, /src/, /notebooks/, /docs/ ; cadence for updates