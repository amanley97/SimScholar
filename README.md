# EAGER-Gem5-GUI
EAGER computer architecture learning tool utilizing Gem5

This branch is for development of an api based gui.
Place this directory in `configs/example/gem5_library/`

## Current functionality:

### Update January 25th 2024
Rebuit frontend using python
Use ```python3 frontend/frontend.py``` to run the frontend. NOTE: Frontend will error without backend server.

Backend remains the same, but now has a shutdown function.
Use ```gem5 api/obtain_api.py```

Also added a single script to setup both front and backend.
Use ```bash run.sh```

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