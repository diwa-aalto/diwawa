#!/bin/sh

if [ "$#" -lt 1 ]; then
   echo "Usage: $0 "
   exit
fi

SRC=$1
DST=$1.sqlite3.sql
DB=$1.sqlite3.db
ERR=$1.sqlite3.err

cat $SRC |
grep -v ' KEY "' |
grep -v ' UNIQUE KEY "' |
grep -v ' PRIMARY KEY ' |

sed 's/ENGINE=MyISAM/ /g' |
sed 's/DEFAULT/ /g' |
sed 's/CHARSET=[a-zA-Z0-9]*/ /g' |
sed 's/AUTO_INCREMENT=[0-9]*/ /g' |

sed 's/\\r\\n/\\n/g' |
sed 's/\\"/"/g' |
sed '/^SET/d' |
sed 's/ unsigned / /g' |
sed 's/ auto_increment/ primary key autoincrement/g' |
sed 's/ smallint([0-9]*) / integer /g' |
sed 's/ tinyint([0-9]*) / integer /g' |
sed 's/ int([0-9]*) / integer /g' |
sed 's/ character set [^ ]* / /g' |
sed 's/ enum([^)]*) / varchar(255) /g' |
sed 's/ on update [^,]*//g' |
sed 's/UNLOCK TABLES;//g' |
sed 's/LOCK TABLES [^;]*;//g' |
perl -e 'local $/;$_=<>;s/,\n\)/\n\)/gs;print "begin;\n";print;print "commit;\n"' |
perl -pe '
  if (/^(INSERT.+?)\(/) {
     $a=$1;
     s/\\'\''/'\'\''/g;
     s/\\n/\n/g;
     s/\),\(/\);\n$a\(/g;
  }
  ' > $DST

cat $DST | sqlite3 $DB > $ERR

ERRORS=`cat $ERR | wc -l`

if [ "$ERRORS" -eq "0" ]; then
	echo "Conversion completed without error. Your db is ready under: $DB"
	echo "\$ sqlite3 $DB"
  rm -f $ERR
else
   echo "There were errors during conversion. \
	Please review $ERR and $DST for details."
fi

