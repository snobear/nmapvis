# NmapVis

## About

NmapVis is a super simple web GUI for importing and displaying nmap scan results. This is my entry for the BF code challenge.

## Deploy

Build and run with Docker. From main directory:

```
docker build -t nmapvis .
docker run -d --name nmapvis -p 3000:3000 nmapvis
```

Then go to [http://localhost:3000/](http://localhost:3000/) in your browser.

## Usage

The UI *should* be intuitive, but if not:

- Click `Upload nmap scan results` button to import an nmap results xml file.
- Exit import modal and results will populate.
- Click an IP to filter results by specific IP.

## Assumptions

- Any results files uploaded will reflect the sample xml file provided, i.e. contain similar xml structure and fields. There is definitely some error checking in place, but I could have been much more rigorous in testing
a variety of xml files to put it through serious QA.

## Additional Comments and Notes

For the sake of brevity in this small project, I cut a few corners :). For a more robust production app, here are some things we should/could do:

- Use https
- Add authentication layer for server -> DB access
- User auth for web app, i.e. support multiple users and lock down dashboard if required
- Front end state management would be beneficial to put in place, e.g. Redux
- Pagination. Currently all results are recklessly grabbed from the DB and displayed on the web page
- Tests! Unit and integration testing is always a huge plus.
- Log rotation of app logs
- Store uploaded files in S3 or persistent storage. Compress and add lifecycle/retention rules.
- Scan all uploaded files prior to opening and parsing, e.g. with clamav.
- More attention to detail to DB schema, e.g. store IPs in binary format instead of chars for easier sorting.
- Use a battle-tested production web server like nginx+uwsgi instead of using flask to serve everything.cd ..

## Language Selection

#### REST API

Python is my fav and strongest language currently. If speed were the highest concern, I may have reached for Go or Rust for the backend.

#### Front-end

React is awesome. We could have a more robust SPA by introducing Redux as mentioned above, and using change feeds/streams from the DB to push updates to the app for a more real-time UI.
