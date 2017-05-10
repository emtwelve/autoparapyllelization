from copy import deepcopy


i = range(1,3,1)
j = range(4,6,1)
k = range(7,9,1)
lstlst = {'i':i,'j':j,'k':k}

def DP(doflsts):
  if len(doflsts) == 1:
    d_lst = []
    for itr, vals in doflsts.items():
      for val in vals:
        d_lst.append({itr:val})
    return  d_lst
  else:
    key = doflsts.keys()[0]
    lst = doflsts[key]
    del doflsts[key]
    d_lst = DP(doflsts)
    new_d_lst = []
    for val in lst:
      for ds in d_lst:
        new_d = deepcopy(ds)
        new_d[key] = val
        new_d_lst.append(new_d)
    return new_d_lst

