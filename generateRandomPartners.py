import random

students = [
    "Student One",
    "Student Two",
    "Student Three",
    "Student Four",
    "Student Five",
    "Student Six",
    "Student Seven",
]

def round_robin_pairs(number_of_students):
    schedule = []
    oddNumberOfStudents = number_of_students % 2 == 1

    if (oddNumberOfStudents):
        number_of_students += 1 # this creates a fictional student so groups can be formed in perfect pairs
    
    print(number_of_students)

    for i in range(1, number_of_students): # the number of possible pairings is one less than the number of students
        day_pairs = []
        for j in range(number_of_students // 2):
            # Pair the fixed student with one from the circle and others in the circle with each other
            first_student = (j + i) % (number_of_students - 1) + 2
            second_student = (number_of_students - 1 - j + i) % (number_of_students - 1) + 2
            if j == 0:  # Pair with the fixed student (student 1)
                first_student = 1
            day_pairs.append((first_student, second_student))

        # If the number of students is odd, add last student to random group
        if oddNumberOfStudents: 
            # find/store the group that contains the fictional student
            fictionalGroupIndex = find_index_of_pair_with_student(day_pairs, number_of_students)
            fictionalGroup = day_pairs[fictionalGroupIndex]
            # remove that group from day_pairs
            day_pairs.pop(fictionalGroupIndex)
            # find that fictional student's partner
            realStudentIndex = 0 if fictionalGroup[0] != number_of_students else 1
            realStudent = fictionalGroup[realStudentIndex]
            # add that partner to a random team
            randomTeam = random.randint(0,len(day_pairs) - 1)
            day_pairs[randomTeam] =(day_pairs[randomTeam][0], day_pairs[randomTeam][1], realStudent)

        schedule.append(day_pairs)
    return schedule

def find_index_of_pair_with_student(day_pairs, student_index):
    for index, pair in enumerate(day_pairs):
        if student_index in pair:
            return index
    return None

def get_student_name(studentIndex):
    return students[studentIndex - 1]

def format_pair(studentIndex, pair, column_width=30):
    dots = '.' * (column_width - len(get_student_name(studentIndex)))

    partnerIndices = [student for student in pair if student != studentIndex]
    groupString = get_student_name(partnerIndices[0])
    if(len(partnerIndices) > 1):
        groupString += ", " + get_student_name(partnerIndices[1])

    return f"{get_student_name(studentIndex)}{dots}{groupString}"

def save_daily_schedule_to_files(schedule, filename_prefix):
    for i, day in enumerate(schedule):
        daily_filename = f"{filename_prefix}_Day_{i+1}.txt"
        with open(daily_filename, 'w') as file:
            file.write(f"Partners Set #{i+1}:\n")
            for studentIndex in range(1,len(students)+1):
                # Find the student's partner for the day
                for pair in day:
                    if studentIndex in pair:  # Adjusting index as schedule starts from 1
                        # Identify the partner index in the pair
                        partnerIndex = pair[0] if pair[1] == studentIndex else pair[1]
                        # Adjusting partnerIndex to match students list index
                        partnerIndex -= 1
                        formatted_pair = format_pair(studentIndex, pair)
                        file.write(formatted_pair + '\n')
                        break
            file.write("\n")

schedule = round_robin_pairs(len(students))
print(schedule)
save_daily_schedule_to_files(schedule, './PartnerSets/PartnerSet')
