import pandas as pd

def preprocess_data(file_path,min_sup):
    df= pd.read_excel(file_path)

    transactions=[]
    support_counter={}

    for items in df["items"]:
        transaction = {i.strip() for i in str(items).split(",")}  #this just to prevent any addational spaces  
        transactions.append(transaction)

        for item in transaction:
            if item not in support_counter:
                support_counter[item]=1
            else:
                support_counter[item]+=1

    sorted_transactions= []

    for transaction in transactions:
        filtered=[]
        for item in transaction:
            if support_counter[item]>=min_sup:
                filtered.append(item)

        filtered = sorted(filtered,key=lambda x: (-support_counter[x], x))  #to sort them descindenglt and if they are tie order them alphabaticlly
        # so -support so order them in numbers then x to order them alphabatically
        sorted_transactions.append(filtered)

    return sorted_transactions, support_counter


