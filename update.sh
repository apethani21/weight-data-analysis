printf "running update_db.py\n"
/home/ubuntu/anaconda3/envs/weight-loss-dev/bin/python -u update_db.py >> /home/ubuntu/logs/weight-db-update.log 2>&1;
printf "successfully updated database\n";
printf "executing weight-loss-analysis.ipynb..\n";
/home/ubuntu/anaconda3/envs/weight-loss-dev/bin/jupyter nbconvert \
    --to notebook \
    --execute \
    /home/ubuntu/repo/weight-data-analysis/weight-loss-analysis.ipynb >> \
    /home/ubuntu/logs/weight-loss-analysis.log 2>&1 && \
    printf "successfully executed weight-loss-analysis.ipynb\n" && \
    mv /home/ubuntu/repo/weight-data-analysis/weight-loss-analysis.nbconvert.ipynb \
    /home/ubuntu/repo/weight-data-analysis/weight-loss-analysis.ipynb && \
    printf "weight-loss-analysis.ipynb updated\n";
