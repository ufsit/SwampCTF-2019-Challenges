package com.swampctf.serialkiller;

import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.util.HashMap;
import java.util.Map;
import java.util.Map.Entry;

import org.apache.commons.collections.Transformer;
import org.apache.commons.collections.map.TransformedMap;

public class TestServer {

	public static void main(String [] args) {
		Transformer transformer = new Transformer() {

			@Override
			public Object transform(Object input) {
				// TODO Auto-generated method stub
				return input + "_added_value";
			}
		};
		
		HashMap<String, String> innermap = new HashMap<String, String>();
		innermap.put("key", "value");
		Map outermap = TransformedMap.decorate(innermap, null, transformer);

		Map.Entry elem = (Entry) outermap.entrySet().iterator().next();
		System.out.println("1:" + elem.getClass().getName());
		System.out.println("2:" + elem.getClass().getCanonicalName());
		System.out.println("3:" + outermap.getClass().getName());
		Map outermap1 = TransformedMap.decorate(innermap, null, null);
		Map.Entry elem1 = (Entry) outermap1.entrySet().iterator().next();
		System.out.println("4:" + elem1.getClass().getName());

		innermap.clear();
		
		/*
		SerialKillersMap smap = new SerialKillersMap(innermap, "java.lang.Runtime");
		smap.put("getRuntime", "");
		smap.put("exec", "cmd /c start cmd.exe /K \"dir && ping localhost\"");
		//Map sOuterMap = TransformedMap.decorate(innermap, null, null);
		Set set = smap.entrySet();
		Iterator it = smap.entrySet().iterator();
		String [] values = {null, "cmd /c start cmd.exe /K \"dir && ping localhost\""};
		int i = 0;
		while(it.hasNext()){
			Map.Entry es = (Entry) it.next();
			es.setValue(values[i]);
			System.out.println("with " + values[i]);
			i++;
		}
		*/
		String fileName = "map.bin";
		SerialKillersMap smap = new SerialKillersMap(innermap, "java.lang.Runtime");
		smap.put("getRuntime", null);
		smap.put("exec", "cmd /c start cmd.exe /K \"dir && ping localhost\"");
		try {
			ObjectOutputStream oos = new ObjectOutputStream(new FileOutputStream(fileName));
			oos.writeObject(smap);
			oos.flush();
			oos.close();
			ObjectInputStream ois = new ObjectInputStream(new FileInputStream(fileName));
			SerialKillersMap rsamp = (SerialKillersMap) ois.readObject();
			rsamp.printMap();
			System.out.println("");
			ois.close();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (ClassNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} finally {
			
		}
		
		/*
		try {
			Class claz = Class.forName("java.lang.Runtime");
			Method method = claz.getMethod("getRuntime");
			// Constructor ctor = claz.getDeclaredConstructor();
			// System.out.println(ctor.isAccessible());
			Object runtime = method.invoke(null);
			try {
				((Runtime)claz.getMethod("getRuntime").invoke(null)).exec("sdf");
			} catch (IOException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
			Runtime rt = java.lang.Runtime.getRuntime();
			System.out.println(runtime.toString());
			// Class runtimeClazz = method.getReturnType();
			Method execMethod = runtime.getClass().getMethod("exec", String.class);
			Object shell = execMethod.invoke(runtime, "cmd /c start cmd.exe /K \"dir && ping localhost\"");
		} catch (NoSuchMethodException | SecurityException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (IllegalAccessException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (IllegalArgumentException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (InvocationTargetException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (ClassNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
*/
	}
}
