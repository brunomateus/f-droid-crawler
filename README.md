# F-drod-crawler
Scrappy crawler to get information about apps from the F-droid repository 

## We provide two ways, two crawlers, to get the links of F-droid application

### one_app.py

To use this crawler you need to provide a file that contains a list of app's package. 
This crawler navigates through the file and for each package, it tries to visit the app's
page on F-droid and get every link for every available versions of the correspondent app.

How to use - command line sample:

```
scrapy crawl one_app  -a package_list_file=/Users/user/dataset.txt -o /Users/user/apps.json -t json
```

Input file sample:

```
acr.browser.lightning
at.bitfire.davdroid
at.bitfire.icsdroid
ca.rmen.android.frenchcalendar
ca.rmen.android.poetassistant
com.commit451.gitlab
com.jmstudios.redmoon
com.mrbimc.selinux
com.rubenwardy.minetestmodmanager
com.zeapo.pwdstore
```
### apps.py

This crawler navigates through the whole F-droid repository. It starts on the [browse link](https://f-droid.org/en/packages/)
and it goes through every page, visiting each app page and for every page,  it visits the tech info link and it gets
all links from the all available app version.

How to use - command line:

```
 scrapy crawl apps -o all_apps_12_05_2018-t.json -t json
```

### Results
For every call to our crawler it returns a json file contaning informations for every app visited by it.
The json contains a array, where every node is an application. 

```javascript
[
    {   
        "name": "Activity Launcher", 
        "summary": "Create shortcuts for apps and activities", 
        "last_version_name": "1.6.1", 
        "last_version_number": "10", 
        "last_added_on": "2017-04-17", 
        "last_download_url": "https://f-droid.org/repo/de.szalkowski.activitylauncher_10.apk", 
        "source_repo": "https://github.com/butzist/ActivityLauncher", 
        "versions": [
            {
                "name": "1.6.1", "code": "10", 
                "download_url": "https://f-droid.org/repo/de.szalkowski.activitylauncher_10.apk", 
                "added_on": "2017-04-17"
            }
         ], 
         "number_of_versions": 2
    },
    {
        "name": "Acrylic Paint", 
        "summary": "Simple finger painting", 
        "last_version_name": "2.2.1", 
        "last_version_number": "16", 
        "last_added_on": "2017-09-11", 
        "last_download_url": "https://f-droid.org/repo/anupam.acrylic_16.apk", 
        "source_repo": "https://github.com/valerio-bozzolan/AcrylicPaint", 
        "versions": [
            {
                "name": "2.2.1", 
                "code": "16", 
                "download_url": "https://f-droid.org/repo/anupam.acrylic_16.apk", 
                "added_on": "2017-09-11"
            }, 
            {
                "name": "2.2.0", 
                "code": "15", 
                "download_url": "https://f-droid.org/repo/anupam.acrylic_15.apk", 
                "added_on": "2016-10-11"
           }, 
           {
               "name": "2.1.4", 
               "code": "14", 
               "download_url": "https://f-droid.org/repo/anupam.acrylic_14.apk", 
               "added_on": "2016-02-19"
           }, 
           {
               "name": "2.1.3", "code": "13", 
               "download_url": "https://f-droid.org/archive/anupam.acrylic_13.apk"
           }, 
           {
               "name": "2.1", 
               "code": "11", 
               "download_url": "https://f-droid.org/archive/anupam.acrylic_11.apk"
           }, 
           {
               "name": "1.3.1", 
               "code": "7", 
               "download_url": "https://f-droid.org/archive/anupam.acrylic_7.apk"
           }, 
           {
               "name": "1.2.4", 
               "code": "4", 
               "download_url": "https://f-droid.org/archive/anupam.acrylic_4.apk"
           }, 
           {
               "name": "1.2.0", 
               "code": "3", 
               "download_url": "https://f-droid.org/archive/anupam.acrylic_3.apk"
           }
        ], 
        "number_of_versions": 8
   },
   ...
```
