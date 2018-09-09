#!/usr/bin/python3

import validate
import wave_generator



years = [2018,2019,2020,2021,2022,2023,2024,2025]
marks = []
ymap = []
for y in years:
    temp = wave_generator.generate_markers(y)
    marks.extend(temp)
    for i in range(len(temp)):
        ymap.append(y)
    
print(marks[0])
print(marks[1])
print(marks[2])
print(marks[3])
print(marks[4])
exit()

print(len(marks))
vald = validate.val(marks)
print(len(vald))
filt = [(marks[i],ymap[i]) for i in range(len(marks)) if vald[i]]
print(len(filt))
print(filt[0])

f = open("generated_locs.csv", "w")
for pnt in filt:
    f.write("%d,,,,,,%f,%f\n" % (pnt[1], pnt[0][0], pnt[0][1]))

f.close()
