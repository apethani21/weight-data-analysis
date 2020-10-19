# Weight data analysis

- Downloading weight data stored in a Google Sheet
- Storing the data in, and regularly updating a Postgres (originally SQLite3) database by checking the Google Sheet for updates, with a cron job.
- Originally regularly updated a Jupyter Notebook with a cron job, and then tried [Dash](https://plot.ly/dash/) and [Streamlit](https://www.streamlit.io/).

- `create.sql` initialises the `WEIGHT` table.
- `migration.py` performs a full migration of the data in the Google Sheet to the postgres database, avoiding duplication.
- `update_db.py` checks the number of rows in the database to figure out how many of the tail-end rows to add from the Google Sheet, and adds them.
- `api_handler.py` handles authentication for querying the Google sheet, and `postgres_utils.py` handles postgres authentication, connection and query execution.
- `weight-loss-analysis.ipynb` contains the analysis, which was then replicated with a Dash dashboard with `dashboarder.py` and a Streamlit dashboard with `streamer_app.py` 

<img src="screenshot.png" alt="dashboard" style="width:200px;"/>
