# Bollywood-Movie-Data-Extraction-from-Wikipedia
Extracted Bollywood movie data since the beginning of Bollywood industry till 2020-21.

This python script file will help you to extract movie data from wikipedia and store it into csv file.
It extracts data such as
<ul>
  <li>Release Year</li>
  <li>Title of movie</li>
  <li>Cast</li>
  <li>Director</li>
  <li>Genre (if there is)</li>
</ul>

I wrote this script to extract data in order to create a Bollywood Movie Recommender System. You can check out it's demo from <a href = "https://bollywoodrecommendation-system.herokuapp.com/">here</a>
## Script Details

<ol>
  <li>It stores all data into JSON format, and seperate json file for Genre, Directors, and Actors for Recommender System</li>
  <li>fetch_link_pages is function of a py script file which extracts base link of wikipedia page and then extract all year wise links for Bollywood movies from WikiPedia</li>
  <li>Then it extracts table data and then for each table we iterate to extract data.</li>
  <li>Since format of WikiPedia is changed time to time, I have used conditional statement to ease up extractions</li>
  <li>Created few lists of words and keywords which we are going to ignore while extracting</li>
  <li>Other than those lists data, every detail is maped with respective header and store into json file and into DataFrame</li>
  <li>As a final step it stores all the data into  csv file</li>
</ol>
