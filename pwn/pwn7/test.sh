#!/bin/bash

# start a local netcat server to get the flag with command: nc -l 60000
# 60000 is hardcoded for now
cd src
javac -Xlint:unchecked -cp ".:../lib/commons-collections-3.2.2-bin/commons-collections-3.2.2/commons-collections-3.2.2.jar" com/swampctf/serialkiller/*.java
java -cp ".:../lib/commons-collections-3.2.2-bin/commons-collections-3.2.2/commons-collections-3.2.2.jar" com.swampctf.serialkiller.Server 5000 & 2>&1
java -cp ".:../lib/commons-collections-3.2.2-bin/commons-collections-3.2.2/commons-collections-3.2.2.jar" com.swampctf.serialkiller.Solution localhost 5000 & 2>&1 

