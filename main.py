from preprocessing import preprocess_data
from fp_tree import build_tree,print_tree,print_header_table
from fp_mining  import mining_output
from generating_rules_conf import generate_association_rules


min_sup=2
min_conf=0.7
file_path= "Horizontal_Format.xlsx"

sorted_transactions,support_counter=preprocess_data(file_path,min_sup)

print("Sorted Transactions: ")
for t in sorted_transactions:
   print(t)

print("\nSupport Counter:")
print(support_counter)

root,header_table= build_tree(sorted_transactions,support_counter,min_sup)
print("\nFP_Tree:")
print_tree(root)
print("\nHeader_Table:")
print_header_table(header_table)
print("\nthe mining output\n")
frequent_items=mining_output(header_table,min_sup,prefix=())
print(frequent_items)
print()
rules=generate_association_rules(frequent_items,len(sorted_transactions),min_conf)
for rule in rules:
    print(f"{rule['rule']} ||  conf:{rule['confidence']} || lift: {rule['lift']} || strength: {rule['strength']}")

