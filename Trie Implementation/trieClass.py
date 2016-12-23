#LastName: Holligan
#FirstName: Kevin
#Email: kevin.holligan@colorado.edu
#Comments:

from __future__ import print_function
import sys

# We will use a class called my trie node
class MyTrieNode:
    # Initialize some fields 
  
    def __init__(self, isRootNode):
        #The initialization below is just a suggestion.
        #Change it as you will.
        # But do not change the signature of the constructor.
        self.isRoot = isRootNode
        self.isWordEnd = False # is this node a word ending node
        self.isRoot = False # is this a root node
        self.count = 0 # frequency count
        self.next = {} # Dictionary mapping each character from a-z to the child node
        




    def addWord(self,w):
        assert(len(w) > 0)

        # If you want to create helper/auxiliary functions, please do so.
        curNode = self
        
        #Iterate the letters in the passed string through the trie
        for letter in w:
            prevNode=curNode
            #See if the letter is in current nodes dictionary
            if(not curNode.next.get(letter)):
                #If letter is not in the dictionary, add a new node
                #and update the dictionary
                curNode = MyTrieNode(False)
                prevNode.next[letter] = curNode
            else:
                curNode = prevNode.next[letter]
            endNode = curNode
        
        #At the end of the added word, update the bool for word end
        #Increase count        
        if endNode.isWordEnd == True:
            endNode.count = endNode.count + 1
        else:
            endNode.isWordEnd = True
            endNode.count = endNode.count + 1
                
        return

    def lookupWord(self,w):
        # Return frequency of occurrence of the word w in the trie
        # returns a number for the frequency and 0 if the word w does not occur.
        curNode = self
        
        #Iterate through the passed string
        for letter in w:
            prevNode = curNode
            #If the letter is not found, return 0
            if (not curNode.next.get(letter)):
                return 0
            else:
                curNode = prevNode.next[letter]
                
        #At the end of the passed word, return the count of the word    
        return prevNode.next[letter].count
    

    def autoComplete(self,w):
        #Returns possible list of autocompletions of the word w
        #Returns a list of pairs (s,j) denoting that
        #         word s occurs with frequency j

        retList = []
        word = ""
        curNode = self
        
        #Iterate through the passed string
        for letter in w:
            prevNode = curNode
            #If the letter is not found, return an empty list
            if (not curNode.next.get(letter)):
                return retList
            else:
                #Continue incrementing and add the letter to the word to be returned
                curNode = prevNode.next[letter]
                word = word + letter

        #Test if the passed word is a word end before beginning recursion
        #If true, add it to the return list
        if curNode.isWordEnd == True:
            retList.append((word,curNode.count))
        
        #Iterate through all remaining dictionaries after initial word    
        curNode.nestedSearch(word, retList)
        
        return retList
    
    def nestedSearch(self, word, retList):
        curNode = self
        
        #Iterate the dictionary at the current level, obtain the letter and the node
        for letter, node in curNode.next.items():
            #Verify that node.next is a dictionary
            if isinstance(node.next, dict):
                #If it's a word end, add the letter to the word and add the word to the return list
                if node.isWordEnd == True:
                    newWord = word + letter
                    retList.append((newWord,node.count))
                    #Continue searching down this branch in the trie
                    curNode.next[letter].nestedSearch(newWord, retList)
                else:
                    #Increase the string
                    word = word + letter
                    #Continue searching down this branch in the trie
                    curNode.next[letter].nestedSearch(word, retList)
                    #Need to pop the last letter of the word when returning
                    #out of the trie, otherwise you end up with a superfluous letter
                    word = word[:-1]
    
                
if (__name__ == '__main__'):
    t= MyTrieNode(True)
    lst1=['test','testament','testing','ping','pin','pink','pine','pint','testing','pinetree']

    for w in lst1:
        t.addWord(w)
        
    j = t.lookupWord('testy') # should return 0
    j2 = t.lookupWord('telltale') # should return 0
    j3 = t.lookupWord ('testing') # should return 2
    
    lst3 = t.autoComplete('pi')
    print('Completions for \"pi\" are : ')
    print(lst3)
    
    lst4 = t.autoComplete('tes')
    print('Completions for \"tes\" are : ')
    print(lst4)
 
    
    
     
