# [SwampCTF 2019 Pwn] Serial Killer

## Flavor Text
Hacking for fun is dead. Hacking in 2077 is all about business.

One of your more trigger-happy employers has managed to land themselves on the city PD's list of "wanted killers".
Earn your keep and erase any record of them from the database. If you happen to find anything else of value while on the job, submit it here.

* Flag: `flag{accomp1Ic3_in_De_5eri4l_killing}`
* Expected difficulty: medium

## Description
Idea here is to use Map<methodName, arguments>
take entry.getKey() from map entry and use it as a method name, and
take entry.getValue() as arguments to method we got in key of entry.
Using this we can create chain of method calls if there are multiple
key, value pairs.

To trigger the chain, while deserializing the map setValue will be called
and a vulnerability will be added, to keep invoking method with args as described
earlier and state of chain will be maintained in the vulnerability

Constructor will allow to initialize the gunPowederClazz with class
"java.lang.Runtime" and next calls to setValue during deserialization
gives the opportunity to make a chain till getRuntime().exec()

## Challenge Solution
Recognize the deserialization vulnerability. Create a Java socket server that can send the right serialized object.
Compiled using `OpenJDK Runtime Environment (build 1.8.0_191-8u191-b12-2ubuntu0.16.04.1-b12)`
1. Create a map of SerialKillersMap with gunPowder as "java.lang.Runtime"
2. then create a chain by passing key(method name): value (arguments)
- getRuntime: null
- exec(): "any command to run" in base64 encoded form
3. Serialize the map and send it to server

Run the local server using netcat: `nc.traditional -l -p 1111 -v -c 'java -jar Server.jar'`.
Create a connect back listener for the command results: `nc -l -v localhost -p 60000`.
Finally, run the exploit: `java com.swampctf.serialkiller.Solution localhost 1111 | grep -v null`.

```
$ nc -l -v localhost -p 60000
Listening on [localhost] (family 0, port 60000)
Connection from [127.0.0.1] port 60000 [tcp/*] accepted (family 2, sport 35636)
flag{accomp1Ic3_in_De_5eri4l_killing}
```
