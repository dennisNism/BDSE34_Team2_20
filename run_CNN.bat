@echo off

for %%s in (Finance Technology) do (
  for %%c in (0 1 2 3 4) do (
    python ./src/CNN.py --sector %%s --clusterID %%c
  )
)