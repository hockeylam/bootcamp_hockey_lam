# Project Title
**Stage:** Problem Framing & Scoping (Stage 01)
## Problem Statement
A casual human trader is susceptable to clouded judgement due to emotions. This may cause them to execute and lose out on trades, which is completely avoidable had they stuck to their strategies. This is why it can be beneficial to create a trading bot equipped with a profitable strategy. 
The goal of this project is to automate trading strategies to be executed percisely, using python and IBridgePy, thus eliminating human error from trade execution. This then allows us to pick and choose strategies to adapt to different market conditions.
In order to achieve success in this project, trading strategies will be backtested and compared to the growth of the SPY. Should a strategy score higher returns than the SPY, project sucess is achieved.
## Stakeholder & User
This project is academic and self driven. Depending on the results of algorithmic paper trading, I may personally deploy with my own IB account.
Stakeholder artifacts of this project will be graphic representations of different strategy's P/L over time.
## Useful Answer & Decision
Useful extractions from the project are the strategies which are shown (not proven) to be profitable using historic data. Therefore, these strategies are predictive. 
As deliverables, both metrics (profits) and artifacts (performance charts).
## Assumptions & Constraints
Since the project is set to be complete at the end of the 2 week bootcamp, the project is confined to the usage of historical data, rather than live testing, as there is would be a strong lack of sample with only 2 weeks to test.
The project is also limited by information avaliable of stock prices, that can be accessible to the IB apis.
## Known Unknowns / Risks
One of the risks is that due to the limitations of historical data, there is no guarentee that the strategies tested will produce profits. The project can only showcase strategies that are historically profitable, and cannot guarentee future profits.
## Lifecycle Mapping
Goal → Stage → Deliverable
- Set up IBridgePy → installing packages → set up IBridgePy
- Make Strategies → conception/coding → Strategy Crafting
- Filter Strategies → awaiting previous stage → Measure/Compare Profits
## Repo Plan
/data/, /src/, /notebooks/, /docs/ ; cadence for updates