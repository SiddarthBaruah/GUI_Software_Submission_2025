Details on how to run the app:-
1)	Run the main.py file in python using the command “streamlit main.py”.
2)	Make sure u are connected to a good internet connection as weather api might not work if your network is bad or you are offline.
3)	First the route monitoring page will be opened as other pages are using live values from the route monitoring page(such as speed and battery). So if other pages are opened before they might show some error.

My learnings and thought process:-
At first as I knew only c/c++ programming languages , I spent two days for fully learning python in which I also learned how to request data from an api. After that, I started learning streamlit specific simple features like st.title , markdown etc. 

Then I started building my application with the first page being Route monitoring(which took more than half of my time). So I learned pydeck and how I can use it to make a live map on my site. I ran the code for one map and it worked really good. Then I thought of having 3 maps which run simultaneously and differently from each other. For this, I spent so much time and tried using threading(as I was using time.sleep function so I wanted every map runs independently) but then I got to know that streamlit is a single threaded environment which doesn’t support multiple threading. Then I got the idea of doing it iteratively but I dropped it for later as I spent a lot time on this before. 

So then I started learning the weather api. I made the application such that the weather api would take the live cursor’s coordinates regularly in certain time period and give the weather of that point at that time in real world. Then I would adjust the speed to 900 if it is cloudy and 700 it is rainy weather. 

Then I created the filter or comparisons page using the panda library in python and different features of streamlit. Then I created the maintenance page which would take random values from the random library and show when is maintenance needed for each pod.

At last, I again came to the same problem I dropped earlier.  I wrote the code to iteratively move all the maps together which again was a really painful task. Then I wanted to use the speed and battery which was changing in this page in other pages so I used session state feature of streamlit to maintain the data among all the pages. This also solved my problem that when I was switching from route monitoring page and coming back on it again, All the routes were starting from the beginning, so I used session state on the progress of the pods which helped me maintain their progress even after switching page(took a lot of tries for it work ☹).

Finally everything was completed and it felt really good learning a whole lot of new stuff which was really interesting to me.
