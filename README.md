# 2023 Robot

## Deploy code to robot

## Install RobotPy on Robot (periodically)

### upgrade robotpy locally on each laptop

```
py -3 -m pip install -U robotpy[all]
```

### Upgrade robotpy on the robot only on one laptop:

Installing python (only needs to be done after reimaging)

```
py -3 -m robotpy_installer download-python
py -3 -m robotpy_installer install-python
```

Upgrading RobotPy packages (periodically)

```
py -3 -m robotpy_installer download robotpy[all]
py -3 -m robotpy_installer install robotpy[all]
```


## Useful command line things

```
dir
```
```py -3 robot.py sim

```
```
py -3 robot.py deploy

```
