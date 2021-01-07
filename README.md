# Network Supported RAID5 Storage System: 
Developed a python model of a network UNIX filesystem. This model was divided into a client and servers which provided redundant block storage for the client. The model provides an equal distribution of load (data from client) across servers, and is fault tolerant.
## Goal
The goal of this project is to create a network file system that is tolerant to two types of failuers which are soft and hard failuers. Soft failuers occur when data in a storage system statrs to decay and some kind of a masking process can correct the fault bits and a hard failuer occurs when the entire server goes down. 
## Client/Servers
In this project, a modle of a UNIX file system that contains  (inode tables - path and name reslover - unix commands) is created in python. Also an I/O controller (Disk controller) to store data on a moduled disk is used. The main goal is for the client to issue requsts from a server over a network using [RPC](https://en.wikipedia.org/wiki/Remote_procedure_call) the client uses the servers as a reliable storage system.      

## Redundancy 
The storage system uses a [RAID5](https://searchstorage.techtarget.com/definition/RAID-5-redundant-array-of-independent-disks#:~:text=RAID%205%20is%20a%20redundant,case%20of%20a%20disk%20failure.) module to insure the integrity of the data and correct any corrupted data. The error detection 
is done by keeping a checksum on the server side and compaing the checksum to the actual data on a read request from the client. If the data is corrupted, parity blocks are read and used to obtain back the actual (correct) data via an Xoring operation. 
In case a server failed, that servers data is obtained using the remaning servers and the parity blocks that are part of the RAI5 storage system. 
 
## Virtualizing Storage 
The client is not aware of the multipule server; thus, a mapping between a virtual address (issued by client) and a physicall address (used by the server) is implemented in software. After choosing the correct server, the RPC mechanisim is induced and data is transfered to correct address. 

