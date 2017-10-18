# Tutorial code from: http://materials.jeremybejarano.com/MPIwithPython/introMPI.html#hello-world

from mpi4py import MPI
rank = MPI.COMM_WORLD.Get_rank()

a = 6.0
b = 3.0

if rank == 0:
  print "Rank [%d]: %f" % (rank, a+b)
elif rank == 1:
  print "Rank [%d]: %f" % (rank, a*b)
elif rank == 2:
  print "Rank [%d]: %f" % (rank, max(a,b))
else:
  print "Unexpected rank [%d]" % rank
