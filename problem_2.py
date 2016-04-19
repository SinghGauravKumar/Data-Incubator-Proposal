import numpy as np
import pylab as pl
import csv
import geopy
from geopy.distance import VincentyDistance as vincenty
all_csv=[]
csv_11=[]
csv_12=[]
csv_13=[]
csv_14=[]
csv_15=[]
with open('Calls_for_Service_2011.csv') as f:
    reader=csv.reader(f)
    header=reader.next()
    for line in reader:
        csv_11.append(line)
        
with open('Calls_for_Service_2012.csv') as f:
    reader=csv.reader(f)
    header=reader.next()
    for line in reader:
        csv_12.append(line)

with open('Calls_for_Service_2013.csv') as f:
    reader=csv.reader(f)
    header=reader.next()
    for line in reader:
        csv_13.append(line)

with open('Calls_for_Service_2014.csv') as f:
    reader=csv.reader(f)
    header=reader.next()
    for line in reader:
        csv_14.append(line)        

with open('Calls_for_Service_2015.csv') as f:
    reader=csv.reader(f)
    header=reader.next()
    for line in reader:
        csv_15.append(line)    
all_csv=csv_11+csv_12+csv_13+csv_14+csv_15
num_calls={'11':len(csv_11),'12':len(csv_12),'13':len(csv_13),'14':len(csv_14),'15':len(csv_15)}
call_type_list = [row[1] for row in all_csv]
call_type_11 = [row[1] for row in csv_11]
call_type_12 = [row[1] for row in csv_12]
call_type_13 = [row[1] for row in csv_13]
call_type_14 = [row[1] for row in csv_14]
call_type_15 = [row[1] for row in csv_15]
unique_types = np.unique(call_type_list)
from collections import Counter
call_type_counter_all = Counter(call_type_list)
call_type_counter_all_11 = Counter(call_type_11)
call_type_counter_all_12 = Counter(call_type_12)
call_type_counter_all_13 = Counter(call_type_13)
call_type_counter_all_14 = Counter(call_type_14)
call_type_counter_all_15 = Counter(call_type_15)
sorted_types_all = call_type_counter_all.most_common()
sorted_call_type_11 = call_type_counter_all_11.most_common()
sorted_call_type_12 = call_type_counter_all_12.most_common()
sorted_call_type_13 = call_type_counter_all_13.most_common()
sorted_call_type_14 = call_type_counter_all_14.most_common()
sorted_call_type_15 = call_type_counter_all_15.most_common()
counter_dict_all = dict(sorted_types_all)
counter_dict_11 = dict(sorted_call_type_11)
counter_dict_12 = dict(sorted_call_type_12)
counter_dict_13 = dict(sorted_call_type_13)
counter_dict_14 = dict(sorted_call_type_14)
counter_dict_15 = dict(sorted_call_type_15)
decrease_15_11={}
for key,val in counter_dict_11.iteritems():
    if key in counter_dict_15.keys():
        val_15 = counter_dict_15[key]
    else:
        val_15=0
    decrease_15_11[key] = float(val-val_15)/val
sorted_decrease=np.sort(decrease_15_11.values())
top_decrease=sorted_decrease[-1]
probs_all = {}
all_events_csv = len(call_type_list)
for key,val in counter_dict_all.iteritems():
    probs_all[key]=float(val)/all_events_csv
probs_11 = {}
all_events_11 = len(call_type_11)
for key,val in counter_dict_11.iteritems():
    probs_11[key]=float(val)/all_events_11  
probs_12 = {}
all_events_12 = len(call_type_12)
for key,val in counter_dict_12.iteritems():
    probs_12[key]=float(val)/all_events_12  
probs_13 = {}
all_events_13 = len(call_type_13)
for key,val in counter_dict_13.iteritems():
    probs_13[key]=float(val)/all_events_13   
probs_14 = {}
all_events_14 = len(call_type_14)
for key,val in counter_dict_14.iteritems():
    probs_14[key]=float(val)/all_events_14
probs_15 = {}
all_events_15 = len(call_type_15)
for key,val in counter_dict_15.iteritems():
    probs_15[key]=float(val)/all_events_15
import operator
sorted_probs_all = sorted(probs_all.items(), key=operator.itemgetter(1))[::-1]
sorted_probs_11 = sorted(probs_11.items(), key=operator.itemgetter(1))[::-1]
sorted_probs_12 = sorted(probs_12.items(), key=operator.itemgetter(1))[::-1]
sorted_probs_13 = sorted(probs_13.items(), key=operator.itemgetter(1))[::-1]
sorted_probs_14 = sorted(probs_14.items(), key=operator.itemgetter(1))[::-1]
sorted_probs_15 = sorted(probs_15.items(), key=operator.itemgetter(1))[::-1]
most_common_all = call_type_counter_all.most_common()[0]
top_fraction = float(most_common_all[1])/len(all_csv)
import datetime
from dateutil import parser
response_times=[]
district_response={}
district_types={}
for row in all_csv:
    if row[8]!='' and row[7]!='':
        arrival=parser.parse(row[8])
        dispatch=parser.parse(row[7])
        response=(arrival-dispatch).total_seconds()
        response_times.append(response)
        district = row[14]
        if district in district_response.keys():
            district_response[district]=district_response[district]+[response]
        else:
            district_response[district]=[response]
    if row[1]!='':
        event_type=row[1]
        if district in district_types.keys():
            district_types[district]=district_types[district]+[event_type]
        else:
            district_types[district]=[event_type]
district_mean_times={}
for district in district_response:
    d_response_times=district_response[district]
    valid_district_times=[response_time for response_time in d_response_times if response_time>=0]
    average_response = np.mean(valid_district_times)
    district_mean_times[district]=average_response
sorted_times = sorted(district_mean_times.items(), key=operator.itemgetter(1))[::-1]
diff_shortest_longest = sorted_times[0][1]-sorted_times[-1][1]
probs_all = {}
all_events_csv = len(call_type_list)
for key,val in counter_dict_all.iteritems():
    if val>100:
        probs_all[key]=float(val)/all_events_csv
district_probs={}
prob_ratios={}
for district,events in district_types.iteritems():
    total_events = float(len(events))
    call_type_counter_all_i = Counter(events)
    probs_i={}
    ratios_i={}
    for item in call_type_counter_all_i.iteritems():
        num_i=item[1]
        if num_i>100:
            probs_i[item[0]]=num_i/total_events
            ratios_i[item[0]]=num_i/total_events/probs_all[item[0]]
    district_probs[district]=probs_i
    prob_ratios[district]=ratios_i
district_maxes=[]
for district,ratio_dict in prob_ratios.iteritems():
    sorted_ratios = sorted(ratio_dict.items(), key=operator.itemgetter(1))[::-1]
    if district!='0':
        district_maxes.append(sorted_ratios[0][1])
max_overall=np.max(district_maxes)
positive_times=[response_time for response_time in response_times if response_time>0]
valid_times=[response_time for response_time in response_times if response_time>=0]
median_response=np.median(valid_times)
median_positive=np.median(positive_times)
hour_dispositions=np.zeros(24)
hour_dispositions=[[] for hour in hour_dispositions]
for row in all_csv:
    creation=parser.parse(row[6])
    creation_hour=creation.hour
    disposition=row[10]
    hour_dispositions[creation_hour].append(disposition)
nums_per_hour=[]
hour_counts=[]
for disp in hour_dispositions:
    nums_per_hour.append(len(disp))
    disp_counter = Counter(disp)
    hour_counts.append(disp_counter)
hour_fractions=[]
for i,hour_count in enumerate(hour_counts):
    fractions_i={}
    for disp,count in hour_count.iteritems():
        fractions_i[disp]=float(count)/nums_per_hour[i]
    hour_fractions.append(fractions_i)
all_disp_types=[]
for hour,counter in enumerate(hour_counts):
    all_disp_types=all_disp_types+counter.keys()
all_disp_types=np.unique(all_disp_types)
fractions_per_type={}
for disp_type in all_disp_types:
    fractions_per_type[disp_type]=np.zeros(24)
    for hour,hour_fracs in enumerate(hour_fractions):
        if disp_type in hour_fracs.keys():
            frac_i=hour_fracs[disp_type]
        else:
            frac_i=0.0
        fractions_per_type[disp_type][hour]=frac_i
disp_std={}
disp_ranges={}
for dt,fracs in fractions_per_type.iteritems():
    disp_std[dt]=np.std(fracs)
    disp_max=max(fracs)
    disp_min=min(fracs)
    disp_range=disp_max-disp_min
    disp_ranges[dt]=disp_range
sorted_ranges=sorted(disp_ranges.items(), key=operator.itemgetter(1))[::-1]
districts=district_mean_times.keys()
district_codes=range(9)
district_locations=[[] for i in range(9)]
from ast import literal_eval
for row in all_csv:
    try:
        location=row[-1]
        if location!='':
            location=literal_eval(location)
            district_code=int(row[14])
            district_locations[district_code].append([location[0],location[1]])
        else:
            pass
    except:
        print row
csv_coord=(29.951065,-90.071533)
district_standard_deviations=[[] for i in range(9)]
for district, locations in enumerate(district_locations):
    locations=np.array(locations)
    clean_locations=[]
    for location in locations:
        if np.abs(location[0])>1 and np.abs(location[1])>1:
            clean_locations.append(location)
    x_std=np.std(np.array(clean_locations)[:,0])
    y_std=np.std(np.array(clean_locations)[:,1])
    district_standard_deviations[district]=[x_std,y_std]
areas=[]
for stds in district_standard_deviations:
    fake_point_x=(csv_coord[0]+stds[0],csv_coord[1])
    fake_point_y=(csv_coord[0],csv_coord[1]+stds[1])
    a=vincenty(csv_coord, fake_point_x).km
    b=vincenty(csv_coord, fake_point_y).km
    area=np.pi*a*b
    areas.append(area)
clean_areas=areas[1:]
unique_call_type_list=list(unique_types)
type_priorities=[[] for i in range(len(unique_types))]
for row in all_csv:
    call_type=row[1]
    priority=row[3]
    type_index=unique_call_type_list.index(call_type)
    type_priorities[type_index].append(priority)
priority_counts=[]
max_priority_fracs=[]
for call_type, priorities in enumerate(type_priorities):
    priority_counter = Counter(priorities)
    sorted_priorities=sorted(priority_counter.items(), key=operator.itemgetter(1))[::-1]
    priority_counts.append(sorted_priorities)
    most_common=sorted_priorities[0][1]
    fraction_i=float(most_common)/len(priorities)
    max_priority_fracs.append(fraction_i)
min_priority=min(max_priority_fracs)
min_priority_index=max_priority_fracs.index(min_priority)
min_priority_type=unique_call_type_list[min_priority_index]
