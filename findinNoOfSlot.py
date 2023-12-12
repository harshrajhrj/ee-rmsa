from math import ceil

# [900, 1000, 1000, 1200, 2050] [[10, 8], [10, 9], [9, 7], [8, 5], [10, 13, 17]] {10: [8, 9, 13], 8: [5], 9: [7], 7: [], 5: [], 13: [17], 17: []}
def noOfSlots(bandwidth,dist_array):
    guard=2
    slots_arr=[]
    for dist in dist_array:
        path_slot=0
        mf=0
        if(2000<dist<=4000):
            mf=1
        elif 1000<dist<=2000 :
            mf=2
        elif 500<dist<=1000 :
            mf=3
        elif 0<dist<=500: 
            mf=4
        path_slot=ceil(bandwidth/(12.5*mf))+guard
        slots_arr.append(path_slot)
    return slots_arr
        
# print(noOfSlots(100,[900, 1000, 1000, 1200, 2050]))


def assignSlots(slots_list,paths,link_mat):
    for idx,tot_path in enumerate(paths):
        slots=slots_list[idx]
        tuple_list = [(tot_path[i], tot_path[i+1]) if tot_path[i] < tot_path[i+1] else (tot_path[i+1], tot_path[i]) for i in range(len(tot_path)-1)]
        # print(f"tuple list (pair): for {tot_path}",tuple_list)
        if link_mat is None:
            return None
        link_mat=find_sequence(link_mat,slots,tuple_list)
        
    return link_mat

def find_sequence(lists_dict, seq_length, keys):
    n = len(lists_dict[keys[0]])
    for i in range(n-seq_length+1):
        if all(all(lists_dict[key][i+j] == 0 for key in keys) for j in range(seq_length)):
            for key in keys:
                for j in range(seq_length):
                    lists_dict[key][i+j] = 1
            return lists_dict
    return None
