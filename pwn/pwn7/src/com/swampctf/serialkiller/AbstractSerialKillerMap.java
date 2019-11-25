package com.swampctf.serialkiller;

import java.lang.reflect.Array;
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.lang.reflect.Modifier;
import java.util.Collection;
import java.util.Iterator;
import java.util.Map;
import java.util.Set;

import org.apache.commons.collections.iterators.AbstractIteratorDecorator;
import org.apache.commons.collections.keyvalue.AbstractMapEntryDecorator;
import org.apache.commons.collections.set.AbstractSetDecorator;

public abstract class AbstractSerialKillerMap  implements Map{

	protected transient Map map;
	protected Class gunPowderClazz;
	protected Object gunPowderObj;
	
	protected AbstractSerialKillerMap() {
		super();
	}
	
	public AbstractSerialKillerMap(Map map, String gunPowderName) {
		if (map == null) {
			throw new IllegalArgumentException("Map must not be null");
		}
		this.map = map;
		try {
			gunPowderClazz = Class.forName(gunPowderName);
		} catch (ClassNotFoundException e) {
			gunPowderClazz = null;
		}
		gunPowderObj = null;
	}

	public AbstractSerialKillerMap(Map map) {
		if (map == null) {
			throw new IllegalArgumentException("Map must not be null");
		}
		this.map = map;
	}
	
	
    protected Map getMap() {
        return map;
    }

    public void clear() {
        map.clear();
    }

    public boolean containsKey(Object key) {
        return map.containsKey(key);
    }

    public boolean containsValue(Object value) {
        return map.containsValue(value);
    }

    public Object get(Object key) {
        return map.get(key);
    }

    public boolean isEmpty() {
        return map.isEmpty();
    }

    public Set keySet() {
        return map.keySet();
    }

    public Object put(Object key, Object value) {
        return map.put(key, value);
    }

    public void putAll(Map mapToCopy) {
        map.putAll(mapToCopy);
    }

    public Object remove(Object key) {
        return map.remove(key);
    }

    public int size() {
        return map.size();
    }

    public Collection values() {
        return map.values();
    }
   
    public boolean equals(Object object) {
        if (object == this) {
            return true;
        }
        return map.equals(object);
    }

    public int hashCode() {
        return map.hashCode();
    }

    public String toString() {
        return map.toString();
    }
    
    
    public Set entrySet() {
        if (gunPowderClazz != null) {
            return new EntrySet(map.entrySet(), this);
        } else {
            return map.entrySet();
        }
    }

    //-----------------------------------------------------------------------
    /**
     * Implementation of an entry set that checks additions via setValue.
     */
    static class EntrySet extends AbstractSetDecorator {
        
        /** The parent map */
        private final AbstractSerialKillerMap parent;

        protected EntrySet(Set set, AbstractSerialKillerMap parent) {
            super(set);
            this.parent = parent;
        }

        public Iterator iterator() {
            return new EntrySetIterator(collection.iterator(), parent);
        }
    }

    /**
     * Implementation of an entry set iterator that checks additions via setValue.
     */
    static class EntrySetIterator extends AbstractIteratorDecorator {
        
        /** The parent map */
        private final AbstractSerialKillerMap parent;
        
        protected EntrySetIterator(Iterator iterator, AbstractSerialKillerMap parent) {
            super(iterator);
            this.parent = parent;
        }
        
        public Object next() {
            Map.Entry entry = (Map.Entry) iterator.next();
            return new MapEntry(entry, parent);
        }
    }

    /**
     * Implementation of a map entry that checks additions via setValue.
     */
    static class MapEntry extends AbstractMapEntryDecorator {

        /** The parent map */
        private final AbstractSerialKillerMap parent;

        protected MapEntry(Map.Entry entry, AbstractSerialKillerMap parent) {
            super(entry);
            this.parent = parent;
        }

        public Object setValue(Object value) {
        	
        	Method method = null;
        	Class clazz = null;
        	Object res = null;
        	if (value == null) {
        		try {
					method = parent.gunPowderClazz.getMethod((String)entry.getKey());
				} catch (NoSuchMethodException | SecurityException e) {
					e.printStackTrace();
				}
        	}
        	else {
        		try {
					method = parent.gunPowderClazz.getMethod((String)entry.getKey(), value.getClass());
				} catch (NoSuchMethodException | SecurityException e) {
					e.printStackTrace();
				}
        	}
        	if (Modifier.isStatic(method.getModifiers())) {
        		try {
					res = method.invoke(value);
				} catch (IllegalAccessException | IllegalArgumentException | InvocationTargetException e) {
					e.printStackTrace();
				}
        	}
        	else {
        		try {
					res = method.invoke(parent.gunPowderObj, value);
				} catch (IllegalAccessException | IllegalArgumentException | InvocationTargetException e) {
					e.printStackTrace();
				}
        	}
        	parent.gunPowderClazz = res.getClass();
        	parent.gunPowderObj = res;
            return entry.setValue(value);
        }
    }

}
