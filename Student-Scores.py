# --------------------------- Requirements & Notes ---------------------------
"""
    Required:
        - Retrive student scores from provided site
        - Minimum 3 Summaries: file stats, career aspiration, & overall score
    Optional/Consider:
        - Encrypt/Decrypt the email
        - Graphs
        - Error Handling
        - Structure
        
    Additional Notes:
        - Save graphs as .png
        - Write summaries to .txt file
        - blocks of code are sectioned with commented Headers
    
    File Stats:
        - File size in bytes
        - Milliseconds to retrieve (elapsed time)
        - Number of records processed
        - Number of records with error
        - Time to process the file after download
    
"""

# --------------------------- Code ---------------------------
import json
import requests
import time
import matplotlib.pyplot as plt
from collections import Counter

summary_file = open('summary_file.txt','w')

# --------------------------------------------
# Computes File Stats 
# --------------------------------------------
start_time = time.time() 
response = requests.get("https://api.slingacademy.com/v1/sample-data/files/student-scores.json")
end_time = time.time()
download_time = (end_time - start_time) * 1000 
file_size = len(response.content)

if response.status_code == 200: # Success code
    start_processing = time.time()
    data = json.loads(response.text)
    end_processing = time.time() 
    process_time = (end_processing - start_processing) * 1000
    records_error = 0
    numb_records = len(data)   
else:
    records_error = response.status_code
    summary_file.write(f"Error Retrieving Data: {records_error}")

summary_file.write("_________ File Stats _________") 
summary_file.write(f"\nFile Size: {file_size} bytes")
summary_file.write(f"\nDownload Time: {round(download_time,3)} milliseconds")
summary_file.write(f"\nNumber of Records Processed: {numb_records}")
summary_file.write(f"\nNumber of Records Processed with error: {records_error}")
summary_file.write(f"\nProcess Time: {round(process_time,3)} milliseconds\n") 

# --------------------------------------------------------------------------------------------------------------------
# Finds the different career aspirations and corresponding count. Creates bar graph for visualization
# --------------------------------------------------------------------------------------------------------------------
aspirations = [career['career_aspiration'] for career in data]  # creates list of aspirations from JSON list
aspiration_counts = Counter(aspirations)
sorted_aspirations = sorted(aspiration_counts.items(), reverse = False)
aspirations, counts = zip(*sorted_aspirations)  # allows iteration over 2 lists simultaneously

summary_file.write("\n_________ Career Aspirations _________")
for aspiration, count in sorted_aspirations:
    summary_file.write(f"\n{aspiration}: {count} students")
summary_file.write("\n")

font1 = {'family':'serif','color':'blue','size':20}
font2 = {'family':'serif','color':'darkred','size':15}

plt.figure(figsize= (15,10))
plt.barh(aspirations, counts, height=0.5)
plt.xlabel('Number of Students', fontdict= font2)
plt.ylabel('Career', fontdict= font2)
plt.title('Student Career Aspirations', fontdict= font1)
plt.savefig("Career Aspirations Data.png")

#---------------------------------------------------------------------------------
# Function returns letter grade based on corresponding overall score. 
#---------------------------------------------------------------------------------
def grade(overall_score):
    if float(overall_score) >= 90 and float(overall_score) <= 100:
        return 'A'
    elif float(overall_score) >= 80 and float(overall_score) < 90:
        return 'B'
    elif float(overall_score) >= 70 and float(overall_score) <80:
        return 'C'
    elif float(overall_score) >= 60 and float(overall_score) < 70:
        return 'D'
    elif float(overall_score) < 60:
        return 'F'
a_count = 0
b_count = 0
c_count = 0
d_count = 0
f_count = 0

for i in data:
    math_score = i["math_score"]
    history_score= i["history_score"]
    physics_score = i["physics_score"]
    chemistry_score = i["chemistry_score"]
    biology_score = i["biology_score"]
    english_score = i["english_score"]
    geography_score = i["geography_score"]

    average_score = (math_score + history_score + physics_score + chemistry_score + biology_score + english_score + geography_score)/7
    overall_score = round(average_score,2)
    letter_grade = grade(overall_score)
    
    if letter_grade == 'A':
        a_count += 1
    elif letter_grade == 'B':
        b_count += 1
    elif letter_grade == 'C':
        c_count += 1
    elif letter_grade == 'D':
        d_count += 1
    else:
        f_count += 1

grades = ['A', 'B', 'C', 'D', 'F']
counts = [a_count, b_count, c_count, d_count, f_count] 

summary_file.write("\n_________ Overall Scores _________")
summary_file.write(f"\nNumber of A's: {a_count}")
summary_file.write(f"\nNumber of B's: {b_count}")
summary_file.write(f"\nNumber of C's: {c_count}")
summary_file.write(f"\nNumber of D's: {d_count}")
summary_file.write(f"\nNumber of F's: {f_count}\n")

plt.figure()
plt.bar(grades, counts)
for x, y in enumerate(counts):  # adds corresponding values to each bar
    plt.text(x, y, str(y), ha='center', va='bottom')
plt.xlabel("Grade")
plt.ylabel("Number of Students")
plt.title("Grade Distribution")
plt.savefig('Grade Distribution.png')

# ---------------------------------------------------------------------
# Function 2) Calculates individual subject's average across data. 
# ---------------------------------------------------------------------
def subject_avg_score(data, subject):
  total_score = 0
  for student in data:
    total_score += student[subject]
  average_score = total_score / len(data)
  return round(average_score,2)

math_avg = subject_avg_score(data, "math_score")
history_avg= subject_avg_score(data, "history_score")
physics_avg = subject_avg_score(data, "physics_score")
chemistry_avg = subject_avg_score(data, "chemistry_score")
biology_avg = subject_avg_score(data, "biology_score")
english_avg = subject_avg_score(data, "english_score")
geography_avg = subject_avg_score(data, "geography_score") 

summary_file.write("\n_________ Individual Subject Averages _________")
summary_file.write(f"\nMath: {math_avg}%")
summary_file.write(f"\nHistory: {history_avg}%")
summary_file.write(f"\nPhysics: {physics_avg}%")
summary_file.write(f"\nChemistry: {chemistry_avg}%")
summary_file.write(f"\nBiology: {biology_avg}%")
summary_file.write(f"\nEnglish: {english_avg}%")
summary_file.write(f"\nGeography: {geography_avg}%\n")

# ----------------------------------------------------------------------
# Function 3) Create Pie Charts for visualization
# ----------------------------------------------------------------------
def pie_chart(data, labels, title):
    plt.figure()
    plt.pie(data, labels = labels, autopct='%1.1f%%')
    plt.title(title)
    plt.savefig(f'{title}.png')

# Determines how many students have a part-time job
part_time_jobs = sum(jobs['part_time_job'] for jobs in data)
percent_jobs = (part_time_jobs/numb_records) * 100
no_job = numb_records - part_time_jobs
job_labels = ['Has Part-Time Job', 'No Part-Time Job']
job_sizes = [part_time_jobs, no_job]
pie_chart(job_sizes, job_labels, 'Part-Time Job Data')

summary_file.write("\n_________ Part Time Jobs _________") 
summary_file.write(f"\nOut of {numb_records} students, {part_time_jobs} or {percent_jobs}% have part-time jobs.\n")

# Determine how many students participate in extracurricular activities
ec_activities = sum(activities['extracurricular_activities'] for activities in data) 
percent_active = (ec_activities/numb_records) * 100
no_activities = numb_records - ec_activities
ec_labels = ['Participates in Activities', 'No Participation']
ec_sizes = [ec_activities, no_activities]
pie_chart(ec_sizes, ec_labels, 'Extracurricular Activities Data')

summary_file.write("\n_________ Extracurricular Activities _________") 
summary_file.write(f"\n{ec_activities} or {percent_active}% students participate in extracurricular activities.")

summary_file.close()