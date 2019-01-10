--Create scripts for all tables except Master MRDS data
set timezone ='America/New_York';

drop table if exists public.t_raster_cropped;
drop table if exists public.t_raster_master;
drop table if exists public.t_site;

CREATE TABLE t_site (
    site_id serial CONSTRAINT t_site_pk PRIMARY KEY,
    site_name text,
    source text,
    latitude double precision NOT NULL,
    longitude double precision NOT NULL,
    com_type text,
    commodity_1 text,
    commodity_2 text,
    commodity_3 text,
    oper_type text,
    dep_type text,
    prod_size text,
    dev_stat text,
    ore text,
    gangue text,
    other_matl text,
    orebody_fm text,
    work_type text,
    model text,
    alteration text,
    conc_proc text,
    names text,
    ore_ctrl text,
    hrock_unit text,
    hrock_type text,
    arock_unit text,
    arock_type text,
    structure text,
    tectonic text,
    disc_yr text,
    prod_yrs text,
    gold text,
    silver text,
    lead text,
    tin text,
    copper text,
    antimony text,
    molybdenum text,
    iron text,
    zinc text,
    chromium text,
    cobalt text,
    volcanic_materials text,
    wollastone text,
    bismuth text,
    arsenic text,
    kaolinite text,
    quartz text,
    calcium text,
    mica text,
    silica text,
    marble text,
    crtd_dt timestamp without time zone DEFAULT now() NOT NULL,
    updt_dt timestamp without time zone,
    classifier character varying(16)
);

create table t_raster_master(
    master_id serial CONSTRAINT t_master_pk PRIMARY KEY,
    filename varchar(64),
    data_type varchar(64)
);

create table t_raster_cropped(
    raster_id serial CONSTRAINT t_raster_pk PRIMARY KEY,
    raster_name varchar(32) NOT NULL,
    site_id integer REFERENCES public.t_site(site_id) ON DELETE CASCADE,
    resolution varchar(16),
    filename varchar(64),
    filepath varchar(512),
    crtd_dt TIMESTAMP NOT NULL DEFAULT NOW(),
    updt_dt TIMESTAMP default null	
);
