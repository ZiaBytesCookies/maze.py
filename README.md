# 🧩 Maze Generator & Solver (Python CLI)

This is a single-file Python script to generate and solve ASCII mazes right in your terminal. It supports animations, customizable size, seed control, pathfinding, and even text file export.

---

## Features

- 🧱 Maze generation using recursive backtracking (DFS)
- 🔍 Maze solving using breadth-first search (BFS)
- 🎞️ Optional animation in terminal
- 📝 Export maze to a `.txt` file
- 🧪 Built-in self-test for correctness
- 🔁 Fully command-line configurable

---

## Usage

```bash
python3 maze.py [OPTIONS]
```

### Options

| Flag            | Description                                      |
|-----------------|--------------------------------------------------|
| `--width`       | Maze width (default: 21)                         |
| `--height`      | Maze height (default: 11)                        |
| `--seed`        | Random seed for reproducibility                  |
| `--solve`       | Solve the maze after generation                  |
| `--animate`     | Animate carving and solving in terminal          |
| `--export FILE` | Export final maze to a text file                 |
| `--test`        | Run internal tests                               |

---

## Examples

Generate a 10×5 maze and solve it:
```bash
python3 maze.py --width 10 --height 5 --solve
```

Animate the process:
```bash
python3 maze.py --animate --solve
```

Export maze to a file:
```bash
python3 maze.py --width 30 --height 15 --export output.txt
```

Run self-tests:
```bash
python3 maze.py --test
```

---

## Output

The maze is displayed using ASCII characters:
- `█` = wall  
- `S` = start  
- `E` = end  
- `·` = solution path (if `--solve` used)

Example:
```
█████████████
█S·     █   █
█ █ █ █ █ █ █
█ █ █ █ █ █ █
█   █······E█
█████████████
```

---

## License

Free to use, modify, and share.  
Made with 🧠 and ❤️ in Python.
