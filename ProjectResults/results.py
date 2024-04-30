import subprocess

def runAllAlgo(pram1,pram2,pram3):
    #algo-1
    tot_req_slots = 3639
    subprocess.run(['python', './EE_RMSA-NEW/multicast_requestGen.py', str(pram1), str(pram2), str(pram3), str(tot_req_slots)])

    #algo-2
    tot_req_slots = 3606
    subprocess.run(['python', './EE_RMSA-NEW-1(i)/multicast_requestGen.py', str(pram1), str(pram2), str(pram3), str(tot_req_slots) ])

    #algo-3
    tot_req_slots = 3626
    subprocess.run(['python', './EE_RMSA-NEW-1(ii)/multicast_requestGen.py', str(pram1), str(pram2), str(pram3), str(tot_req_slots) ])

    # algo-4
    tot_req_slots = 3639
    subprocess.run(['python', './EE_RMSA-NEW-2/multicast_requestGen.py', str(pram1), str(pram2), str(pram3), str(tot_req_slots) ])


if __name__ == "__main__":
    request_path = './NewRequests24/Fixed-80/50_Fixed-80_24.txt'
    regenerator = 100
    slots = 221
    runAllAlgo(request_path, regenerator, slots)