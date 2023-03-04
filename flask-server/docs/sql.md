创建 `xasa` 数据库

``` sql
CREATE DATABASE xasa;
```

创建 `users` 表
``` sql
CREATE TABLE `users` (
    id int primary key NOT NULL AUTO_INCREMENT COMMENT 'primary key' ,
    name varchar(128) COMMENT 'user name',
    password varchar(256) COMMENT 'user password',
    email varchar(128) COMMENT 'email',
    description text COMMENT 'description',
    KEY `idx_name` (`name`),
    UNIQUE KEY `uni_name` (`name`)
) ENGINE=InnoDB CHARSET=utf8 AUTO_INCREMENT=20220801;
```

创建 `reports` 表
``` sql
CREATE TABLE `reports` (
    id int primary key NOT NULL AUTO_INCREMENT COMMENT 'primary key' ,
    name varchar(128) COMMENT 'report name',
    status varchar(16) COMMENT 'report status',
    progress varchar(128) COMMENT 'progress',
    create_at varchar(128) COMMENT 'create time',
    owner varchar(128) COMMENT 'owner',
    KEY `idx_name` (`name`),
    UNIQUE KEY `uni_name` (`name`)
) ENGINE=InnoDB CHARSET=utf8 AUTO_INCREMENT=21220801;
```
