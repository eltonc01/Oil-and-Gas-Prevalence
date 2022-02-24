from openpyxl import load_workbook

import geopy.distance

wb = load_workbook('fracking wells.xlsx')
sheet = wb.active
lat_input = input('Latitude: ')
long_input = input('Longitude: ')
location = [lat_input, long_input]

'''for i in range(0, 2):
    nlist = float(input(f"Coordinate {i + 1}: "))
    location.append(nlist)'''

fac_status = 'S'
latitude = 'AG'
longitude = 'AH'

a = 0.8
b = 2
c = 3
d = 10
e = 20
f = 50

a_value = 0
b_value = 0
c_value = 0
d_value = 0
e_value = 0
f_value = 0

for row in range(0, 121580):
    if sheet[f'{fac_status}{row + 1}'].value == 'PR':
        lat = sheet[f'{latitude}{row + 1}'].value
        long = sheet[f'{longitude}{row + 1}'].value
        coord = [lat, long]
        distance = geopy.distance.distance(location, coord).km
        if distance <= a:
            a_value += 1
        elif distance <= b:
            b_value += 1
        elif distance <= c:
            c_value += 1
        elif distance <= d:
            d_value += 1
        elif distance <= e:
            e_value += 1
        elif distance <= f:
            f_value += 1
prevalence = (2 * a_value) + b_value + (0.5 * c_value) + (0.1 * d_value) + (0.01 * e_value) + (0.001 * f_value)
prevalence = round(prevalence, 4)

