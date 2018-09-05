
import pexpect
import time
import sys
import os

def hexStrToInt(hexstr):
    val = int(hexstr[0:2],16) + (int(hexstr[3:5],16)<<8)
    if ((val&0x8000)==0x8000): # treat signed 16bits
        val = -((val^0xffff)+1)
    return val

DEVICE = "43:45:C0:00:1F:AC"   # device #24
if len(sys.argv) == 2:
  DEVICE = str(sys.argv[1])

# Run gatttool interactively.
child = pexpect.spawn("gatttool -I")

# Connect to the device.
print("Connecting to:"),
print(DEVICE)
NOF_REMAINING_RETRY = 3

while True:
  try:
    child.sendline("connect {0}".format(DEVICE))
    child.expect("Connection successful", timeout=5)
  except pexpect.TIMEOUT:
    NOF_REMAINING_RETRY = NOF_REMAINING_RETRY-1
    if (NOF_REMAINING_RETRY>0):
      print "timeout, retry..."
      continue
    else:
      print "timeout, giving up."
      break
  else:
    print("Connected!")
    break

if NOF_REMAINING_RETRY>0:
  unixTime = int(time.time())
  unixTime += 60*60 # GMT+1
  unixTime += 60*60 # added daylight saving time of one hour

  # open file
  file = open("data.csv", "a")
  if (os.path.getsize("data.csv")==0):
    file.write("Device\ttime\t")

  file.write(DEVICE)
  file.write("\t")
  file.write(str(unixTime)) # Unix timestamp in seconds 
  file.write("\t")
  file.write("\n")
  file.close()
  print("done!")
  sys.exit(0)
else:
  print("FAILED!")
  sys.exit(-1)