# OS_TASK_1
# Multithreading Projects

This repository contains three multithreading projects implemented using Python and JavaScript.

## Projects

1. Producer-Consumer Problem
2. 100×100 Matrix Multiplication Using TensorFlow and Multithreading
3. Threaded Matrix Laboratory Using HTML, CSS, JavaScript and Web Workers

---

# 1. Producer-Consumer Problem

## Description

The Producer-Consumer program demonstrates communication between a producer thread and a consumer thread using a shared bounded buffer.

The producer generates 10 items and places them into a shared queue. The consumer retrieves and processes the items.

The shared buffer has a maximum capacity of 5 items.

## Concepts Used

* Python threading
* Producer-Consumer model
* Shared buffer
* Queue
* Thread synchronization
* Blocking operations
* Threading Event

## Code

Save as `producer_consumer.py`.

```python
import threading
import time
import random
import queue

BUFFER_LIMIT = 5
shared_buffer = queue.Queue(maxsize=BUFFER_LIMIT)

stop_signal = threading.Event()


def producer(name, item_count):
    for i in range(item_count):
        if stop_signal.is_set():
            break

        item = f"{name}-item-{i}"
        wait_time = random.uniform(0.1, 0.5)
        time.sleep(wait_time)

        shared_buffer.put(item)
        print(
            f"[{name}] produced -> {item} "
            f"(buffer size: {shared_buffer.qsize()})"
        )

    print(f"[{name}] finished producing.")


def consumer(name, item_count):
    for i in range(item_count):
        if stop_signal.is_set():
            break

        item = shared_buffer.get()
        wait_time = random.uniform(0.2, 0.6)
        time.sleep(wait_time)

        print(
            f"[{name}] consumed -> {item} "
            f"(buffer size: {shared_buffer.qsize()})"
        )

        shared_buffer.task_done()

    print(f"[{name}] finished consuming.")


def main():
    num_items = 10

    producer_thread = threading.Thread(
        target=producer,
        args=("Producer-1", num_items)
    )

    consumer_thread = threading.Thread(
        target=consumer,
        args=("Consumer-1", num_items)
    )

    producer_thread.start()
    consumer_thread.start()

    producer_thread.join()
    consumer_thread.join()

    print("All items produced and consumed. Program complete.")


if __name__ == "__main__":
    main()
```

## Run

```bash
python producer_consumer.py
```

## Expected Output

```text
[Producer-1] produced -> Producer-1-item-0
[Consumer-1] consumed -> Producer-1-item-0
[Producer-1] produced -> Producer-1-item-1
[Consumer-1] consumed -> Producer-1-item-1
...
[Producer-1] finished producing.
[Consumer-1] finished consuming.
All items produced and consumed. Program complete.
```

---

# 2. 100×100 Matrix Multiplication

## Description

This program performs multiplication of two 100×100 matrices using Python multithreading and TensorFlow.

A `ThreadPoolExecutor` is used with 32 worker threads.

Each output cell is calculated as a separate task.

For a 100×100 matrix:

```text
100 × 100 = 10,000 output cells
```

Each output cell requires 100 scalar multiplications.

Therefore:

```text
100 × 100 × 100 = 1,000,000 scalar multiplications
```

The result is also verified using TensorFlow's `tf.linalg.matmul()`.

## Concepts Used

* Matrix multiplication
* Multithreading
* ThreadPoolExecutor
* TensorFlow
* NumPy
* Thread synchronization
* Lock
* Matplotlib animation
* Result verification

## Required Libraries

```bash
pip install numpy tensorflow matplotlib pillow
```

## Code

Save as `matrix_threading.py`.

```python
import time
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
import matplotlib.animation as animation

N = 100
WORKER_THREADS = 32
SNAPSHOT_EVERY = 40

tf.random.set_seed(7)

A = tf.constant(
    tf.random.uniform(
        (N, N),
        minval=1,
        maxval=10,
        dtype=tf.int32
    )
)

B = tf.constant(
    tf.random.uniform(
        (N, N),
        minval=1,
        maxval=10,
        dtype=tf.int32
    )
)

C = np.zeros((N, N), dtype=np.int64)
done_mask = np.zeros((N, N), dtype=bool)

write_lock = threading.Lock()


def compute_cell(row, col):
    row_vals = A[row, :]
    col_vals = B[:, col]

    products = tf.multiply(row_vals, col_vals)
    total = tf.reduce_sum(products)

    value = int(total.numpy())

    with write_lock:
        C[row, col] = value
        done_mask[row, col] = True


def multiply_with_threads():
    frames = []
    jobs_done = 0
    total_jobs = N * N

    print(
        f"Multiplying two {N}x{N} matrices via TensorFlow across "
        f"{WORKER_THREADS} worker threads..."
    )

    start_time = time.time()

    with ThreadPoolExecutor(
        max_workers=WORKER_THREADS
    ) as pool:

        futures = [
            pool.submit(compute_cell, r, c)
            for r in range(N)
            for c in range(N)
        ]

        for _ in as_completed(futures):
            jobs_done += 1

            if (
                jobs_done % SNAPSHOT_EVERY == 0
                or jobs_done == total_jobs
            ):
                with write_lock:
                    snapshot = np.where(
                        done_mask,
                        C.astype(float),
                        np.nan
                    )

                frames.append(snapshot)

    elapsed = time.time() - start_time

    print(
        f"Done. {total_jobs} cells "
        f"({total_jobs * N} scalar multiplications) "
        f"finished in {elapsed:.2f}s "
        f"using {WORKER_THREADS} threads."
    )

    return frames, elapsed


def render_animation(
    frames,
    out_path="tf_matrix_multiply.gif"
):
    fig, ax = plt.subplots(figsize=(6, 6))

    ax.set_title(
        "Threaded 100x100 Matrix Multiplication (TensorFlow)"
    )

    ax.set_xticks([])
    ax.set_yticks([])

    vmax = np.nanmax(frames[-1])

    img = ax.imshow(
        frames[0],
        cmap="viridis",
        vmin=0,
        vmax=vmax
    )

    def update(i):
        img.set_data(frames[i])

        ax.set_xlabel(
            f"cells completed: "
            f"{min((i + 1) * SNAPSHOT_EVERY, N * N)} "
            f"/ {N * N}"
        )

        return [img]

    anim = animation.FuncAnimation(
        fig,
        update,
        frames=len(frames),
        interval=40,
        blit=False
    )

    anim.save(
        out_path,
        writer=animation.PillowWriter(fps=25)
    )

    plt.close(fig)

    print(f"Saved animation to {out_path}")


if __name__ == "__main__":
    frames, elapsed = multiply_with_threads()

    render_animation(frames)

    expected = tf.linalg.matmul(A, B).numpy()

    assert np.array_equal(
        C,
        expected
    ), "Mismatch! Threaded result is wrong."

    print(
        "Verified: threaded result matches "
        "tf.linalg.matmul exactly."
    )
```

## Run

```bash
python matrix_threading.py
```

## Expected Output

```text
Multiplying two 100x100 matrices via TensorFlow across 32 worker threads...
Done. 10000 cells (1000000 scalar multiplications) finished in X.XXs using 32 threads.
Saved animation to tf_matrix_multiply.gif
Verified: threaded result matches tf.linalg.matmul exactly.
```

The program generates:

```text
tf_matrix_multiply.gif
```

---

# 3. Threaded Matrix Laboratory

## Description

Threaded Matrix Laboratory is a browser-based matrix multiplication visualization.

It uses JavaScript Web Workers to perform matrix calculations using multiple background workers.

The application supports matrix sizes from 2×2 to 100×100.

Users can generate new matrices, start the calculation, observe worker contributions, and view the output matrix.

## Concepts Used

* JavaScript
* HTML5
* CSS3
* Web Workers
* Parallel processing
* Matrix multiplication
* Worker communication
* DOM manipulation
* Execution time measurement

## Code

Save as `index.html`.

```html
<!DOCTYPE html>
<html lang="en">

<head>

<meta charset="UTF-8">

<title>Threaded Matrix Laboratory</title>

<style>

:root{
  --bg:#eef1ee;
  --panel:#f7f8f6;
  --text:#333;
  --border:#ccc;
  --btn:#3a4750;
  --btn-text:#fff;
  --muted:#777;
  --cell:#fff;
  --accent:#4a7fb5;
}

@media (prefers-color-scheme: dark){

  :root:not([data-theme="light"]){

    --bg:#1c1e1c;
    --panel:#26282a;
    --text:#eee;
    --border:#444;
    --btn:#7fb2c9;
    --btn-text:#0d0f10;
    --muted:#aaa;
    --cell:#333a3f;
    --accent:#7fb2c9;

  }

}

:root[data-theme="dark"]{

  --bg:#1c1e1c;
  --panel:#26282a;
  --text:#eee;
  --border:#444;
  --btn:#7fb2c9;
  --btn-text:#0d0f10;
  --muted:#aaa;
  --cell:#333a3f;
  --accent:#7fb2c9;

}

body{

  background:var(--bg);
  color:var(--text);
  font-family:'Segoe UI', sans-serif;
  text-align:center;
  padding:30px 16px;

}

h1{
  margin-bottom:4px;
  font-size:1.8rem;
}

.sub{
  color:var(--muted);
  font-size:0.95rem;
  margin-bottom:24px;
}

.controls{

  display:flex;
  gap:10px;
  justify-content:center;
  flex-wrap:wrap;
  align-items:center;
  margin-bottom:24px;

}

.controls input[type=number]{

  width:70px;
  padding:6px;
  border-radius:8px;
  border:1px solid var(--border);
  background:var(--panel);
  color:var(--text);

}

button{

  padding:8px 18px;
  border:none;
  border-radius:20px;
  background:var(--btn);
  color:var(--btn-text);
  cursor:pointer;
  font-size:0.95rem;

}

button:disabled{

  opacity:0.5;
  cursor:default;

}

.stage{

  display:flex;
  justify-content:center;
  gap:16px;
  flex-wrap:wrap;
  align-items:center;

}

.panel{

  background:var(--panel);
  border-radius:14px;
  box-shadow:0 2px 10px rgba(0,0,0,0.12);
  padding:18px;

}

.panel h3{

  margin:0 0 12px 0;
  font-size:1.05rem;
  letter-spacing:0.02em;

}

.grid{

  display:grid;
  gap:5px;
  justify-content:center;

}

.cell{

  background:var(--cell);
  border:1px solid var(--border);
  border-radius:6px;
  display:flex;
  align-items:center;
  justify-content:center;
  font-size:0.85rem;
  font-variant-numeric:tabular-nums;
  transition:background 0.25s ease, transform 0.15s ease;

}

.cell.pop{
  transform:scale(1.12);
}

.op{

  font-size:1.8rem;
  color:var(--muted);
  padding:0 4px;

}

#statusMain{

  margin-top:26px;
  font-size:1rem;

}

#statusWorker{

  margin-top:8px;
  font-family:'Consolas','Courier New',monospace;
  font-size:0.9rem;
  color:var(--accent);
  background:var(--panel);
  display:inline-block;
```
