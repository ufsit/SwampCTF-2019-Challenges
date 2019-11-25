#!/bin/sh
set -eu
javac -Xlint:unchecked -cp ".:../lib/commons-collections-3.2.2-bin/commons-collections-3.2.2/commons-collections-3.2.2.jar" com/swampctf/serialkiller/*.java
jar cmvf META-INF/MANIFEST.MF serial_killer.jar commons-collections-3.2.2.jar com/swampctf/serialkiller/Server.class com/swampctf/serialkiller/*Serial*class
echo "Jar built!"
