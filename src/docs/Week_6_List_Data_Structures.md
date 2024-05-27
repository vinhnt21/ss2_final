
# Week 6: List Data Structures - Implementations and Operations

## 1. Introduction to Lists
- A list is a collection of elements, where each element has a specific position.
- Lists allow duplicate elements and provide a way to access, insert, and delete elements based on their position.

## 2. Types of Lists
### 2.1. ArrayList
- **Implementation:** Resizable array.
- **Characteristics:** Fast random access, slower inserts and deletes (except at the end).
- **Use Cases:** When you need fast access to elements by index.

### 2.2. LinkedList
- **Implementation:** Doubly linked list.
- **Characteristics:** Fast inserts and deletes, slower random access.
- **Use Cases:** When frequent addition and removal of elements are required.

## 3. Common Operations on Lists
### 3.1. Adding Elements
- **ArrayList:** `add(E element)`, `add(int index, E element)`
- **LinkedList:** `add(E element)`, `add(int index, E element)`, `addFirst(E element)`, `addLast(E element)`

### 3.2. Accessing Elements
- **ArrayList:** `get(int index)`
- **LinkedList:** `get(int index)`, `getFirst()`, `getLast()`

### 3.3. Removing Elements
- **ArrayList:** `remove(int index)`, `remove(Object o)`
- **LinkedList:** `remove(int index)`, `remove(Object o)`, `removeFirst()`, `removeLast()`

### 3.4. Checking Size
- `size()`

### 3.5. Iterating Through the List
- Using a for-loop, for-each loop, or iterator.

## 4. Sample Code in Java

### 4.1. ArrayList Example
```java
import java.util.ArrayList;

public class ArrayListExample {
    public static void main(String[] args) {
        // Creating an ArrayList
        ArrayList<String> list = new ArrayList<>();

        // Adding elements
        list.add("Apple");
        list.add("Banana");
        list.add("Cherry");
        list.add(1, "Blueberry");

        // Accessing elements
        System.out.println("Element at index 2: " + list.get(2));

        // Removing elements
        list.remove(1); // Removes "Blueberry"
        list.remove("Cherry");

        // Checking size
        System.out.println("Size of the list: " + list.size());

        // Iterating through the list
        for (String fruit : list) {
            System.out.println(fruit);
        }
    }
}
```

### 4.2. LinkedList Example
```java
import java.util.LinkedList;

public class LinkedListExample {
    public static void main(String[] args) {
        // Creating a LinkedList
        LinkedList<String> list = new LinkedList<>();

        // Adding elements
        list.add("Apple");
        list.add("Banana");
        list.add("Cherry");
        list.addFirst("Blueberry");
        list.addLast("Date");

        // Accessing elements
        System.out.println("First element: " + list.getFirst());
        System.out.println("Last element: " + list.getLast());

        // Removing elements
        list.removeFirst(); // Removes "Blueberry"
        list.removeLast();  // Removes "Date"
        list.remove(1);     // Removes "Cherry"

        // Checking size
        System.out.println("Size of the list: " + list.size());

        // Iterating through the list
        for (String fruit : list) {
            System.out.println(fruit);
        }
    }
}
```
