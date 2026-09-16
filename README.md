#OS TASK1
# Multithreading Task

## Project Title

**Multithreading and Concurrent Matrix Processing**

## Introduction

This task demonstrates the use of **multithreading and concurrent processing** using Python and web technologies.

The project consists of three parts:

1. Producer-Consumer Problem using Python Threads
2. 100 × 100 Matrix Multiplication using Python Threads
3. HTML-based Matrix Multiplication Visualization using Web Workers

The main objective is to understand how multiple threads can execute tasks concurrently, how shared resources are synchronized, and how parallel processing can be visualized.

---

## Task 1: Producer-Consumer Problem

### Description

The Producer-Consumer problem demonstrates communication and synchronization between two threads using a shared buffer.

A producer generates items and places them into the buffer, while a consumer removes and processes those items.

### Working

* A producer thread generates 10 items.
* A consumer thread consumes the generated items.
* A shared buffer is used to temporarily store the items.
* The buffer has a maximum capacity of 5 items.
* Python's Queue is used for safe communication between the threads.
* If the buffer becomes full, the producer waits.
* If the buffer becomes empty, the consumer waits.
* Both producer and consumer execute concurrently.
* Threads are joined after their execution is completed.

### Concepts Demonstrated

* Multithreading
* Producer-Consumer synchronization
* Shared resources
* Thread communication
* Queue-based buffering
* Thread joining
* Concurrent execution

### Expected Result

The terminal displays the items produced and consumed along with the current buffer size. After all items are processed, a completion message is displayed.

---

# Task 2: 100 × 100 Matrix Multiplication Using Multithreading

## Description

This task performs multiplication of two **100 × 100 matrices** using Python multithreading.

The program creates a separate thread for every individual multiplication contribution.

### Working

Two 100 × 100 matrices are generated with random values between 1 and 10.

For every output element, the corresponding row of the first matrix and column of the second matrix are multiplied and accumulated.

The program uses:

* Python Threading
* Random
* Time
* Matrix operations
* Locks for synchronization

### Number of Operations

For two 100 × 100 matrices:

**Number of output elements:**

100 × 100 = **10,000**

**Individual multiplication operations:**

100 × 100 × 100 = **1,000,000**

Therefore, the program creates **1,000,000 threads** to perform the individual multiplication operations.

### Synchronization

Since multiple threads update the shared result matrix, locks are used to prevent multiple threads from modifying the same result element at the same time.

This ensures that the final matrix is calculated correctly.

### Result Verification

The program first calculates the matrix multiplication sequentially.

The threaded result is then compared with the sequential result.

If both results are the same, the program confirms that the threaded matrix multiplication is correct.

### Output

The program displays:

* Matrix size
* Number of worker threads created
* Execution time
* Whether the threaded result is correct
* A sample result from the output matrix

### Concepts Demonstrated

* Python multithreading
* Concurrent execution
* Matrix multiplication
* Thread synchronization
* Locks
* Shared memory
* Performance measurement
* Result verification

---

# Task 3: HTML Matrix Multiplication Visualization

## Description

This task provides a visual representation of matrix multiplication using **HTML, CSS and JavaScript**.

JavaScript **Web Workers** are used to perform calculations separately from the main webpage.

### Working

The webpage displays:

* Input Matrix A
* Input Matrix B
* Output Matrix

The user can select a matrix size between 2 and 100.

After starting the process:

1. Random matrices are generated.
2. Multiple Web Workers are created.
3. Workers perform matrix multiplication calculations.
4. Each multiplication contribution is sent back to the main webpage.
5. The output matrix is updated as calculations are completed.
6. The webpage displays the current calculation progress.
7. After all operations are completed, the final output matrix is displayed.

### Main Features

* Interactive matrix size selection
* Random matrix generation
* Multiple Web Workers
* Concurrent processing
* Real-time progress display
* Worker contribution display
* Output matrix visualization
* Matrix sizes up to 100 × 100

### Technologies Used

* HTML
* CSS
* JavaScript
* Web Workers
* Browser-based concurrent processing

---

# Project Objectives

The main objectives of this task are:

* To understand multithreading.
* To implement concurrent execution.
* To understand the Producer-Consumer problem.
* To perform matrix multiplication using threads.
* To understand thread synchronization.
* To use locks for protecting shared resources.
* To understand Web Workers.
* To visualize concurrent matrix processing.
* To compare threaded and sequential results.

---

# Software Requirements

## Python

Python is required to run the Producer-Consumer and Matrix Multiplication programs.

## Web Browser

A modern web browser such as Chrome, Edge or Firefox is required to run the HTML visualization.

---

# Project Structure

The project contains:

* Producer-Consumer Python program
* Threaded Matrix Multiplication Python program
* HTML Matrix Visualization
* README documentation

---

# Execution

## Producer-Consumer

Run the Producer-Consumer Python program.

The terminal displays the production and consumption of items and the buffer status.

## Matrix Multiplication

Run the Python matrix multiplication program.

The program generates two 100 × 100 matrices, performs threaded multiplication and verifies the result.

## HTML Visualization

Open the HTML file in a web browser.

Select the required matrix size and click **Start** to view the matrix multiplication process.

---

# Applications

Multithreading and concurrent processing are useful in:

* Data processing
* Scientific computing
* Image processing
* Machine Learning
* Web applications
* Server applications
* Real-time systems
* Large-scale computations

---

# Advantages

* Allows multiple tasks to execute concurrently.
* Improves utilization of system resources.
* Demonstrates synchronization of shared resources.
* Helps understand parallel processing.
* Provides practical experience with threads.
* Web Workers allow calculations to run separately from the main webpage.

---

# Conclusion

This task demonstrates important concepts of **multithreading, synchronization and concurrent processing**.

The Producer-Consumer program demonstrates communication between threads using a shared queue. The matrix multiplication program demonstrates how individual multiplication operations can be handled using separate threads and synchronized using locks. The HTML application provides a visual demonstration of matrix processing using Web Workers.

Overall, the task provides practical understanding of how concurrent execution can be implemented using Python threads and browser-based Web Workers.
