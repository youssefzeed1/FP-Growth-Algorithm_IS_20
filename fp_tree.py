class Node:
  def __init__(self,item,parent=None):
    self.item=item
    self.count=1
    self.parent=parent
    self.children={}
    self.node_link = None  #link each node with other nodes that all have same item
    #use it to calc the support

def create_header_table(support_counter, min_sup):
    header_table = {} #containts 1 level items has >=minsupport

    for item, support in support_counter.items():
        if support >= min_sup:
          header_table[item] = {
          "support": support,
          "head": None,
          "tail": None   #these are the first appearence and last appearance of the item used to link them
          }
    return header_table

def insert_transaction(root,transaction,header_table):
  current = root

  for item in transaction:  #here if the item already exists we add the counter
    if item in current.children:
      child = current.children[item]
      child.count+=1
    else:
        child =Node(item,current)
        current.children[item]=child   #add it as new node if it doesnot exists before

        if header_table[item]["head"] is None:  #head=none means this is the first time to appear
         header_table[item]["head"]= child
         header_table[item]["tail"]= child
        else:
         header_table[item]["tail"].node_link= child  #make the last appearance to points to the new appearnce and make 
         #the last appearnce pointer as the new one as the tail
         header_table[item]["tail"]= child
    current =child

def build_tree(transactions,support_counter,min_sup):
  root=Node(None)
  root.count=0

  header_table= create_header_table(support_counter,min_sup)

  for transaction in transactions:
    insert_transaction(root,transaction,header_table)

  return root,header_table


def print_tree (node,level=0):
  for child in node.children.values():
    print("  " * level, child.item, ":", child.count)
    print_tree(child,level+1)

def print_header_table(header_table):
  for item,data in header_table.items():
    print(item," Support: ", data["support"])
    current=data["head"]
    while current is not None:
      print(current.item, ":", current.count, end=" -> ")
      current=current.node_link
    print("None")