// Hashtable
// 09/28/2021

import java.util.NoSuchElementException;
import java.util.LinkedList;

public class Hashtable<KeyType, ValueType> {
    public class Obj<KeyType, ValueType> {
        private KeyType key;
        private ValueType value;

        public Obj(KeyType key, ValueType value) {
            this.key = key;
            this.value = value;
        }

        public KeyType getKey() {
            return key;
        }
        public ValueType getValue() {
            return value;
        }
    }

    private int capacity;
    private LinkedList<Obj>[] array;

    public Hashtable(int capacity) {
        this.capacity = capacity;
        this.array = new LinkedList[capacity];
    }

    public Hashtable() {
        this.capacity = 20;
        this.array = new LinkedList[capacity];
    }

    public boolean put(KeyType key, ValueType value) {
        if (key == null) {return false;} //check if key is null
        Obj obj = new Obj(key, value); //Obj is a helper class that stores key-value pairs
        int k = key.hashCode() % capacity;
        if (array[k] == null) { //if the given bucket is empty, create a new linked list and store the key-value pair
            array[k] = new LinkedList<Obj>();
            array[k].add(obj);
            if ((size() / (double)this.capacity) >= 0.8) {putHelper();} //double capacity and rehash if load factor >= 0/8
            return true;
        }
        else { //if the given bucket is nonempty
            for (int i = 0; i < array[k].size(); i++) {
                if (array[k].get(i).getKey().equals(key)) {return false;} //check if key is already stored
            }
            array[k].addLast(obj); //the key-value pair is stored at the end of the linked list
            if ((size() / (double)this.capacity) >= 0.8) {putHelper();} //double capacity and rehash if load factor >= 0/8
            return true;
        }
    }
    public void putHelper() { //helper function for doubling capacity and rehashing
        int n = this.capacity; //store current capacity in n
        this.capacity *= 2; //double capacity
        LinkedList<Obj>[] temparray = this.array; //store array in a temporary array
        this.array = new LinkedList[capacity]; //array is now an empty array with doubled capacity
        for (int i = 0; i < n; i++) { //rehash all elements in the temporary array into array
            if (!(temparray[i] == null)) {
                for (int k = 0; k < temparray[i].size(); k++) {
                    put((KeyType)temparray[i].get(k).getKey(), (ValueType)temparray[i].get(k).getValue());
                }
            }
        }
    }

    public ValueType get(KeyType key) throws NoSuchElementException {
        int k = key.hashCode() % capacity;
        if (array[k] == null) {throw new NoSuchElementException();} //throw exception if given bucket is empty
        for (int i = 0; i < array[k].size(); i++) {
            if (array[k].get(i).getKey().equals(key)) {return (ValueType)array[k].get(i).getValue();} //return the associated value if the key is found in the bucket
        }
        throw new NoSuchElementException(); //if the key is not found in the bucket, throw exception

    }
    public int size() {
        int sum = 0;
        for (int i = 0; i < this.capacity; i++) {//traverse through the array and sum the sizes of each linked list
            if (!(array[i] == null)) {
                sum += array[i].size();
            }
        }
        return sum;
    }

    public boolean containsKey(KeyType key) {
        int k = key.hashCode() % capacity;
        if (array[k] == null) {return false;} //if the given bucket is empty, return false
        for (int i = 0; i < array[k].size(); i++) {
            if (array[k].get(i).getKey().equals(key)) {return true;} //if the key is found in the bucket, return true
        }
        return false; //if the key is not found in the bucket, return false
    }

    public ValueType remove(KeyType key) {
        int k = key.hashCode() % capacity;
        if (array[k] == null) {return null;} //if the given bucket is empty, return null
        for (int i = 0; i < array[k].size(); i++) {
            if ((array[k].get(i).getKey().equals(key))) {
                ValueType temp = (ValueType)array[k].get(i).getValue(); //if the key is found in the bucket, store the associated value in temp
                array[k].remove(i); //remove the key-value pair from the linked list
                return temp; //return the associated value
            }
        }
        return null; //if the key is not found in the bucket, return null
    }

    public void clear() {
        for (int i = 0; i < this.capacity; i++) { //traverse through array and clear each linked list
            if (!(array[i] == null)) {
                array[i].clear();
            }
        }
    }
    public int arraySize() {return array.length;} //helper function to access the size of array
}