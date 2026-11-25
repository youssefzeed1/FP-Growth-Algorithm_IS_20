from fp_tree import Node,create_header_table
def get_mining_order(items,min_support):
  frequent_items={}
  for item in items.items():
    if item[1]>=min_support:
      frequent_items[item[0]]=item[1]
  frequent_items=dict(sorted(frequent_items.items(),key=lambda x:x[1]))
  return frequent_items

def get_condational_pattern_base(item,header_table):
      cond_entries={}
      current = header_table[item]["head"]
      while current is not  None:
        list_entry=[]
        parent=current.parent
        while parent is not None and parent.item is not None :
           list_entry.append(parent.item)
           parent=parent.parent
        list_entry.reverse()
        path=tuple(list_entry)
        if path:  #this if the item is root we wont have entry for it 
          if path  not in cond_entries:
              cond_entries[path]=current.count
          else:#so if the same path happened it wont overwrite but add on it 
            cond_entries[path]+=current.count
           
        current=current.node_link
      return  cond_entries



def insert_path(root, transaction, count, header_table):
    current = root
   
    for item in transaction:  
      if item in current.children:
         child = current.children[item]
         child.count+=count
      else:
           child =Node(item,current)
           current.children[item]=child 
           child.count=count  
   
           if header_table[item]["head"] is None:  
            header_table[item]["head"]= child
            header_table[item]["tail"]= child
           else:
            header_table[item]["tail"].node_link= child 
            header_table[item]["tail"]= child
      current =child





   
def build_condational_tree(cond_entries,min_support):
  dict_items={}
  for item_tuple ,value in cond_entries.items():
      for  item in item_tuple :
        if item not in dict_items:
            dict_items[item]=value
        else:
            dict_items[item]+=value
  frequent_items=get_mining_order(dict_items,min_support)
  new_paths_filtered={}
  for item_tuple,value in cond_entries.items():
    newtuplelist=[]
    for  item in item_tuple :
        if item  in frequent_items:
           newtuplelist.append(item)
    if newtuplelist:   #if the path is empty
      newtuplelist.sort(key=lambda x: dict_items[x], reverse=True)
      path=tuple(newtuplelist)
      if path in new_paths_filtered:
        new_paths_filtered[path]+=value
      else:
         new_paths_filtered[path]=value

  root = Node(None)
  root.count = 0

  header_table = create_header_table(frequent_items, min_support)
  for path ,count in new_paths_filtered.items():
    insert_path(root,path,count,header_table)
  return root, header_table

def mining_output(header_table,minsupport,prefix=()):  #the prefix default value is to be empty so we can output the elments of level 1
   patterns={}
   iems_mining_order=get_mining_order({item:item_support["support"] for item ,item_support in header_table.items()},minsupport) #this makes a dictionary
   #from the items of header table buut just with their support and item itself and mine them ascendingly
   for item ,item_support in iems_mining_order.items():
      newpath=prefix+(item,)  #a tuple 
      patterns[newpath]=item_support
      conditional_pattern_base= get_condational_pattern_base(item, header_table)
      root,header=build_condational_tree(conditional_pattern_base,minsupport)
      if header : #the stop condations that stops if the tree becomes empty
         #the prefix new result is the new path
         patterns.update(mining_output(header,minsupport,newpath))  #this the result from recursion to append the result in a dic

   return patterns



