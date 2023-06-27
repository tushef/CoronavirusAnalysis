# Coronavirus Analysis
Conducting efficient basic analysis on the pandemic and visualizing the data using Plotly &amp; Dash

o Analysis on overall attributes of the pandemic in one country

o It fetches data from “Our World in Data” open source dataset in Git-Hub

o It uses Plotly and Dash to build interactive dashboards as shown in Jose Portillas Udemy course

o The CSV table is converted from a 20,000 rows x 36 columns dataframe (they usually add more
  over time) into a multi-index dataframe with about 200 rows (dates being studied) x 214 columns
  (states recorded) with another level of about 29 columns(total cases, new cases, total deaths, new
  deaths, total cases per million, population etc). The converting process takes about 4 to 5 minutes,
  then it is saved in a CSV file for later usage.

o The table makes all the analysis faster as it is easier to traverse the dataset by eliminating
  repetitions during iterations and using only a fixed amount of memory as it is the only dataframe
  the program needs, whereas with the other one, in order to compare x states we had to iterate
  through the entire table x times, in order to extract the information we needed, save it in another
  dataframe, so that it could interact properly with Plotly and Dash

o 1st graph is a simple line+dot graph showing the total cases and total deaths of a country

o The 2nd graphs are 2 histograms showcasing the new cases(blue) and new deaths(red) probability
distribution

o The 3rd graph is a simple box plot used to analyse the variance of the new cases and new deaths columns of the dataset

o The 4th graph is a simple stacked bar chart which analyses the development of new cases and deaths in a country through time

o The 5th graph is a bubble chart showcasing 4 features in one graph: total cases development through time, total cases per million through time via the size of the bubble and total deaths through time via the color of the bubble

o The 6 th graph is an entire map of the world showcasing total cases all around the world, however Plotly has problems in recognizing all the ISO codes, so it is still in works
