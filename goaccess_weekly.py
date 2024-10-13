import os
import subprocess
import datetime

LOG_DIR = "/var/log/nginx/"
OUT_DIR = "/var/www/weblogs/"
SITES = ["example.com"]

def date_pattern(now):
    dates = []
    for i in range(7):
        dates.append((now - datetime.timedelta(days=i + 1)).strftime('%d/%b/%Y'))
    return "\|".join(dates)

if __name__ == "__main__":
    now = datetime.datetime.now()
    date_start = (now - datetime.timedelta(days=7)).strftime('%Y%m%d')
    date_end = (now - datetime.timedelta(days=1)).strftime('%Y%m%d')
    os.makedirs(f"{OUT_DIR}{now.strftime('%Y')}", exist_ok=True)
    for site in SITES:
        week_ago = now - datetime.timedelta(weeks=1)
        outfile_name = f"{OUT_DIR}{week_ago.strftime('%Y')}/{week_ago.strftime('%Y-%W')}-[{date_start}-{date_end}]-{site}.html"
        cmd = f"zcat -f {LOG_DIR}{site}.access.log* | grep '{date_pattern(now)}' | goaccess - -a -o {outfile_name} --html-report-title={site} --log-format COMBINED"
        subprocess.run(cmd, shell=True)
        cmd = f"gzip -c {outfile_name} > {outfile_name}.gz && > {outfile_name}"
        subprocess.run(cmd, shell=True)
