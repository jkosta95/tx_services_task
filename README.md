infostud - Scrapy project that crawls https://poslovi.infostud.com/
Crawler extracts the following data from the job ad:
    ·      Job title
    ·      Employer name
    ·      Job address
    ·      Job details
    ·      Publishing date

infostud_app  - Flask application that returns job ads from mongo database. 

Required APIs are:
    ·      Get all job post.
    ·      Get job post per city.
    ·      Get job post per employer.
