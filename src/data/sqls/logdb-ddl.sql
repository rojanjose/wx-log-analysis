
--Create file_io table
CREATE TABLE IF NOT EXISTS public.file_io
(
    id integer NOT NULL,
    io_timestamp timestamp with time zone,
    file_accessed character varying(20) COLLATE pg_catalog."default",
    disk_reads integer,
    disk_writes integer,
    "user" character varying(20) COLLATE pg_catalog."default",
    CONSTRAINT file_io_pkey PRIMARY KEY (id)
)

