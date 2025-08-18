I edited the df sample given in stage 06 (next stage) as my data snippet. I saved it as a csv to data/raw and parquet to data/processed respectively.


Then I validated my saved data by reloading and comaring with the original df. 
This showed my that the date was not automatically converted in my parquet copy, because my validation function came back and said my date had the wrong dtype.

I re-adjusted my parquet saving and explicitly turned date into datetime dtype. 

I also then added the read and write df functions. 

Essentially their purpose is to save time when we read and write to both csvs and parquets as we no longer have to remember/reference their type.

the code itself is relatively straight foward, just type handling. I didnt bother adding add on checks because I have installed my environment already and did not encounter those problems, and if I did it was very obvious. I intend on adding the add-ons to requirements.txt anyway.

