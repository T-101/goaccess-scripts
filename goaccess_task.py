import subprocess
import datetime

LOG_DIR = "/var/log/nginx/"
OUT_DIR = "/var/www/weblogs/"
SITES = ["example.com"]

if __name__ == "__main__":
    for site in SITES:
        outfile_name = f"{OUT_DIR}{site}.html"
        cmd = f"/usr/bin/zcat -f {LOG_DIR}{site}.access.log* | goaccess - -a -o {outfile_name} --html-report-title={site}"
        subprocess.run(cmd, shell=True)
        cmd = f"gzip -c {outfile_name} > {outfile_name}.gz && > {outfile_name}"
        subprocess.run(cmd, shell=True)
