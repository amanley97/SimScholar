# EAGER-Gem5-GUI
EAGER computer architecture learning tool utilizing Gem5

This branch is for development of an api based gui.
Place this directory in `configs/example/gem5_library/`

## Current functionality:

### Update December 7th 2023
Added support for fronted API requests
Run the gem5 server like previous update.
```python3 render-with-api.py```
Runs a local instance of the Graphical user interface.
Go to http://localhost:8000

### Update December 7th 2023
```gem5 render.py``` 
Generates an HTML file with data pulled from gem5.

```gem5 api/obtain_api.py``` 
Opens an HTTP Server on port 5000.
```
    curl http://localhost:5000/get_mem_types
    curl http://localhost:5000/get_cpu_types
```
These are the implemented requests so far.