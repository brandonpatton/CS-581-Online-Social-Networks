#  Author: Brandon Patton
#  Assignment 09 - Analyze Social Network Data
#  This program analyzes a social network dataset and print	results to the terminal	window in both written/tabular and graphical form

#  To run in a terminal window:   py -3 Patton_Assign09.py OR python3 Patton_Assign09.py

import csv
import statistics as stats
import matplotlib.pyplot as plt

u_ids = []      #initialize empty variables for each column csv data
ages = []
dob_months = []
dob_years = []
genders = []
tenures = []
friendship_counts = []
num_friendships_initiated = []
likes = []
likes_received = []
mobile_likes = []
mobile_likes_received = []
www_likes = []
www_likes_received = []

with open('FB_data.csv', newline='') as csvfile:
    linereader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    count = 0
    for row in linereader:                          
        if(count == 0):                             #recognize header line
            count += 1
            continue
        userid, age, dob_month, dob_day, dob_year, gender, tenure, friendship_count, friendships_initiated, likes_, likes_received_, mobile_likes_, mobile_likes_received_, www_likes_, www_likes_received_ = row[0].split(',')
        
        u_ids.append(int(userid))                   #use int() to convert string integers to integer type
        ages.append(int(age))
        dob_months.append(int(dob_month))
        dob_years.append(int(dob_year))
        genders.append(gender)

        try:
            tenures.append(int(tenure))
        except: 
            tenures.append(0)

        friendship_counts.append(int(friendship_count))                 
        num_friendships_initiated.append(int(friendships_initiated))
        likes.append(int(likes_))
        likes_received.append(int(likes_received_))
        mobile_likes.append(int(mobile_likes_))
        mobile_likes_received.append(int(mobile_likes_received_))
        www_likes.append(int(www_likes_))
        www_likes_received.append(int(www_likes_received_))


''' Plot 1: Total Friendship Count vs. Total Initiated Friendships
    This plot compares the total amount of friendships to the total initiated friendships
    using a scatter plot.  The x coordinate for a given point is a user's total initiated friendships
    and the y coordinate for that same point is that same user's total friendship count.
'''
plot_1 = plt.figure(1)
plt.scatter(friendship_counts, num_friendships_initiated)
plt.xlabel("Total Friendship Count")
plt.ylabel("Total Initiated Friendships")
plt.suptitle("Total Friendship Count vs. Total Initiated Friendships")

print("\nMedian Total Friendship Count:\t\t", stats.median(friendship_counts))
print("Median Total Friendships Initiated:\t", stats.median(num_friendships_initiated))

''' Plot 2: Number of Days on Facebook vs. Total Friendship Count
    This plot compares the total amount of friendships to the total number of days on facebook
    using a scatter plot.  The x coordinate for a given point is a user's total number of days on facebook
    and the y coordinate for that same point is that same user's total friendship count.
'''
plot_2 = plt.figure(2)
plt.scatter(tenures, friendship_counts)
plt.xlabel("Number of Days on Facebook")
plt.ylabel("Total Friendship Count")
plt.suptitle("Number of Days on Facebook vs. Total Friendship Count")

print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
print("\nMedian Number of Days on Facebook:\t", stats.median(tenures))
print("Median Total Friendship Count:\t\t", stats.median(friendship_counts))

''' Plot 3: Friendship Count vs. Amount of Likes Received
    This plot compares the total amount of friendships to the total amount of likes received
    using a scatter plot.  The x coordinate for a given point is a user's total amount of friends
    and the y coordinate for that same point is that same user's amount of likes received.
'''
plot_3 = plt.figure(3)
plt.scatter(friendship_counts, likes_received)
plt.xlabel("Total Friendship Count")
plt.ylabel("Likes Received")
plt.suptitle("Total Friendship Count vs. Amount of Likes Received")

print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
print("\nMedian Total Friendship Count:\t\t", stats.median(friendship_counts))
print("Median Likes Received:\t\t\t", stats.median(likes_received))

''' Plot 4: Median Likes Received by Gender
    This plot is a barplot that displays the median likes received by a given gender.  
    The first bar represents the median likes received by Males
    The second bar represents the median likes received by Females
    The third bar represents the median likes received by those identifying with N/A.
'''
m_lr = []
f_lr = []
na_lr = []
count = 0

for g in genders:
    if(g == "male"):
        m_lr.append(likes_received[count])
    elif(g == "female"):
        f_lr.append(likes_received[count])
    else: 
        na_lr.append(likes_received[count])
    count = count + 1


m_median = stats.median(m_lr)
f_median = stats.median(f_lr)
na_median = stats.median(na_lr)

plot_4 = plt.figure(4)
plt.bar(['Males', 'Females', 'N/A'], [m_median, f_median, na_median])
plt.xlabel("Gender")
plt.ylabel("Likes Received")
plt.suptitle('Median Likes Received by Gender') 

print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
print("\nMedian Likes Received by Males:\t\t", m_median)
print("Median Likes Received by Females:\t", f_median)
print("Median Likes Received by Gender 'N/A':\t", na_median)

''' Plot 5: Median Number of Friends vs. Ages
    This plot uses a barplot that displays the median number of friends by ages.
    User ages are displayed at the x-axis of the graph while the median number of friends for that given age
    are displayed on the y-axis.
'''
count = 0
year_data = {}

for year in dob_years:
    age = 2013 - year
    if age in year_data:
        year_data[age] = year_data[age] + [friendship_counts[count]]
    else:
        year_data[age] = [friendship_counts[count]]
    count = count + 1

age_keys = []
age_results = []

for age in year_data:
    age_keys.append(age)
    age_results.append(stats.median(year_data[age]))

plot_5 = plt.figure(5)
plt.bar(age_keys, age_results)
plt.xlabel("User Age")
plt.ylabel("Median Number of Friends")
plt.suptitle("Median Number of Friends vs. Age")

print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
print("\nMedian User Age:\t\t\t", stats.median(age_keys))
print("Median Number of Friends:\t\t", stats.median(age_results))

''' Plot 6: Median Likes Received vs. Age
    This plot uses a barplot that displays the median number of likes by ages.
    User ages are displayed at the x-axis of the graph while the median number of likes for that given age
    are displayed on the y-axis.
'''
count = 0
year_likes = {}

for year in dob_years:
    age = 2013-year
    if age in year_likes:
        year_likes[age] = year_likes[age] + [likes_received[count]]
    else:
        year_likes[age] = [likes_received[count]]
    count += 1

age_likes_keys = []
age_likes_results = []

for age in year_likes:
    age_likes_keys.append(age)
    age_likes_results.append(stats.median(year_likes[age]))

plot_6 = plt.figure(6)
plt.bar(age_likes_keys, age_likes_results)
plt.xlabel("User Age")
plt.ylabel("Median Likes Received")
plt.suptitle("Median Likes Received vs. Age")

print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
print("\nMedian User Age:\t\t\t", stats.median(age_likes_keys))
print("Median Likes Received:\t\t\t", stats.median(age_likes_results))

plt.show()
