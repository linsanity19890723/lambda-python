t2medium = 0.0584*2
t2micro = 0.0146*2
t2small =0.0292*2
t3medium = 0.0528*6
t3small = 0.0264*1
allinstance = t2medium + t2micro + t2small + t3medium + t3small
print('stage instance cost:' + str(allinstance) + 'USD')

oneyearhour = 8760
holidayhour = 2760

nowcost = allinstance * oneyearhour
print('nowcost:'+ str(nowcost) + 'USD')

oneyearworkhour = (365-115)*13
futurecost = allinstance * oneyearworkhour
print('futurecost :'+ str(futurecost) + 'USD')

reducedcost = (nowcost - futurecost) / nowcost
reducedcostnum = (nowcost - futurecost)
print('reducedcost:' + str(reducedcost) + '%')
print('reducedcostnum:'+ str(reducedcostnum) + 'USD')