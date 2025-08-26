## Assumptions

Bootstrapped data is close to the real world data. We are also assuming that the new data which we use the model on is similiar to the dataset used to train. If not, the model may not function well. 

I also didnt deal with outliers, meaning that this model functions with outlier information, which may lead to the occasional highly inaccurate result.

The result should hold as long as the data inflow is similiar to the existing data.

## Sensitivity

the model is around medium sensitivity, meaning it is somewhat sensitive to data changes.

## Results

{'mean': 1.2714062440720517,
 'lo': 1.0550822262814064,
 'hi': 1.5309979723635576}

 meaning 95% of our trails, the MAE falls into the range of 1.05-1.53.