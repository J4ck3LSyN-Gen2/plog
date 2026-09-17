# synlog

_Version_:`1.1.0`  
_Author_:`J4ck3LSyN`  
_Source_: [synlog](https://www.github.com/J4ck3LSyN-Gen2/synlog)

---

**Pretty colored Python logger with in-memory record buffering and JSON export.**

A lightweight, dependency-free logging utility that wraps the standard library `logging` module with:

- Colored terminal output (automatically disabled when not in a TTY)
- Convenient level shortcuts (`d`, `i`, `w`, `r`, `c` or `0`–`4`)
- Visual prefixes (`[*]`, `[!]`, `[-]`, `[CRIT]`)
- In-memory log buffer
- Easy JSON dump / pretty-print helpers

---

## Installation

```bash
pip install synlog
```

Or install from source:

```bash
pip install .
```

---

## Quick Start

```python
from synlog import synlog
log = synlog("myapp")
log.log("Application started")                 # INFO  -> [*]
log.log("Something looks suspicious", lvl=2)   # WARNING -> [!]
log.log("Failed to connect", lvl=3)            # ERROR -> [-]
log.log("Critical failure", lvl="c")           # CRITICAL -> [CRIT]
```

Example output (in a color-capable terminal):

```
14:32:11 INFO     myapp [*] Application started
14:32:11 WARNING  myapp [!] Something looks suspicious
14:32:11 ERROR    myapp [-] Failed to connect
14:32:11 CRITICAL myapp [CRIT] Critical failure
```

---

## Features

### Level Mapping

| Shortcut | Integer | Level      | Prefix  |
|----------|---------|------------|---------|
| `d`      | `0`     | DEBUG      | (none)  |
| `i`      | `1`     | INFO       | `[*]`   |
| `w`      | `2`     | WARNING    | `[!]`   |
| `r`      | `3`     | ERROR      | `[-]`   |
| `c`      | `4`     | CRITICAL   | `[CRIT]`|

You can pass either the letter or the number:

```python
log.log("debug info", lvl="d")
log.log("warning", lvl=2)
```

referece: `synlog.LMAP` & `synlog.PMAP`

### Verbosity Control

```python
log.verbosity = False   # suppress console output
log.verbosity = True    # re-enable
```

### In-Memory Buffer

Every log message is automatically stored:

```python
print(log.count())          # number of stored records

record = log.isingle(0)     # get a single record by index
records = log.irange(5)     # first 5 records
records = log.irange("...") # all records
records = log.irange("..")  # first half
records = log.irange(".")   # first 3 (or less)
```

### Export Logs

```python
# Dump all records to a JSON file
log.dump("logs.json")

# Dump and clear the buffer
log.dump("logs.json", clear=True)

# Just get the list of records
records = log.dump()
```

### Pretty-print Dictionaries

```python
data = {
    "user": "alice",
    "status": 200,
    "path": Path("/tmp/file.txt")
}
log.dumps(data)          # pretty-prints as indented JSON lines
```

---

## API Reference

### `synlog(name, verbosity=True, llvl=logging.DEBUG)`

| Parameter   | Type     | Default          | Description                     |
|-------------|----------|------------------|---------------------------------|
| `name`      | `str`    | required         | Logger name                     |
| `verbosity` | `bool`   | `True`           | Show messages on console        |
| `llvl`      | `int`    | `logging.DEBUG`  | Minimum level for the logger    |

### Methods

| Method                          | Description                                      |
|---------------------------------|--------------------------------------------------|
| `log(msg, lvl=1, ...)`          | Log a message                                    |
| `dump(fp=None, clear=False)`    | Export buffer to JSON file or return the list    |
| `dumps(data, indent=2)`         | Pretty-print a dict as JSON log lines            |
| `count()`                       | Number of stored records                         |
| `isingle(idx)`                  | Get one record by index                          |
| `irange(max, min=0)`            | Get a range of records                           |
| `verbosity` (property)          | Enable / disable console output                  |

---

## License

MIT
