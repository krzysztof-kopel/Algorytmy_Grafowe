class Node:
  def __init__(self, idx):
    self.idx = idx
    self.out = set()
    self.color = None

  def connect_to(self, v):
    self.out.add(v)
