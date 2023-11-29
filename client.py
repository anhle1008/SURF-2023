import ntplib
import time

SERVER = '128.138.140.211' # utcnist3.colorado.edu @ CU, Boulder (NTP only, Recommended)

def get_by_requests(num_requests):
    arr = []
    for i in range(num_requests):
        try:
            client = ntplib.NTPClient()
            response = client.request(SERVER, version=3)
            # Delay describes the round-trip delay of a timing 
            # message passed from client to server and back again
            rtt = response.delay
            # Offset generally refers to the difference in time between 
            # an external timing reference and time on a local machine.
            offset = response.offset
            ntp_time = response.tx_time     # the time reported by the NTP server
            minutes = int(ntp_time / 60)    # Convert NTP timestamp to minutes
            arr.append((minutes, offset, rtt))
            time.sleep(60)                  # Wait for 1 minute before the next request
            print(i+1, ": ", minutes)
        except Exception as e:
            print(f"Error requesting time from {SERVER}: {str(e)}")

    write_file(arr)

def write_file(arr):
    f1 = 'home_data.txt'

    with open(f1, 'a+') as file:
        file.write("Minutes\t\tOffsets\t\t\t\tRound-trip Delay\n")
        for minute, offset, rrt in arr:
            file.write(f"{minute}\t{offset}\t\t{rrt}\n")

    print(f"Data saved to {f1}.")

if __name__ == '__main__':
    get_by_requests(1440) # 24 hours
