import threading
import time
import random
import queue

# Shared buffer with a fixed maximum size
BUFFER_LIMIT = 5
shared_buffer = queue.Queue(maxsize=BUFFER_LIMIT)

# Used to gracefully stop the threads
stop_signal = threading.Event()


def producer(name, item_count):
    """Generates items and pushes them into the shared buffer."""
    for i in range(item_count):
        if stop_signal.is_set():
            break

        item = f"{name}-item-{i}"
        wait_time = random.uniform(0.1, 0.5)
        time.sleep(wait_time)  # simulate time taken to "produce" something

        shared_buffer.put(item)  # blocks automatically if buffer is full
        print(f"[{name}] produced -> {item}  (buffer size: {shared_buffer.qsize()})")

    print(f"[{name}] finished producing.")


def consumer(name, item_count):
    """Pulls items from the shared buffer and processes them."""
    for i in range(item_count):
        if stop_signal.is_set():
            break

        item = shared_buffer.get()  # blocks automatically if buffer is empty
        wait_time = random.uniform(0.2, 0.6)
        time.sleep(wait_time)  # simulate time taken to "consume" something

        print(f"[{name}] consumed -> {item}  (buffer size: {shared_buffer.qsize()})")
        shared_buffer.task_done()

    print(f"[{name}] finished consuming.")


def main():
    num_items = 10

    producer_thread = threading.Thread(target=producer, args=("Producer-1", num_items))
    consumer_thread = threading.Thread(target=consumer, args=("Consumer-1", num_items))

    producer_thread.start()
    consumer_thread.start()

    producer_thread.join()
    consumer_thread.join()

    print("All items produced and consumed. Program complete.")


if __name__ == "__main__":
    main()