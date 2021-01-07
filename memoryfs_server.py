import pickle, logging, sys,time,hashlib

from memoryfs_client import BLOCK_SIZE, TOTAL_NUM_BLOCKS

from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

CHECK_SUM_SIZE = 16   
# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
  rpc_paths = ('/RPC2',)

class DiskBlocks():
  def __init__(self):
    # This class stores the raw block array
    self.block = []    
    self.checksum = [] 
    self.damged_block_index = None                                      
    # Initialize raw blocks 
    for i in range (0, TOTAL_NUM_BLOCKS):
      putdata = bytearray(BLOCK_SIZE)
      check_sum = bytearray(CHECK_SUM_SIZE)
      self.block.insert(i,putdata)
      self.checksum.insert(i,check_sum)


if __name__ == "__main__":

  RawBlocks = DiskBlocks()

  # Create server
  if len(sys.argv) < 2: 
    print("wrong number of inputs. (Please enter a single port number (i.e., 8000))\n")
    exit()
  elif len(sys.argv) == 3:
    RawBlocks.damged_block_index = int(sys.argv[2])
  
  print('check:',RawBlocks.damged_block_index)
  server = SimpleXMLRPCServer(("localhost", int(sys.argv[1])), requestHandler=RequestHandler) 
 
  


  def Get(block_number):
   
    data_block = RawBlocks.block[block_number]
    if(data_block == -1):
      print('data block is faulty it is : ',data_block) # should never happen.
      quit()
      return -1 

    new_check_sum = compute_checksum(data_block)
    prev_check_sum  = (RawBlocks.checksum[block_number])
    
    Null_check_sum = True
    if(prev_check_sum != bytearray(CHECK_SUM_SIZE)):
       # print('not null:',prev_check_sum)
        Null_check_sum = False
          

    if(Null_check_sum == True):
    # print('no prev_check sum')
      return data_block   

   
    
    if(new_check_sum != prev_check_sum):
       print(' checksum did not match!!')
       print('this is the new check sum:',new_check_sum)
       print('this is the prev check sum:',prev_check_sum)
       return -1 
    else:    
       return data_block
       
  server.register_function(Get)  
  

  def Put(block_number, data):
    
    if(data == -1):
      print('I was passed bad data:',data) # should never happen.
      quit()

    RawBlocks.block[block_number] = data
    if(block_number != RawBlocks.damged_block_index):
      checksum = compute_checksum(data)
      RawBlocks.checksum[block_number]=checksum
    else:
      print('faulty block is #:',block_number)
      RawBlocks.checksum[block_number]=0
      RawBlocks.damged_block_index = None
      
    return 0       # always passes 
  server.register_function(Put)  
    
  
  def compute_checksum(block_data):
   value_string = str(block_data)
   value_bytes = bytes(value_string, 'utf-8')
   checksum= hashlib.md5(value_bytes).hexdigest()
   #print(type(checksum))
   return checksum

  # Run the server's main loop
  server.serve_forever()

