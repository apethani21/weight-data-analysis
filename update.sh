/home/ubuntu/anaconda3/envs/weight-loss-dev/bin/python -u update_db.py >> /home/ubuntu/logs/weight-db-update.log 2>&1;
/home/ubuntu/anaconda3/envs/weight-loss-dev/bin/jupyter nbconvert --to notebook --execute /home/ubuntu/repo/weight-data-analysis/weight-loss-analysis.ipynb >> /home/ubuntu/logs/weight-loss-analysis.log 2>&1;
mv /home/ubuntu/repo/weight-data-analysis/weight-loss-analysis.nbconvert.ipynb /home/ubuntu/repo/weight-data-analysis/weight-loss-analysis.ipynb;
