host = 'localhost'
port = 3306
user = 'root'
passwd = 'bit'
db = 'paper_repo'
charset = 'utf8'
"""
create table MirrorFileInfo
(
    id Bigint(20) auto_increment primary key,
    docid Bigint(20),
    title text,
    clc_code Varchar(100),
    index_word Varchar(1024),
    type Int(11),
    finish_time Datetime,
    contributor text,
    organization text,
    bool_check int(10)
);
alter table MirrorFileInfo convert to character set utf8;

create table Citation
(
    id Bigint(20) auto_increment primary key,
    docid Bigint(20),
    title text ,
    reference_id Bigint(20) ,
    reference_paper text ,
    reference_sentence text ,
    finish_time Datetime,
    bool_check int(10) 
);
alter table Citation convert to character set utf8;

create table FrameworkContent
(
    id Bigint(20) auto_increment primary key,
    docid Bigint(20) ,
    title text,
    subsequence Bigint(20),
    subtitle text,
    content text,
    finish_time Datetime,
    bool_check int(10) 
);
alter table FrameworkContent convert to character set utf8;

create table paper_index(
    id Bigint(20) ,
    path text 
);
alter table paper_index convert to character set utf8;
"""