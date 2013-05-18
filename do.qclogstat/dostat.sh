python qcmerger.py -match 20130505 hublog.cfg hug.qc.20130505 
python qcmerger.py -match 20130505 hublog.local.cfg hug2.qc.20130505 

python qcmerger.py -stat hug2.qc.20130505.YSM > stat.YSM 
python qcmerger.py -stat hug2.qc.20130505.GRH > stat.GRH 
python qcmerger.py -stat hug2.qc.20130505.GVH > stat.GVH 
python qcmerger.py -stat hug2.qc.20130505.GLH > stat.GLH
