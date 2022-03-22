from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
import geopy.distance
import math
import numpy as np
from shapely.geometry import Point
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, Lasso, ElasticNet, Ridge
from sklearn.svm import SVR
from sklearn.metrics import r2_score, mean_squared_error, classification_report
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from django.core.exceptions import *
from openpyxl import load_workbook
from sklearn import linear_model


def index(request):
    return render(request, 'hello.html')


def prevalence(request):
    if request.method == 'POST':
        df_wells = pd.read_excel(r'C:\Users\elton\projects\fracking wells.xlsx')
        df_cities = pd.read_csv(r'C:\Users\elton\projects\co city data.csv')
        latitude = float(request.POST.get('latitude', None))
        longitude = float(request.POST.get('longitude', None))
        speed = float(request.POST.get('speed', None))
        direction = request.POST.get('direction', None)

        def well_activity_center(lat_input, long_input):
            for num1 in range(0, 8):
                lat = [0]
                long = [0]
                val = [0]
                toprow = {'Latitude': lat, 'Longitude': long, 'Value': val}
                if num1 == 0:
                    df_north = pd.DataFrame(toprow)
                elif num1 == 1:
                    df_northeast = pd.DataFrame(toprow)
                elif num1 == 2:
                    df_east = pd.DataFrame(toprow)
                elif num1 == 3:
                    df_southeast = pd.DataFrame(toprow)
                elif num1 == 4:
                    df_south = pd.DataFrame(toprow)
                elif num1 == 5:
                    df_southwest = pd.DataFrame(toprow)
                elif num1 == 6:
                    df_west = pd.DataFrame(toprow)
                elif num1 == 7:
                    df_northwest = pd.DataFrame(toprow)
            loc = [lat_input, long_input]
            for row in range(0, len(df_wells)):
                temp_lat = latitude
                temp_long = longitude
                temp_loc = [temp_lat, temp_long]
                dist = geopy.distance.distance(loc, temp_loc).km
                if 20 <= dist <= 50:
                    value = df_wells.loc[row, 'Oil or Gas']
                    if value > 0.1:
                        value = value - (value * 0.5)
                    if value < 0.1:
                        value = 0.1
                    hyp = math.hypot(abs(lat_input - temp_lat), abs(long_input - temp_long))
                    # print(f'Hyp: {hyp}')
                    angle = 0
                    adj_dist = abs(long_input - temp_long)
                    adj_dist_ref = -(long_input - temp_long)
                    opp = -(lat_input - temp_lat)
                    # print(f'Adj: {adj_dist_ref}, Opp: {opp}')
                    rad = (abs(adj_dist) / hyp)
                    deg = math.degrees(math.acos(rad))
                    # print(f'Deg: {deg}')
                    if opp < 0:
                        if adj_dist_ref < 0:
                            angle = 90 - deg + 180
                        elif adj_dist_ref > 0:
                            angle = deg + 90
                    elif opp > 0:
                        if adj_dist_ref < 0:
                            angle = deg + 270
                        elif adj_dist_ref > 0:
                            angle = 90 - deg
                    # print(f'Angle: {angle}')
                    if angle <= 22.5 or angle > 337.5:
                        data = {
                            'Latitude': [temp_lat],
                            'Longitude': [temp_long],
                            'Value': [value]
                        }
                        df = pd.DataFrame(data)
                        df_north.append(df)
                    elif 67.5 >= angle > 22.5:
                        data = {
                            'Latitude': [temp_lat],
                            'Longitude': [temp_long],
                            'Value': [value]
                        }
                        df = pd.DataFrame(data)
                        df_northeast.append(df)
                    elif 112.5 >= angle > 67.5:
                        data = {
                            'Latitude': [temp_lat],
                            'Longitude': [temp_long],
                            'Value': [value]
                        }
                        df = pd.DataFrame(data)
                        df_east.append(df)
                    elif 157.5 >= angle > 112.5:
                        data = {
                            'Latitude': [temp_lat],
                            'Longitude': [temp_long],
                            'Value': [value]
                        }
                        df = pd.DataFrame(data)
                        df_southeast.append(df)
                    elif 202.5 >= angle > 157.5:
                        data = {
                            'Latitude': [temp_lat],
                            'Longitude': [temp_long],
                            'Value': [value]
                        }
                        df = pd.DataFrame(data)
                        df_south.append(df)
                    elif 247.5 >= angle > 202.5:
                        data = {
                            'Latitude': [temp_lat],
                            'Longitude': [temp_long],
                            'Value': [value]
                        }
                        df = pd.DataFrame(data)
                        df_southwest.append(df)
                    elif 292.5 >= angle > 247.5:
                        data = {
                            'Latitude': [temp_lat],
                            'Longitude': [temp_long],
                            'Value': [value]
                        }
                        df = pd.DataFrame(data)
                        df_west.append(df)
                    elif 337.5 >= angle > 292.5:
                        data = {
                            'Latitude': [temp_lat],
                            'Longitude': [temp_long],
                            'Value': [value]
                        }
                        df = pd.DataFrame(data)
                        df_northwest.append(df)
            nlat_avg = 0
            nlong_avg = 0
            for n in range(0, len(df_north)):
                nlat_avg += df_north.iloc[n, 0]
                nlong_avg += df_north.iloc[n, 1]
            if len(df_north) != 1:
                # print(nlat_avg)
                # print(nlong_avg)
                nlat_avg = nlat_avg / (len(df_north) - 1)
                nlong_avg = nlong_avg / (len(df_north) - 1)
            ncenter = [nlat_avg, nlong_avg]
            nelat_avg = 0
            nelong_avg = 0
            for n in range(0, len(df_northeast)):
                nelat_avg += df_northeast.iloc[n, 0]
                nelong_avg += df_northeast.iloc[n, 1]
            if len(df_northeast) != 1:
                nelat_avg = nelat_avg / (len(df_northeast) - 1)
                nelong_avg = nelong_avg / (len(df_northeast) - 1)
            necenter = [nelat_avg, nelong_avg]
            elat_avg = 0
            elong_avg = 0
            for n in range(0, len(df_east)):
                elat_avg += df_east.iloc[n, 0]
                elong_avg += df_east.iloc[n, 1]
            if len(df_east) != 1:
                elat_avg = elat_avg / (len(df_east) - 1)
                elong_avg = elong_avg / (len(df_east) - 1)
            ecenter = [elat_avg, elong_avg]
            selat_avg = 0
            selong_avg = 0
            for n in range(0, len(df_southeast)):
                selat_avg += df_southeast.iloc[n, 0]
                selong_avg += df_southeast.iloc[n, 1]
            if len(df_southeast) != 1:
                selat_avg = selat_avg / (len(df_southeast) - 1)
                selong_avg = selong_avg / (len(df_southeast) - 1)
            secenter = [selat_avg, selong_avg]
            slat_avg = 0
            slong_avg = 0
            for n in range(0, len(df_south)):
                slat_avg += df_south.iloc[n, 0]
                slong_avg += df_south.iloc[n, 1]
            if len(df_south) != 1:
                slat_avg = slat_avg / (len(df_south) - 1)
                slong_avg = slong_avg / (len(df_south) - 1)
            scenter = [slat_avg, slong_avg]
            swlat_avg = 0
            swlong_avg = 0
            for n in range(0, len(df_southwest)):
                swlat_avg += df_southwest.iloc[n, 0]
                swlong_avg += df_southwest.iloc[n, 1]
            if len(df_southwest) != 1:
                swlat_avg = swlat_avg / (len(df_southwest) - 1)
                swlong_avg = swlong_avg / (len(df_southwest) - 1)
            swcenter = [swlat_avg, swlong_avg]
            wlat_avg = 0
            wlong_avg = 0
            for n in range(0, len(df_west)):
                wlat_avg += df_west.iloc[n, 0]
                wlong_avg += df_west.iloc[n, 1]
            if len(df_west) != 1:
                wlat_avg = wlat_avg / (len(df_west) - 1)
                wlong_avg = wlong_avg / (len(df_west) - 1)
            wcenter = [wlat_avg, wlong_avg]
            nwlat_avg = 0
            nwlong_avg = 0
            for n in range(0, len(df_northwest)):
                nwlat_avg += df_northwest.iloc[n, 0]
                nwlong_avg += df_northwest.iloc[n, 1]
            if len(df_northwest) != 1:
                nwlat_avg = nwlat_avg / (len(df_northwest) - 1)
                nwlong_avg = nwlong_avg / (len(df_northwest) - 1)
            nwcenter = [nwlat_avg, nwlong_avg]

            return ncenter, necenter, ecenter, secenter, scenter, swcenter, wcenter, nwcenter, df_north, df_northeast, \
                   df_east, df_southeast, df_south, df_southwest, df_west, df_northwest

        def city_wind_strength(lat_input, long_input):
            for num1 in range(0, 8):
                name = 'str'
                lat = [0]
                long = [0]
                val = [0]
                rad = [0]
                stre = [0]
                toprow = {'Latitude': lat, 'Longitude': long, 'Value': val, 'Radius': rad, 'Strength': stre}
                if num1 == 0:
                    df_north = pd.DataFrame(toprow)
                elif num1 == 1:
                    df_northeast = pd.DataFrame(toprow)
                elif num1 == 2:
                    df_east = pd.DataFrame(toprow)
                elif num1 == 3:
                    df_southeast = pd.DataFrame(toprow)
                elif num1 == 4:
                    df_south = pd.DataFrame(toprow)
                elif num1 == 5:
                    df_southwest = pd.DataFrame(toprow)
                elif num1 == 6:
                    df_west = pd.DataFrame(toprow)
                elif num1 == 7:
                    df_northwest = pd.DataFrame(toprow)
            loc = [lat_input, long_input]
            for row in range(0, len(df_cities)):
                radius = float(df_cities.loc[row, 'Radius'])
                if pd.isnull(radius) is True:
                    continue
                temp_lat = df_cities.loc[row, 'CENTLAT']
                temp_long = df_cities.loc[row, 'CENTLON']
                temp_loc = [temp_lat, temp_long]
                name = df_cities.loc[row, 'BASENAME']
                dist = geopy.distance.distance(loc, temp_loc).km
                if dist - radius > 50:
                    continue
                current_point = [temp_lat, temp_long]
                stren = df_cities.loc[row, 'Strength']
                stren = stren * 0.1
                pop = df_cities.loc[row, 'Population']
                for a in range(0, 3):
                    if a == 0:
                        b = 1 / 3
                        order = 1
                    elif a == 1:
                        b = 2 / 3
                        order = 0.5
                    elif a == 2:
                        b = 1
                        order = 0.2
                    lat = temp_lat
                    long = temp_long
                    temp_location = [temp_lat, temp_long]
                    num = False
                    while not num:
                        dist = geopy.distance.distance(current_point, temp_location).km
                        if round(dist, 1) == round(radius * b, 1):
                            num = True
                        elif round(dist, 1) < round(radius * b, 1):
                            lat -= 0.0001
                        elif round(dist, 1) > round(radius * b, 1):
                            lat += 0.0001
                        temp_location = [lat, long]
                    latref = temp_lat - lat
                    tlat = temp_lat
                    tlong = temp_long
                    lnum = False
                    while not lnum:
                        t_loc = [tlat, tlong]
                        t_dist = geopy.distance.distance(current_point, t_loc).km
                        if round(t_dist, 1) == round(radius * b, 1):
                            lnum = True
                        elif round(t_dist, 1) < round(radius * b, 1):
                            tlong -= 0.0001
                        elif round(t_dist, 1) > round(radius * b, 1):
                            tlong += 0.0001
                    longref = (abs(temp_long - tlong) + abs(latref)) / 2
                    circle = Point(temp_lat, temp_long).buffer(longref)
                    points = np.array(list(circle.exterior.coords))
                    pnum1 = 0
                    pnum2 = 0
                    pnum3 = 0
                    for row in range(0, len(points)):
                        dist = geopy.distance.distance(loc, points[row]).km
                        if 20 <= dist <= 50:
                            if order == 1:
                                pnum1 += 1
                            elif order == 0.5:
                                pnum2 += 1
                            elif order == 0.2:
                                pnum3 += 1
                            if order == 1 and pnum1 >= 40:
                                continue
                            elif order == 2 and pnum2 >= 40:
                                continue
                            elif order == 3 and pnum3 >= 40:
                                continue
                            value = pop
                            hyp = math.hypot(abs(lat_input - temp_lat), abs(long_input - temp_long))
                            # print(f'Hyp: {hyp}')
                            angle = 0
                            adj_dist = abs(long_input - temp_long)
                            adj_dist_ref = -(long_input - temp_long)
                            opp = -(lat_input - temp_lat)
                            # print(f'Adj: {adj_dist_ref}, Opp: {opp}')
                            rad = (abs(adj_dist) / hyp)
                            deg = math.degrees(math.acos(rad))
                            # print(f'Deg: {deg}')
                            if opp < 0:
                                if adj_dist_ref < 0:
                                    angle = 90 - deg + 180
                                elif adj_dist_ref > 0:
                                    angle = deg + 90
                            elif opp > 0:
                                if adj_dist_ref < 0:
                                    angle = deg + 270
                                elif adj_dist_ref > 0:
                                    angle = 90 - deg
                            # print(f'Angle: {angle}')
                            if angle <= 22.5 or angle > 337.5:
                                data = {
                                    'Latitude': [temp_lat],
                                    'Longitude': [temp_long],
                                    'Value': [value],
                                    'Radius': [order],
                                    'Strength': [stren]
                                }
                                df = pd.DataFrame(data)
                                df_north.append(df)
                            elif 67.5 >= angle > 22.5:
                                data = {
                                    'Latitude': [temp_lat],
                                    'Longitude': [temp_long],
                                    'Value': [value],
                                    'Radius': [order],
                                    'Strength': [stren]
                                }
                                df = pd.DataFrame(data)
                                df_northeast.append(df)
                            elif 112.5 >= angle > 67.5:
                                data = {
                                    'Latitude': [temp_lat],
                                    'Longitude': [temp_long],
                                    'Value': [value],
                                    'Radius': [order],
                                    'Strength': [stren]
                                }
                                df = pd.DataFrame(data)
                                df.to_csv('cities_east.csv', mode='a', index=False, header=False)
                                df_east.append(df)
                            elif 157.5 >= angle > 112.5:
                                data = {
                                    'Latitude': [temp_lat],
                                    'Longitude': [temp_long],
                                    'Value': [value],
                                    'Radius': [order],
                                    'Strength': [stren]
                                }
                                df = pd.DataFrame(data)
                                df.to_csv('cities_southeast.csv', mode='a', index=False, header=False)
                                df_southeast.append(df)
                            elif 202.5 >= angle > 157.5:
                                data = {
                                    'Latitude': [temp_lat],
                                    'Longitude': [temp_long],
                                    'Value': [value],
                                    'Radius': [order],
                                    'Strength': [stren]
                                }
                                df = pd.DataFrame(data)
                                df_south.append(df)
                            elif 247.5 >= angle > 202.5:
                                data = {
                                    'Latitude': [temp_lat],
                                    'Longitude': [temp_long],
                                    'Value': [value],
                                    'Radius': [order],
                                    'Strength': [stren]
                                }
                                df = pd.DataFrame(data)
                                df_southwest.append(df)
                            elif 292.5 >= angle > 247.5:
                                data = {
                                    'Latitude': [temp_lat],
                                    'Longitude': [temp_long],
                                    'Value': [value],
                                    'Radius': [order],
                                    'Strength': [stren]
                                }
                                df = pd.DataFrame(data)
                                df_west.append(df)
                            elif 337.5 >= angle > 292.5:
                                data = {
                                    'Latitude': [temp_lat],
                                    'Longitude': [temp_long],
                                    'Value': [value],
                                    'Radius': [order],
                                    'Strength': [stren]
                                }
                                df = pd.DataFrame(data)
                                df_northwest.append(df)

            n_value = 0
            for n in range(0, len(df_north)):
                n_value += df_north.iloc[n, 4] * df_north.iloc[n, 3] * 0.1
            ne_value = 0
            for n in range(0, len(df_northeast)):
                ne_value += df_northeast.iloc[n, 4] * df_northeast.iloc[n, 3] * 0.1
            e_value = 0
            for n in range(0, len(df_east)):
                e_value += df_east.iloc[n, 4] * df_east.iloc[n, 3] * 0.1
            se_value = 0
            for n in range(0, len(df_southeast)):
                se_value += df_southeast.iloc[n, 4] * df_southeast.iloc[n, 3] * 0.1
            s_value = 0
            for n in range(0, len(df_south)):
                s_value += df_south.iloc[n, 4] * df_south.iloc[n, 3] * 0.1
            sw_value = 0
            for n in range(0, len(df_southwest)):
                sw_value += df_southwest.iloc[n, 4] * df_southwest.iloc[n, 3] * 0.1
            w_value = 0
            for n in range(0, len(df_west)):
                w_value += df_west.iloc[n, 4] * df_west.iloc[n, 3] * 0.1
            nw_value = 0
            for n in range(0, len(df_northwest)):
                nw_value += df_northwest.iloc[n, 4] * df_northwest.iloc[n, 3] * 0.1

            return n_value, ne_value, e_value, se_value, s_value, sw_value, w_value, nw_value

        result = well_activity_center(latitude, longitude)
        cities = city_wind_strength(latitude, longitude)

        cn = cities[0]
        cne = cities[1]
        ce = cities[2]
        cse = cities[3]
        cs = cities[4]
        csw = cities[5]
        cw = cities[6]
        cnw = cities[7]

        direcn = result[0]
        dfn = result[8]
        direcne = result[1]
        dfne = result[9]
        direce = result[2]
        dfe = result[10]
        direcse = result[3]
        dfse = result[11]
        direcs = result[4]
        dfs = result[12]
        direcsw = result[5]
        dfsw = result[13]
        direcw = result[6]
        dfw = result[14]
        direcnw = result[7]
        dfnw = result[15]

        site_coord = [latitude, longitude]

        n = 0.05
        ne = 0.05
        e = 0.05
        se = 0.05
        swind = 0.05
        sw = 0.05
        w = 0.05
        nw = 0.05
        if direction.lower() == 'n':
            n = 0.65
        elif direction.lower() == 'ne':
            ne = 0.65
        elif direction.lower() == 'e':
            e = 0.65
        elif direction.lower() == 'se':
            se = 0.65
        elif direction.lower() == 's':
            s = 0.65
        elif direction.lower() == 'sw':
            sw = 0.65
        elif direction.lower() == 'w':
            w = 0.65
        elif direction.lower() == 'nw':
            nw = 0.65

        a = 5
        z = float(speed)
        for direc in range(0, 8):
            site_coord = [latitude, longitude]
            if direc == 0:
                L = geopy.distance.distance(site_coord, direcn).km
                s = 0.0
                for num in range(1, len(dfn)):
                    if pd.isnull(dfn.iloc[num, 2]) is True:
                        continue
                    s += float(round(dfn.iloc[num, 2], 3))
                s = (s / 2) + ((z) - 5)
                x = n
                if L != 0:
                    north_iter = (15 / L) * (s) * x / a * 10
                if s < 0:
                    north_iter = 0
            elif direc == 1:
                L = geopy.distance.distance(site_coord, direcne).km
                s = 0.0
                for num in range(1, len(dfne)):
                    if pd.isnull(dfne.iloc[num, 2]) is True:
                        continue
                    s += round(float(dfne.iloc[num, 2]), 3)
                s = (s / 2) + ((5 * z) - 25)
                x = ne
                if L != 0:
                    northeast_iter = (15 / L) * (s) * x / a * 10
                if s < 0:
                    northeast_iter = 0
            elif direc == 2:
                L = geopy.distance.distance(site_coord, direce).km
                s = 0.0
                for num in range(1, len(dfe)):
                    if pd.isnull(dfe.iloc[num, 2]) is True:
                        continue
                    s += round(float(dfe.iloc[num, 2]), 3)
                x = e
                s = (s / 2) + ((5 * z) - 25)
                if L != 0:
                    east_iter = (15 / L) * (s) * x / a * 10
                if s < 0:
                    east_iter = 0
            elif direc == 3:
                L = geopy.distance.distance(site_coord, direcse).km
                s = 0.0
                for num in range(1, len(dfse)):
                    if pd.isnull(dfse.iloc[num, 2]) is True:
                        continue
                    s += round(float(dfse.iloc[num, 2]), 3)
                s = (s / 2) + ((5 * z) - 25)
                x = se
                if L != 0:
                    southeast_iter = (15 / L) * (s) * x / a * 10
                if s < 0:
                    southeast_iter = 0
            elif direc == 4:
                L = geopy.distance.distance(site_coord, direcs).km
                s = 0.0
                for num in range(1, len(dfs)):
                    if pd.isnull(dfs.iloc[num, 2]) is True:
                        continue
                    s += round(float(dfs.iloc[num, 2]), 3)
                s = (s / 2) + ((5 * z) - 25)
                x = swind
                if L != 0:
                    south_iter = (15 / L) * (s) * x / a * 10
                if s < 0:
                    south_iter = 0
            elif direc == 5:
                L = geopy.distance.distance(site_coord, direcsw).km
                s = 0.0
                for num in range(1, len(dfsw)):
                    if pd.isnull(dfsw.iloc[num, 2]) is True:
                        continue
                    s += round(float(dfsw.iloc[num, 2]), 3)
                s = (s / 2) + ((5 * z) - 25)
                x = sw
                if L != 0:
                    southwest_iter = (15 / L) * (s) * x / a * 10
                if s < 0:
                    southwest_iter = 0
            elif direc == 6:
                L = geopy.distance.distance(site_coord, direcw).km
                s = 0.0
                for num in range(1, len(dfw)):
                    if pd.isnull(dfw.iloc[num, 2]) is True:
                        continue
                    s += round(float(dfw.iloc[num, 2]), 3)
                s = (s / 2) + ((5 * z) - 25)
                x = w
                if L != 0:
                    west_iter = (15 / L) * (s) * x / a * 10
                if s < 0:
                    west_iter = 0
            elif direc == 7:
                L = geopy.distance.distance(site_coord, direcnw).km
                s = 0.0
                for num in range(1, len(dfnw)):
                    if pd.isnull(dfnw.iloc[num, 2]) is True:
                        continue
                    s += round(float(dfnw.iloc[num, 2]), 3)
                s = (s / 2) + ((5 * z) - 25)
                x = nw
                if L != 0:
                    northwest_iter = (15 / L) * (s) * x / a * 10
                if s < 0:
                    northwest_iter = 0

        bn = round(cn, 2) * round(n, 2)
        bne = round(cne, 2) * round(ne, 2)
        be = round(ce, 2) * round(e, 2)
        bse = round(cse, 2) * round(se, 2)
        bs = round(cs, 2) * round(swind, 2)
        bsw = round(csw, 2) * round(sw, 2)
        bw = round(cw, 2) * round(w, 2)
        bnw = round(cnw, 2) * round(nw, 2)

        a_value = 0
        b_value = 0
        c_value = 0
        d_value = 0
        e_value = 0
        f_value = 0
        a = 0.8
        b = 2
        c = 3
        d = 10
        e = 20
        f = 50
        total = 0
        count = 0
        for row in range(0, len(df_wells)):
            value = df_wells.loc[row, 'Oil or Gas']
            if value > 0.1:
                value = value - (value * 0.5)
            if value < 0.1:
                value = 0.1
            if np.isinf(value) is True:
                value = 0.3
            if pd.isnull(value) is True:
                value = 0.5
            if np.isinf(value) is True:
                value = 0.3
            if pd.isnull(value) is True:
                value = 0.5
            lat = df_wells.loc[row, 'Latitude']
            long = df_wells.loc[row, 'Longitude']
            coord = [lat, long]
            distance = geopy.distance.distance(site_coord, coord).km
            if distance <= a:
                a_value += value
                total += value
                count += 1
            elif distance <= b:
                b_value += value
                total += value
                count += 1
            elif distance <= c:
                c_value += value
                total += value
                count += 1
            elif distance <= d:
                d_value += value
                total += value
                count += 1
            elif distance <= e:
                e_value += value
                total += value
                count += 1
            elif distance <= f:
                f_value += value
        prevalenceloc = (2 * a_value) + (1 * b_value) + (0.5 * c_value) + (0.2 * d_value) + (0.01 * e_value) * 3
        total = total / count

        a_value = 0
        b_value = 0
        c_value = 0
        d_value = 0
        e_value = 0
        site_lat = latitude
        site_long = longitude
        location = [site_lat, site_long]
        for row in range(0, len(df_cities)):
            pop = df_cities.loc[row, 'Population']
            if pd.isnull(pop) is True:
                continue
            clat = df_cities.loc[row, 'CENTLAT']
            clong = df_cities.loc[row, 'CENTLON']
            cor = [clat, clong]
            cdistance = geopy.distance.distance(location, cor).km
            if pop >= 500000:
                radius = 15
                stren = 10
            elif pop >= 400000:
                radius = 12
                stren = 8
            elif pop >= 300000:
                radius = 8
                stren = 6
            elif pop >= 100000:
                radius = 6
                stren = 5
            elif pop >= 50000:
                radius = 4
                stren = 3
            elif pop >= 10000:
                radius = 3
                stren = 2
            elif pop >= 5000:
                radius = 2
                stren = 1
            else:
                radius = 1
                stren = 0.1
            dist2 = cdistance - (radius / 3)
            dist3 = cdistance - (radius * 2 / 3)
            dist4 = cdistance - radius
            df_cities.at[row, 'Radius'] = radius
            df_cities.at[row, 'Strength'] = stren

            if cdistance <= a:
                a_value += stren
                continue
            elif dist2 <= a:
                a_value += stren
                continue
            elif dist3 <= a:
                a_value += stren
                continue
            elif dist4 <= a:
                a_value += stren
                continue
            elif cdistance <= b:
                b_value += stren
                continue
            elif dist2 <= b:
                b_value += stren
                continue
            elif dist3 <= b:
                b_value += stren
                continue
            elif dist4 <= b:
                b_value += stren
                continue
            elif cdistance <= c:
                c_value += stren
                continue
            elif dist2 <= c:
                c_value += stren
                continue
            elif dist3 <= c:
                c_value += stren
                continue
            elif dist4 <= c:
                c_value += stren
                continue
            elif cdistance <= d:
                d_value += stren
                continue
            elif dist2 <= d:
                d_value += stren
                continue
            elif dist3 <= d:
                d_value += stren
                continue
            elif dist4 <= d:
                d_value += stren
                continue
            elif cdistance <= e:
                e_value += stren
                continue
            elif dist2 <= e:
                e_value += stren
                continue
            elif dist3 <= e:
                e_value += stren
                continue
            elif dist4 <= e:
                e_value += stren
                continue

        cityprevalence = (2 * a_value) + (1 * b_value) + (0.5 * c_value) + (0.2 * d_value) + (0.01 * e_value) * 3
        cityprevalence = round(cityprevalence, 3)
        city = cityprevalence
        city1 = (bn + bne + be + bse + bs + bsw + bw + bnw) / 30
        city2 = city / 35
        city_prevalence = city1 + city2

        wind_prevalence = north_iter + northeast_iter + east_iter + \
                          southeast_iter + south_iter + southwest_iter + west_iter + northwest_iter

        overall = round(wind_prevalence + prevalenceloc, 2)

        df_no2 = pd.read_excel(r'C:\Users\elton\projects\wind and no2 urban.xlsx')
        df_no2.drop_duplicates(inplace=True)
        x = df_no2.drop(['Overall', 'Highest', 'Mean', 'Mean_Urban', 'Highest_Urban', 'Unnamed: 10', 'Site Name'], axis=1)
        y = df_no2['Mean']
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)
        sc = MinMaxScaler()
        x_train = sc.fit_transform((x_train))
        x_test = sc.transform(x_test)
        model = LinearRegression()
        model.fit(x_train, y_train)
        xnew = [[prevalenceloc, wind_prevalence, city, total]]
        xnew = sc.transform(xnew)
        ynew = model.predict(xnew)
        no2_mean = ynew

        df_ozone = pd.read_excel(r'C:\Users\elton\projects\wind and ozone summer.xlsx')

        return HttpResponse(f"Prevalence (wind and locational): {overall}, "
                            f"NO2 Mean = {no2_mean}")



