# GUI_Software_Submission_2025
# **Thought process for the 1st question**:
The main idea behind my web application is that all the location, speed, battery levels, pod status, maintenance are all randomised. And they can **only** be changed when we reload the page. This was achieved using session_state. Eventhough the locations are "randomised" they are 7 different locations where the data of the location could be obtained (why this approach? the ans is that if the location is randomised and the weatherapi doesn't have any response for that place it would simply print out an error). 
There is a sidebar which has **GO To:**, **Sort By:**, **Filter By:** and a **Filter By(maintenance):**. The **Go To:** option lists all the places that we could go to ```Home, A_1, A_2, A_3, A_4, A_5```. The number of pods could also be changed with the help by changing the ```x``` value in the run.py file. I have kept it as 5 for simplicity sake.
The **Sort By** obviously givees us the sorted data according to the request.
The **Filter By** filter out the "Docked","Maintenance","Operational" pods.
The **Filter By (maintenance):** filters out the pods which have the maintenance as "None","Major","Minor".
In the individual pod page, there is a ```Real Time Data``` button which gives us the the real time data (it's obviously not realtime but the battery level decrases by 0.2 % every 8 seconds and the speed either increases or decreases by a factor of -2 or +1)
It also has weather api which would get weather data from the api
Also the api gets the temperature and recommends the suggested speed ie. if the temperature is below 1.7C
**NOTE:** Only run the command from the directory where the run.py is stored.
The pixel art shows the issue with the breaking system of the pod (highly unlikeely in real life).
The suggested speed also changes according to the weather description ie. if the weather description is "Rainy" then the suggested speed changes to some safer speed for the pod
**And that's it I hope you have a good time going thorugh my app**
```
Create a fork
Push your code in that repo
Finally create a pull request
```
## docs:

### https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request
