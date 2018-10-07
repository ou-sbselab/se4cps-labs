# Source from https://rabernat.github.io/research_computing/parallel-programming-with-mpi-for-python.html

from mpi4py import MPI
import numpy as np

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

# Create  an NP array for each process
value = np.array(rank, 'd')
print 'Rank: ', rank, ' value= ', value

# Initialize arrays
value_sum = np.array(0.0, 'd')
value_max = np.array(0.0, 'd')

# Perform reduce operations
comm.Reduce(value, value_sum, op=MPI.SUM, root=0)
comm.Reduce(value, value_max, op=MPI.MAX, root=0)

# Rank 0 aggregates
if rank == 0:
  print 'Rank 0: value_sum = ', value_sum
  print 'Rank 0: value_max = ', value_max

