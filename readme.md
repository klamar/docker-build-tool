
Usage in Dockerfile

    curl https://raw.githubusercontent.com/klamar/docker-build-tool/master/dbt.py --output /usr/local/bin/dbt && chmod a+x /usr/local/bin/dbt

# Tools

Download

    dbt dl https://foo.bar.com/foo.sh foo.sh

## File Manipulation

Search/Replace

    dbt replace " foo " "-bar-" readme.md

## System Manipulation

Prepare Shell

    dbt prepare-shell
    
