---
title: "Building an Oil & Gas Production Forecasting App with Python, SARIMAX, and Dash"
lastmod: 2023-02-21
date: 2023-02-21
draft: false
topics: ["data science", "analytics", "Georgia Tech", "oil and gas", "time series", "python"]
summary: "A hands-on group project experience in the Data and Visual Analytics course at Georgia Tech, where we built a forecasting application for oil & gas production using real-world data, SARIMAX models, and modern web technologies."
---

About three months ago, I finished one of the most exciting and hands-on courses in the Masters of Analytics at Georgia Tech. It is called "Data and Visual Analytics." The course covered a broad range of topics such as SQL, Big data, Cloud Computing, Javascript (D3 😓), Docker, some analytics topics, etc., in a single semester! However, the most interesting part of the course was the group project.

In this project, we had a well-defined objective: create a practical application that handles lots of real data, uses analytics, and applies good coding practices.

We decided to go for a project related to the oil & gas industry. Concretely, we agreed to create a simple application to **forecast the oil & gas production given a group of wells selected by the user**. You can find the GitHub repo here: [Energy-DVA/energy: Group project for Data and Visual Analytics at Georgia Tech](https://github.com/Energy-DVA/energy)

To summarize the story, here are some high-level challenges and solutions we found during this journey.

## Real dataset with lots of data

- We found the [Kansas Geological Survey](https://www.kgs.ku.edu/PRS/petroDB.html) dataset for Oil & Gas production. This dataset consists of semi-structured data (CSV, shapefiles, ASCII, etc.) of well locations, production, and geolocation data. It was the information we needed!

## Collaboration in software development

- It was time to start putting some code together. We set up a git repo in GitHub, but we wanted to be agile in collaborating with the code. In this case, there was no need to create a Kanban board with the tasks since we had only three: build the backend (or model in MVC), build the analytics model, and generate the frontend. Still, basic git knowledge was helpful for everyone to work on their branches and merge them into "development." After we had the first version of the working app, we would merge the dev -> main branch. This [article](https://nvie.com/posts/a-successful-git-branching-model/) helps get started with a branching model for collaboration.

## Data persistence

- Since this would be a web app, we couldn't just load all the information in memory when the user loaded the app. We decided to use **SQLite** to store the information on our computers. After we gathered the information we needed, we ended up with an SQLite file of 2 GB in 6 tables, 500k well records, and 8.8 million records of time series data until April 2022. We used sqlalchemy to create the DB schema and the queries for the app in case we needed to change the database in the future (PostgreSQL, MySQL, etc.)

## Simple Analytics Model for Time Series Forecasting

- Since our main objective was forecasting oil & gas production, we needed an analytics model that was easy and quick to train multiple times during the use of the application. We used a **Seasonal Auto-Regressive Integrated Moving Average with eXogenous factors** (SARIMAX) model. In this case, the exogenous variable was the number of wells. It proved to be very fast and reliable for short-term forecasts.

## Data Visualization

- In this course, we had to deal with D3; you guessed it, we didn't use it for our project, at least not directly. We had little time to deliver the project and needed to iterate quickly to test things out. As such, we wanted a library that provided a **Python** API and was flexible at the same time if we needed to add more complicated interaction to the app. We used **Dash**. It allowed us to create the frontend in a breeze, without using any javascript, although you need a bit of knowledge on the DOM.

## Create a maintainable codebase

- Ok, I must admit this wasn't required for the project, but we wanted to apply some basic software architecture concepts to make our life easier. We used MVC (Model-View-Controller) architecture to create the app, where database interaction and SARIMAX were in the model portion; the View was created using the Dash API and plotly, as well as the Controller, which were basically Dash callbacks. This [article](https://towardsdatascience.com/clean-architecture-for-ai-ml-applications-using-dash-and-plotly-with-docker-42a3eeba6233) helped us to set things up.

---

Ultimately, we put everything in place and created a nice web app. However, here are some things that we would've liked to complete:

- We tested the other time-series analytics methods but needed more time to test against decline curve analysis or analytical methods commonly used in the oil & gas industry.
- Instead of downloading the production data for offline use, it would've been nice to create a web scrapper to get the most up-to-date information from the KGS website.
- And, of course, the best user experience would've come from deploying the app in the cloud. We wanted to use **Docker** to make the process easier, but we had a deadline upon us (and it wasn't required for the project).

---

Last but not least, we finished this project in about four months of intermittent work between weeks, the last month being the most intensive. This would've been an impossible task without such a fantastic team. Thanks again to Efrain Rodriguez, Sheena Abraham, Nikhil (Nik) Kanoor, Jagath Jonnalagedda, and Geetak Ingle, P.Eng. for making this project possible. We had so much fun during this journey!!!

Here is a demo of the web app in action:

{{< youtube 24CmbDLP-_E >}}

You are welcome to fork the project and add your personal touch to the app.

{{< subscription >}}
