######################################################################################################################
#
#Social Media Analysis Tool-DEVYANSH BHANSALI
#
########################################################################################################################

import sys
import csv
choices = '''
  Menu : 
     1: Max number of friends intersection between X and Facebook among all
     2: Percentage of people with no shared friends between X and Facebook
     3: Individual information
     4: Percentage of people with more friends in X compared to Facebook
     5: The number of triangle friendships in X
     6: The number of triangle friendships on Facebook
     7: The number of triangle friendships in X and Facebook together 
       Enter any other key(s) to exit '''

def open_file(fileName):
    try:
        filePointer = open(fileName, "r", encoding="utf-8")
        return filePointer
    except:
        return None

def read_Names_data(filePointer):
    dlist=[]
    csv_reader = csv.reader(filePointer)
    for row in csv_reader:
        dlist.append(row[0].strip())
    return dlist

def read_FB_friends(filePointer):
    FB_Namelist = []    
    for line in filePointer:
        names = [name.strip() for name in line.strip().split(',') if name.strip()]
        FB_Namelist.append(names)
    return FB_Namelist

def read_X_friends(filePointer):
    X_noList = []    
    for line in filePointer:
        nos = [name.strip() for name in line.strip().split(',') if name.strip()]
        X_noList.append(nos)
    return X_noList

def fNames_from_X(dictFriends):
    X_FrndList= [dictFriends[r]['X'] for r in dictFriends.keys()]
    return X_FrndList

def fNames_from_FB(dictFriends):
    FB_FrndList= [dictFriends[r]['FB'] for r in dictFriends.keys()]
    return FB_FrndList

def sortData(my_list):
    my_list = sorted(my_list)
    for row in my_list:
        print(row)
        
def create_dict(names_list,FB_FriendsList,X_file):
    X_friendsIds = read_X_friends(X_file)
    X_friendsList= [[names_list[int(ids)] for ids in line] for line in X_friendsIds]
    friends_dict = {names_list[i]: {"X": X_friendsList[i], "FB": FB_FriendsList[i]} for i in range(len(names_list))}
    return friends_dict

def intersect_X_FB(xFriends, FbFriends):
    return max(len(set(rowFb) & set(rowx)) for rowFb, rowx in zip(FbFriends, xFriends))

def noCommon_X_FB(xFriends, FbFriends):
    cnt = sum(1 for rowFb, rowx in zip(FbFriends, xFriends) if not set(rowFb) & set(rowx))
    return (cnt / len(xFriends) * 100)

def moreIn_X(xFriends, FbFriends):
    cnt = sum(1 for rowFb, rowx in zip(FbFriends, xFriends) if len(rowx) > len(rowFb))
    return (cnt / len(xFriends) * 100)

def triangleFriends(dictt,opt):
    triFrnd = []
    for na1, k in dictt.items():
        for na2 in k[opt]:
            for na3 in k[opt]:
                if na3 not in dictt[na2][opt]:
                    continue
                if {na1, na2, na3} not in triFrnd:
                    triFrnd.append({na1, na2, na3})
    return triFrnd


def Triangle_X_FB(dictt):
    dictXFB = combine_X_FB_Friends(dictt)
    triXFB = []
    for na1, item in dictXFB.items():
        for na2 in item:
            for na3 in item:
                if na3 in dictXFB[na2] and {na1, na2, na3} not in triXFB:
                    triXFB.append({na1, na2, na3})
    return triXFB

def combine_X_FB_Friends(dictt):
    return {item: set(dictt[item]['X']) | set(dictt[item]['FB']) for item in dictt}

def main():
    while True:
        file1 = input("\nEnter a names file ~:")
        fpNames = open_file(file1)
        if fpNames:
            break
        else:
            print("Error. File does not exist")
            
    while True:
        file2 = input("\nEnter the X id file ~:")
        fpX = open_file(file2)
        if fpX:
            break
        else:
            print("Error. File does not exist")
            
    while True:
        file3 = input("\nEnter the Facebook id file ~:")
        fpFB = open_file(file3)
        if fpFB:
            break
        else:
            print("Error. File does not exist")

    listNames = read_Names_data(fpNames)
    fb_Friends = read_FB_friends(fpFB)
    dict_X_FB = create_dict(listNames, fb_Friends, fpX)
    all_X_Friends = fNames_from_X(dict_X_FB)
    all_FB_Friends = fNames_from_FB(dict_X_FB)
           
    while True:
        print(choices)
        try:
            ch = int(input("Input a choice ~:"))
        except:
            break
        if ch == 1:
            MaxIntersection = intersect_X_FB(all_X_Friends, all_FB_Friends)
            print("The Max number intersection of friends between X and Facebook is: {}".format(MaxIntersection))
        elif ch == 2:
            pNoCommon = noCommon_X_FB(all_X_Friends, all_FB_Friends)
            print("{}% of people have no friends in common on X and Facebook".format(round(pNoCommon)))
        elif ch == 3:
            while True:
                na = input("Enter a person's name ~:")
                if na in listNames:
                    print("-" * 14 + "\nFriends in X\n" + "*" * 14)
                    ind = listNames.index(na)
                    for row in sorted(all_X_Friends[ind]):
                        print(row)
                    print("-" * 20 + "\nFriends in Facebook\n" + "*" * 20)
                    for row in sorted(all_FB_Friends[ind]):
                        print(row)
                    break
                else:
                    print("Invalid name or does not exist")
                
        elif ch == 4:
            moreX = moreIn_X(all_X_Friends, all_FB_Friends)
            print("{}% of people have more friends in X compared to Facebook".format(round(moreX)))
        elif ch == 5:
            noTriX = triangleFriends(dict_X_FB, "X")
            print("The number of triangle friendships in X is: {}".format(len(noTriX)))
        elif ch == 6:
            noTriFB = triangleFriends(dict_X_FB, "FB")
            print("The number of triangle friendships in Facebook is: {}".format(len(noTriFB)))
        elif ch == 7:
            CommonXFB = Triangle_X_FB(dict_X_FB)
            print("The number of triangle friendships in X merged with Facebook is:  {}".format(len(CommonXFB)))            
        else:
            break
    print("Thank you")

if __name__ == '__main__':
    main()

