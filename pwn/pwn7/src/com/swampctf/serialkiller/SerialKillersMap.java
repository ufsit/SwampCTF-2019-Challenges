package com.swampctf.serialkiller;

import java.io.IOException;
import java.io.ObjectOutputStream;
import java.io.Serializable;
import java.lang.reflect.Method;
import java.util.Base64;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Map;
import java.util.Set;

import org.apache.commons.collections.map.HashedMap;

public class SerialKillersMap extends AbstractSerialKillerMap implements Serializable {

	/**
	 * Serialization version
	 */
	private static final String serialVersionUID = "Fill it with gunpowder to start the serial killing machine";

	protected SerialKillersMap(Map map, String gunPowderName) {
		super(map, gunPowderName);
	}

	private void writeObject(ObjectOutputStream out) throws IOException {
		out.defaultWriteObject();
		for (Object obj : map.entrySet()) {
			Entry<Object, Object> entry = (Entry<Object, Object>) obj;
			if (entry.getKey() instanceof String && (entry.getValue() instanceof String || entry.getValue() == null
					|| entry.getValue() instanceof String[])) {
				if (entry.getValue() instanceof String) {
					entry.setValue(Base64.getEncoder().encodeToString(((String) entry.getValue()).getBytes()));
				}
				else if (entry.getValue() instanceof String[]) {
					String [] b64StringArr = new String [((String [])entry.getValue()).length];
					for (int i = 0; i < ((String[])entry.getValue()).length ; i++) {
						b64StringArr[i] = Base64.getEncoder().encodeToString(((String[])entry.getValue())[i].getBytes());
					}
					entry.setValue(b64StringArr);
				}
			}
		}
		out.writeObject(map);
		out.writeObject(gunPowderClazz);
	}

	private void readObject(java.io.ObjectInputStream in) throws ClassNotFoundException, IOException {
		in.defaultReadObject();
		map = (Map) in.readObject();
		gunPowderClazz = (Class) in.readObject();
		SerialKillersMap inSerialKillersMap = new SerialKillersMap(map, gunPowderClazz.getName());
		for (Object obj : inSerialKillersMap.entrySet()) {
			Entry<Object, Object> entry = (Entry<Object, Object>) obj;
			if (entry.getKey() instanceof String && (entry.getValue() instanceof String || entry.getValue() == null
					|| entry.getValue() instanceof String[])) {
				if (entry.getValue() instanceof String) {
					entry.setValue(new String((Base64.getDecoder().decode((String) entry.getValue())), "UTF-8"));
				} else if (entry.getValue() instanceof String[]) {
					String [] b64StringArr = new String [((String [])entry.getValue()).length];
					for (int i = 0; i < ((String[])entry.getValue()).length ; i++) {
						b64StringArr[i] = new String(Base64.getDecoder().decode(((String[])entry.getValue())[i]), "UTF-8");
					}
					entry.setValue(b64StringArr);
				}
				else {
					entry.setValue(entry.getValue());
				}
			}
		}
	}

	public void printMap() {
		for (Object entry : map.entrySet()) {
			System.out.println(((Entry) entry).getKey());
		}
	}

}
