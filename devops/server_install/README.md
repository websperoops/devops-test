
## Create django user for mysql database
**DONT FORGET TO CHANGE PASSWORD IN THE COMMAND**
```
GRANT ALL PRIVILEGES ON *.* TO 'django'@'localhost' IDENTIFIED BY '<SET THIS PASSOWD>';
```

## Create blocklightx database
```
CREATE DATABASE `blocklightx` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_bin */;
```
