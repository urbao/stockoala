from date_time import add_1day

# check which twse stock id is wut we want
def chk_twse_id(row):
    if(row.count("\"")!=32): # the row is too short
        return False
    # try to find the indivdual stock based on id
    array=row.split("\"")
    if(len(array[1])>=5): # id too long
        return False
    if(int(array[1][0:4])<1000): # id too small(since first stock start from 1101)
        return False
    return True # the stock we looking for

# remove extra data of twse(ONLY left 'stock id/high/low')
def twse_rm_extras(filename):
    data=open(filename+"[twse].csv", 'r', encoding='ISO-8859-1')
    f=open(filename+"[twse].txt",'w')
    for row in data:
        if(chk_twse_id(row)):
            arr=row.split("\"")
            f.write(arr[1]+"/"+arr[13]+"/"+arr[15]+"\n")
    f.close()
    import os
    os.remove(filename+"[twse].csv") # no more needed
    return

# remove extra data of tpex(ONLY left 'stock id/high/low')
def tpex_rm_extras(filename):
    with open(filename+"[tpex].json", 'r') as j:
        import json
        data=json.loads(j.read())
        f=open(filename+"[tpex].txt",'w')
        for idx in range(int(data['iTotalRecords'])):
            if(len(data['aaData'][idx][0])<5):
                f.write(data['aaData'][idx][0]+"/"+data['aaData'][idx][5]+"/"+data['aaData'][idx][6]+"\n")
        f.close()
    j.close()
    import os 
    os.remove(filename+"[tpex].json")
    return
