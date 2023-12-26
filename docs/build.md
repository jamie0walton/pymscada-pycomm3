# Building a pymscada Extension
This module started out as a demonstration of how to add a busclient for
pymscada that carries out logical processes on tags. However to keep
pymscada purely focussed on tags value sharing and the Angular UI this
needed to be moved out.

## Create the Python module

- Create the github project ```pymscada-process```
  - Set the licence to GPL-3
  - Add a Python .gitignore
- ```git clone https://github.com/jamie0walton/pymscada-process.git```
- ```cd pymscada-process```
- ```pdm init```
  - /usr/bin/python3.11 (3.11) -- prompts for creating the venv
  - installable library -- yes
  - project name -- pymscada
  - version -- 0.0.1
  - description -- Shared tag value SCADA with python backup and Angular UI
  - pdm-backend
  - licence -- GPL-3.0-or-later
  - Author Name -- Jamie Walton
  - email -- jamie@walton.net.nz
  - python -- >=3.9  although I am setting up in 3.11. importlib choice
- ```pdm add -dG test pytest pytest-asyncio pytest-cov flake8 flake8-docstrings```
- ```pdm add pymscada pycomm3```
- ```pdm build```
- ```pdm publish```


