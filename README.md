# Project Title
**Stage:** Problem Framing & Scoping (Stage 01)
## Problem Statement
A casual human trader is susceptable to clouded judgement due to emotions. This may cause them to execute and lose out on trades, which is completely avoidable had they stuck to their strategies. This is why it can be beneficial to create a trading bot equipped with a profitable strategy. 

The goal of this project is to automate trading strategies to be executed percisely, using python and IBridgePy, thus eliminating human error from trade execution. This then allows us to pick and choose strategies to adapt to different market conditions.
In order to achieve success in this project, trading strategies will be backtested and compared to the growth of the SPY. Should a strategy score higher returns than the SPY, project sucess is achieved.

## Stakeholder & User
This project is academic and self driven. Depending on the results of algorithmic paper trading, I may personally deploy with my own IB account. I am both the stakeholder and the user.

Stakeholder artifacts of this project will be graphic representations of different strategy's P/L over time.

## Useful Answer & Decision
Useful extractions from the project are the strategies which are shown (not proven) to be profitable using historic data. Therefore, these strategies are predictive. 
As deliverables, both metrics (profits) and artifacts (performance charts).

## Assumptions & Constraints
Assumptions:
Accurate and reliable historical pricing

Constaints:
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


## Homwwork Grading locations

Dear TA, due to instructions around homwork folder stucture still being unclear to me, I thought I should include some explaination of how I did my work.

Essentially all of my work for a specific homework is within its own homwwork folder, if they told me to make a directory, or change the README, There should be a copy of a the directory or a README.md within the specific homework folder. I understand this is really redundant and very much not standard SWE practice, but its the best interpretation I have on the homework instructions as they are conflicting with what professors and other GAs are saying.

Therefore, please look inside the folder of the homework for each of them, ignore the directoried of notebook or src .env. The only relevant piece in the root directory is the requirements.txt, and the .gitignore.


