The domain of our database is highly related to “European Soccer”, containing core tables like “Players, Teams, Leagues, Matches” and secondary tables like “Stadium, Injury, etc”. When designing the E-R model, we endow detailed attributes including several highly related entities, such as Player Attributes, Team Attributes, Country Injuries and Stadium, etc.

# Data Extraction:
The main dataset named “European Soccer Database” we use in our project is from https://www.kaggle.com/hugomathien/soccer, which includes 25k+ matches, players & teams attributes for European Professional Football. Besides, we integrate several external datasets such as ”soccer-players-injuries” showing history per player in european soccer league from https://www.kaggle.com/eliesemmel/soccerplayersinjuries, and “Football (Soccer) Stadiums” listing football (soccer) stadiums all across the world with their capacity and other informations from https://data.world/johayes13/football-soccer-stadiums. What’s more, we apply players and teams attributes from EA Sports FIFA games, which helps us analyze, evaluate a player or a team’s ability. This will mean a lot to finish our task: player ranking, team ranking and match outcome prediction. Different datasets from different data sources have different id to quote their objects, therefore, we develop several methods to join them into our final dataset. For example, to combine the Injury Dataset and Player relation from European Soccer Database, we based on player name and date of birth to make sure two tuples are pointing to the same player. We also perform data cleaning to remove null values in our table, since those null values will influence the final prediction results. Those redundant and irrelevant attributes are removed from tables. And we also achieve data normalization: an example is we split a tuble to several tuples since one player can have more than one injury record. The final dataset is composed of Player_Attributes, Player, Match, League, Country, Team, Team_Attributes, Stadium and Injury.

# Software Platform:
Instead of MySQL, we decided to use Sqlite and Python with its rich packages. The reason we give up on MySQL is its restrictions and difficulties to perform data mining. Compared with MySQL, Sqlite is much less-weight and can be executed by Python directly due to the convenience of using built-in databases in Python and the similar SQL syntax. Using Sqlite in Python can bring more flexibility of using different useful functions and packages. For example, we have the chance to use sklearn to import machine learning models, seaborn & matplotlib to plot figures and perform data visualization, pandas to deal with complicated table operations as well as flask to build complex and beautiful web interfaces.

# User Guide:
All codes are commented in detail. Once the user installed all needed packages and datasets, the code can be executed smoothly. There are mainly two code files to achieve two separate tasks: The first one is sql_data_mining.ipynb, which mainly performs data loading, data processing, database construction, sql queries, data visualization and data mining.  

The second code file is user_interface.py, which performs data loading and builds our beautiful user interface to connect databases with users. We mainly used “Flask” inside Python to build the advanced GUI to complete multiple interactions between users and our databases.

# Major/Minor Areas of Specialization:
(1) Data Analysis and Data Mining:  
We choose our first focus area to be data mining since it is one of the most popular topics nowadays. With our integrated soccer dataset, we measured the weighted ability of a player, a team and a league, as well as rank them in descending order. We also make match outcome prediction by taking advantage of several machine learning models including Logistic Regression, KNN Classifier, Random Forest Classifier, AdaBoost Classifier and Gaussian Naive Bayes Classifier. There are more than 30 features as data input, and we also perform Principal Components Analysis (PCA) to select more important features. We also compare our model with predictions made by betting odds, and our results turn out to give better accuracy.  

<img src="https://github.com/HaojieChu/Analyzing_Soccer_Database_SQL_WebUI/blob/main/images/clubs.png"/>

<img src="https://github.com/HaojieChu/Analyzing_Soccer_Database_SQL_WebUI/blob/main/images/models.png"/>

(2) Advanced GUI form interface:  
Our second focus area is realizing advanced GUI form interfaces. We implemented a beautiful GUI to realize a series of interesting interactions
with users, completing the queries related to soccer. Users will be first verified via their identification. Official staff have the right to make different modifications, “Insertion, Updation, Deletion”, of the match records, while unofficial staff can only have the right to view the related information of different tables like a certain Player or a certain Team, etc. All tables used here are under-processed instead of raw data downloaded from resources. In the end, users can also view the prediction result of a match between two teams or a combat between two players by inputting two objects’ names. The whole UI is based on Flask which is a light-weight micro web framework, making the UI website beautiful and fast-response.

<img src="https://github.com/HaojieChu/Analyzing_Soccer_Database_SQL_WebUI/blob/main/images/screen.png"/>

## Contact the Author  

If you got any enquiries or suggestions, I'm all ears :sunglasses:  

- **Institution:**  University of Malaya  :mortar_board: Data Science Graduate  
- **Author** Haojie Chu
- **Academic E-mail:** hjchuyu5@gmail.com
