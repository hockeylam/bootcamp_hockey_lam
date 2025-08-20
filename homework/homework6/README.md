## Assumptions

By filling in missing numerica columns with the median, I am replacing something that is unknown with a standard represenation of the column value...
But this is only a good method when the value in there is random. 

For example, this could be a problem if a big population of people from, say, city P (for poor) who are more sensitive about their income and do not want to share, unlike city R (for rich) who are bragging about it all day on surveys. Therefore, the median would be skewed to be higher, as only higher incomers are submitting their data. Then, filling in the unknown income of residents of city P, this becomes a problem as it could be very far off from where they actually are.

I also dropped extra_data, I just assumed that it is not important as it is not specified, and also, it may be hard to draw any conclusions at all since 71% of the entries have NaN in said field.

## Reflection

I am a bit unsure about removing the extra_data, I wonder if it would have been better to replace the NaNs with 0s. Lets say, pessimistically, extra_data is criminal offense, so most people would turn out to have a Nan, meaning they have never had a criminal record. In this case then, we should have replaced NaNs with 0s, not removing the column completely. My decision caused some loss of data, but without specification, I thought I did a good job "cleaning" it.

