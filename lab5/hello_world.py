# Tutorial code from: http://materials.jeremybejarano.com/MPIwithPython/introMPI.html#hello-world

from mpi4py import MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()

print "Hello World -- rank [%d]" % rank
