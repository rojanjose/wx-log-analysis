

--Select io records for a time window
SELECT * from postgre_log.public.file_io
                WHERE io_timestamp BETWEEN TIMESTAMP '2024-05-09 17:00:00.000' AND TIMESTAMP '2024-05-09 20:12:00.000'


--Sample federated query joining data from two catalog sources.
SELECT types.car, rides.company
 FROM "hive_data"."taxi"."taxirides" rides, "iceberg_data"."my_schema"."taxi_type" types
    WHERE 
        rides.company = types.company


