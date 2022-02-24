df_wells = pd.read_excel(r'C:\Users\elton\projects\fracking wells.xlsx')
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

        df_no2 = pd.read_excel(r'C:\Users\elton\projects\wind and no2.xlsx')
        reg_no2_mean = linear_model.LinearRegression()
        reg_no2_mean.fit(df_no2[['Overall']],df_no2.Mean)
        reg_no2_highest = linear_model.LinearRegression()
        reg_no2_highest.fit(df_no2[['Overall']], df_no2.Highest)
        df_ozone = pd.read_excel(r'C:\Users\elton\projects\wind and ozone summer.xlsx')
        reg_ozone_mean = linear_model.LinearRegression()
        reg_ozone_mean.fit(df_ozone[['Overall']], df_ozone.Mean)
        reg_ozone_highest = linear_model.LinearRegression()
        reg_ozone_highest.fit(df_ozone[['Overall']], df_ozone.Highest)

        result = well_activity_center(latitude, longitude)

        if direction.lower() == 'n':
            direc = result[0]
            df = result[8]
        elif direction.lower() == 'ne':
            direc = result[1]
            df = result[9]
        elif direction.lower() == 'e':
            direc = result[2]
            df = result[10]
        elif direction.lower() == 'se':
            direc = result[3]
            df = result[11]
        elif direction.lower() == 's':
            direc = result[4]
            df = result[12]
        elif direction.lower() == 'sw':
            direc = result[5]
            df = result[13]
        elif direction.lower() == 'w':
            direc = result[6]
            df = result[14]
        elif direction.lower() == 'nw':
            direc = result[7]
            df = result[15]

        site_coord = [latitude, longitude]
        L = geopy.distance.distance(site_coord, direc).km
        s = 0.0
        a = 5
        z = float(speed)
        for num in range(1, len(df)):
            if pd.isnull(df.iloc[num, 2]) is True:
                continue
            s += round(float(df.iloc[num, 2]), 3)
        s = (s / 2) - ((5 * z) - 25)
        if L != 0:
            wind = (15 / L) * (s) / a
        if s < 0:
            wind = 0

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
        for row in range(0, len(df_wells)):
            value = df_wells.loc[row, 'Oil or Gas']
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
            elif distance <= b:
                b_value += value
            elif distance <= c:
                c_value += value
            elif distance <= d:
                d_value += value
            elif distance <= e:
                e_value += value
            elif distance <= f:
                f_value += value
        prevalenceloc = (2 * a_value) + (1 * b_value) + (0.5 * c_value) + (0.2 * d_value) + (0.01 * e_value) + (
                0.001 * f_value) * 3

        overall = round(wind + prevalenceloc, 2)
        no2_highest = reg_no2_highest.predict(np.array([[overall]]))
        no2_mean = reg_no2_mean.predict(np.array([[overall]]))
        ozone_highest = reg_ozone_highest.predict(np.array([[overall]]))
        ozone_mean = reg_ozone_mean.predict(np.array([[overall]]))
        print(f"Prevalence (wind and locational): {overall}, "
                            f"NO2 Mean = {no2_mean}, "
                            f"NO2 Highest = {no2_highest}, "
                            f"Ozone Mean = {ozone_mean}, "
                            f"Ozone Highest = {ozone_highest}, ")
