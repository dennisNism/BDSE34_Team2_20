@echo off

for %%s in (Finance Technology) do (
  for %%c in (0 1 2 3 4) do (
    python ./src/GRU_prediction.py --sector %%s --clusterID %%c
  )
)