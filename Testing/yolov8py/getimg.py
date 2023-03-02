from roboflow import Roboflow
rf = Roboflow(api_key="5ioJqiehSyYoClJk3jEv")
project = rf.workspace("deanpop").project("flame-cuq1f")
dataset = project.version(2).download("yolov8")
