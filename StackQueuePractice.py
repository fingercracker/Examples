import sys

class Solution:
    # Write your code here
    def __init__(self):
        self.myQueue = []
        self.myStack = []
    def pushCharacter(self, ch):
        self.myStack.append(ch)
        return self.myStack
    def enqueueCharacter(self, ch):
        self.myQueue.append(ch)
        return self.myQueue
    def popCharacter(self):
        return self.myStack.pop()
    def dequeueCharacter(self):
        retVal = self.myQueue[0]
        self.myQueue.remove(self.myQueue[0])
        return retVal

# read the string s
s=input()
#Create the Solution class object
obj=Solution()   

l=len(s)
# push/enqueue all the characters of string s to stack
for i in range(l):
    obj.pushCharacter(s[i])
    obj.enqueueCharacter(s[i])
    
isPalindrome=True
'''
pop the top character from stack
dequeue the first character from queue
compare both the characters
''' 
for i in range(l // 2):
    if obj.popCharacter()!=obj.dequeueCharacter():
        isPalindrome=False
        break
#finally print whether string s is palindrome or not.
if isPalindrome:
    print("The word, "+s+", is a palindrome.")
else:
    print("The word, "+s+", is not a palindrome.")    
