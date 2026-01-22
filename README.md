# Simple log minotoring script

## What does this script do
- Reads linux auth logs (for now from test file)
- Detects failed SSH auth attemps
- Distinguishs between:
    - invalid user attepms
    - valid user with wrong password
- Tracks failed attemps by:
    - Ip address 
    - Port 
    - Username used
    - Time window 
- Detect suspicuious activity based on repeated failures in short time with my own algoritm

## Why this project exists
- To understand how does linux auth logs looks and works
- To practice python regex and parsing
- To learn basic log detection

## Program stracture
- `controller.py` - is main file with logic and algoritm
- `test_log.txt` - file with test logs copied from real ssh failed auth

## ToDo
- Create a check function wich will detect if it is a cybr attach or just scared employe
- Replace prints with my own logs
- Implement it to CLI like a package u can use
- Finally replace the `test_log.txt` with real log adress

## Try it your self

### Dependencies
- python 3.6+
- yaml

### 1. Clone repository 
```bash
git clone https://github.com/Habybyi/basic_log_monitor.git
cd basic_log_monitor
```
### 2. Make sure to have the file with logs
```bash
cat test_log.txt
```
### 3. Start the program
```bash
python3 controller.py
```
