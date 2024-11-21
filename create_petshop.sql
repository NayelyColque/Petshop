create database petshop;
use petshop;

create table petshop (
    id			int identity(1,1) primary key,
    tipo_pet	varchar(50),
    nome_pet	varchar(50),
    idade		int
);

select * from petshop

