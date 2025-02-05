# demty2025_cine_lambda

Description of the decision-making process of utilizing the AWS tools to: Count average movie categories and (if possible) a sentiment analysis of movie titles.

## Quick Introduction

As part of the DE MTY BC 2025, a day before this activity, a new DynamoDB table was created with records that contained among other fields: `clasificacion` and `nombre`. With this fields, we where 
requested to create a process to get the average movie `clasification` and probable `genres` of the movies.

## Design

Though the request was simple (apart from the sentiment classification), I chose to use AWS Glue due to the ETL capabilities that allow us to quicly load data from DynamoDB and apply aggregation operations. It's also important to note that Glue allows us to choose an output format and location.

![ETL Flow](https://github.com/user-attachments/assets/9a6450d2-605c-4c8d-901b-8d9268a45e66)


 - The first step in the process requires a crawler that automatically analysis the DynamoDB table and creates a table with the required structure.

 - Once the crawler is done, now it's time to load the data from DynamoDB by selecting the newly created Glue table.

 - As a third step, a grouping operation is applied on the `clasificacion` table that allows to apply a `max` aggregation to get the most common `clasification`.

 - As an almost final step, the new max column is selected, along with the `clasification` column so they can be sent to the output table.

 - Finally, a MYSQL table, in an already available database, is ready to receive the data and store it for further use with possible an API to display the results.


### Why not Lambda

Though completely possible to choose lambda, I considered that the data source could potentially grow and cause longer execution times and thus money, to execute the process in a Lambda. In addition, the process would require more processing power due to the convertion from JSON in a growing data source.


