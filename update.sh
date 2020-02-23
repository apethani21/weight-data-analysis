/home/pi/miniconda3/bin/python -u update_db.py >> /home/pi/logs/weight-db-update.log 2>&1;
/home/pi/miniconda3/bin/jupyter nbconvert --to notebook --execute /home/pi/repo/weight-data-analysis/weight-loss-analysis.ipynb >> /home/pi/logs/weight-loss-analysis.log 2>&1;
mv /home/pi/repo/weight-data-analysis/weight-loss-analysis.nbconvert.ipynb /home/pi/repo/weight-data-analysis/weight-loss-analysis.ipynb;
