from re import M
from flask import Flask, render_template

app=Flask(__name__)
force=[]
torque=[]
cs=[]
rs=[]
print("THIS RUNS")

from pyfiles.cluster_details import compressed
from pyfiles import routes
from pyfiles import rul

routes.execute(cs,rs)
