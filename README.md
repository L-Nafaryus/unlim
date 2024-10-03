# test tasks

## Running

- Nix related development environment:

```sh
nix develop 
```

- PDM related development environment:

```sh
pdm install
pdm run python -m task_two Catwoman Tokyo Radio
# or
eval $(pdm venv activate)
python -m task_one "[(datetime(2020, 1, 1), datetime(2020, 1, 7)),(datetime(2020, 1, 15), datetime(2020, 2, ))]"
```


