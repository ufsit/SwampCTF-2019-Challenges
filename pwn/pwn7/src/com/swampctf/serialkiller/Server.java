package com.swampctf.serialkiller;

import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.lang.reflect.Constructor;
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Map;
import java.util.Map.Entry;
import java.util.Set;

import org.apache.commons.collections.Transformer;
import org.apache.commons.collections.map.TransformedMap;

import com.swampctf.serialkiller.AbstractSerialKillerMap.EntrySet;

public class Server {

	public static void main(String[] args) {

		/*int portNumber = -1;
		if (args.length == 0) {
			System.out.println("Enter a valid socket in range 1025-65536 to listen on");
			System.exit(1);
		}
		else {
			portNumber = Integer.parseInt(args[0]);
		}*/
		ObjectInputStream ois = null;
		//ServerSocket serverSocket = null;
		try {
			System.out.println("Ready.");
			//System.out.println("Going to listen on port: " + portNumber);
			//serverSocket = new ServerSocket(portNumber);
			//Socket socket = serverSocket.accept();
			//ois =  new ObjectInputStream(socket.getInputStream());
			ois =  new ObjectInputStream(System.in);
			ois.readObject();
			System.out.println("Serialized data read complete.");
		} catch (IOException e2) {
			e2.printStackTrace();
		} catch (ClassNotFoundException e) {
			e.printStackTrace();
		} finally {
			try {
				ois.close();
				//serverSocket.close();
			} catch (IOException e) {
				e.printStackTrace();
			}
		}
	}
}
