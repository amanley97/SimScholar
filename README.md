# EAGER-Gem5-GUI
EAGER computer architecture learning tool utilizing Gem5

This branch is for development of an api based gui.
Place this directory in `configs/example/gem5_library/`

### Current functionality:
```gem5 render.py``` 
Generates an HTML file with data pulled from gem5.

```gem5 api/obtain_api.py``` 
Opens an HTTP Server on port 8000.
```
    curl http://localhost:8000/get_mem_types
    curl http://localhost:8000/get_cpu_types
```
These are the implemented requests so far.