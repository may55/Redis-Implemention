 
class ZNode(object): 
    def __init__(self, score, element): 
        self.score = score 
        self.element = element
        self.left = None
        self.right = None
        self.parent = None
        self.n_count = 1
        self.height = 1
        self.pred = None
        self.succ = None

  

class Tree(object): 

    def insert(self, root, score, element, curr_pred, curr_succ): 

        if not root:
            temp = ZNode(score, element) 
            temp.succ = curr_succ
            temp.pred = curr_pred
            if(curr_pred):
                curr_pred.succ = temp
            if(curr_succ):
                curr_succ.pred = temp
            return temp
        elif (score < root.score) or (score==root.score and element<root.element): 
            root.left = self.insert(root.left, score, element, curr_pred, root)
            if(root.left):
                root.left.parent = root
        else:
            root.right = self.insert(root.right, score, element, root, curr_succ) 
            if(root.right):
                root.right.parent = root

        # Height Update
        root.height = 1 + max(self.getHeight(root.left),
                             self.getHeight(root.right)) 

        # Node count update
        root.n_count = 1 + self.getCount(root.left) + self.getCount(root.right)

        
        balance = self.getBalance(root) 
             
        if ((balance > 1) and (score < root.left.score or (score==root.left.score and element<root.left.element))): 
            return self.rightRotate(root)

        if ((balance < -1) and (score > root.right.score or (score==root.right.score and element>root.right.element))):
            return self.leftRotate(root) 

        if ((balance > 1) and (score > root.left.score or (score==root.left.score and element>root.left.element))):
            root.left = self.leftRotate(root.left) 
            return self.rightRotate(root) 
  
        if ((balance < -1) and (score < root.right.score or (score==root.right.score and element<root.right.element))): 
            root.right = self.rightRotate(root.right) 
            return self.leftRotate(root) 
  
        return root 


    def delete(self, root, score, element, curr_pred, curr_succ):

        if not root: 
            return root 
  
        elif ((score < root.score) or (score==root.score and element<root.element)): 
            root.left = self.delete(root.left, score, element, curr_pred, root) 
            if(root.left):
                root.left.parent = root
  
        elif ((score > root.score) or (score==root.score and element>root.element)): 
            root.right = self.delete(root.right, score, element, root, curr_succ) 
            if(root.right):
                root.right.parent = root
  
        else: 
            if(root.left is None and root.right is None):
                if(root.pred):
                    root.pred.succ = root.succ
                if(root.succ):
                    root.succ.pred = root.pred
                # Node count update
                root.n_count = 1 + self.getCount(root.left) + self.getCount(root.right)
                return None

            elif root.left is None: 
                temp = root.right 
                if(root.succ):
                    root.succ.pred = root.pred
                if(root.pred):
                    root.pred.succ = root.succ
                if(temp):
                    temp.parent = root.parent
                root = None
                # Node count update
                temp.n_count = 1 + self.getCount(temp.left) + self.getCount(temp.right)
                return temp 
  
            elif root.right is None: 
                temp = root.left 
                if(temp):
                    temp.parent = root.parent
                if(root.succ):
                    root.succ.pred = root.pred
                if(root.pred):
                    root.pred.succ = root.succ
                root = None
                # Node count update
                temp.n_count = 1 + self.getCount(temp.left) + self.getCount(temp.right)
                return temp 
  
            # If have both childs
            temp = root.succ
            root.score = temp.score 
            root.element = temp.element
            root.right = self.delete(root.right, 
                                      temp.score,temp.element, root, curr_succ)
            root.n_count = 1 + self.getCount(root.left) + self.getCount(root.right)
            if(root.right):
                root.right.parent = root
  
        if root is None: 
            return root 

        # Node count update
        root.n_count = 1 + self.getCount(root.left) + self.getCount(root.right)
  
        # Height update
        root.height = 1 + max(self.getHeight(root.left), 
                            self.getHeight(root.right)) 
   
        balance = self.getBalance(root) 

        if balance > 1 and self.getBalance(root.left) >= 0: 
            return self.rightRotate(root) 
  
        if balance < -1 and self.getBalance(root.right) <= 0: 
            return self.leftRotate(root) 
  
        if balance > 1 and self.getBalance(root.left) < 0: 
            root.left = self.leftRotate(root.left) 
            return self.rightRotate(root) 

        if balance < -1 and self.getBalance(root.right) > 0: 
            root.right = self.rightRotate(root.right) 
            return self.leftRotate(root) 
  
        return root 

    # Get Information Fucntions
    def getBalance(self, root): 
        if not root: 
            return 0
  
        return self.getHeight(root.left) - self.getHeight(root.right)

    def getCount(self,root):
        if not root:
            return 0
        return root.n_count

    def getHeight(self, root): 
        if not root: 
            return 0
  
        return root.height

    def getMinValueNode(self, root): 
        if root is None or root.left is None: 
            return root 
  
        return self.getMinValueNode(root.left) 

    def getNode(self,root,start,count):
        if(root is None):
            return root
        left_count = self.getCount(root.left)
        right_count = self.getCount(root.right)
        if(start==left_count+count):
            return root
        if(start<left_count+count):
            return self.getNode(root.left,start,count)
        return self.getNode(root.right,start,count+left_count+1)

    def getRank(self, root, score, element):
        score = float(score)
        if(root is None):
            return 0
        if(score==root.score and element==root.element):
            return self.getCount(root.left)
        elif (score < root.score) or (score==root.score and element<root.element): 
            return self.getRank(root.left,score,element)
        elif (score > root.score) or (score==root.score and element>root.element):
            return self.getCount(root.left) + 1 + self.getRank(root.right,score,element)
        return -1;

    def getRange(self,root,start,end):
        start_node = self.getNode(root,start,0)
        result = []
        for i in range(start,min(end+1,root.n_count)):
            result.append(start_node)
            start_node = start_node.succ
        return result


    #Rotation Functions
    def leftRotate(self, z):
        y = z.right 
        T2 = y.left 
  
        # Perform rotation 
        y.left = z 
        z.right = T2 
  
        y.parent = z.parent
        z.parent = y
        if(T2):
            T2.parent = z

        # Count update
        z.n_count = 1 + self.getCount(z.left) + self.getCount(z.right)
        y.n_count = 1 + self.getCount(y.left) + self.getCount(y.right)

        # Update heights 
        z.height = 1 + max(self.getHeight(z.left), 
                         self.getHeight(z.right)) 
        y.height = 1 + max(self.getHeight(y.left), 
                         self.getHeight(y.right)) 
        # Return the new root 
        return y 
  
    def rightRotate(self, z): 
  
        y = z.left 
        T3 = y.right 
  
        y.right = z 
        z.left = T3 
  
        y.parent = z.parent
        z.parent = y
        if(T3):
            T3.parent = z


        # Count update
        z.n_count = 1 + self.getCount(z.left) + self.getCount(z.right)
        y.n_count = 1 + self.getCount(y.left) + self.getCount(y.right)

        # Height update
        z.height = 1 + max(self.getHeight(z.left), 
                        self.getHeight(z.right)) 
        y.height = 1 + max(self.getHeight(y.left), 
                        self.getHeight(y.right)) 
  
        # return new root
        return y 

  
    # Traversal Functions
    def inOrder(self,root):
        if not root:
            return

        self.inOrder(root.left)
            
        print("Score: {0}, ".format(root.score),end="")
        if(root.left):
            print("Left: {0}, ".format(root.left.score),end="")
        if(root.right):
            print("Right: {0}, ".format(root.right.score),end="")
        if(root.parent):
            print("Parent: {0}, ".format(root.parent.score),end="")
        print("Node Count: {0}, ".format(root.n_count),end="")
        print("Height: {0}, ".format(root.height),end="")
        if(root.pred):
            print("Predecessor: {0}, ".format(root.pred.score),end="")
        if(root.succ):
            print("Succecessor: {0}, ".format(root.succ.score),end="")
        print()
        self.inOrder(root.right)

    
  

# Procedure for avl test
# if __name__=='__main__':


#     # Driver program to test above function 

#     myTree = Tree() 
#     root = None

#     root = myTree.insert(root,0,"element",None,None)
#     root = myTree.insert(root,1,"element",None,None)
#     root = myTree.insert(root,2,"element",None,None)
#     root = myTree.insert(root,3,"element",None,None)
#     root = myTree.insert(root,4,"element",None,None)
#     root = myTree.insert(root,5,"element",None,None)
#     root = myTree.insert(root,6,"element",None,None)





#     while(True):
#         print("1. Insert, 2.Delete, 3.Inorder, 4. Exit")
#         cmd = int(input())
#         if cmd==1:
#             score = int(input("Score: "))
#             element = input("Element: ")
#             root = myTree.insert(root,score,element,None,None)
#         elif cmd==2:
#             score = int(input("Score: "))
#             element = input("Element: ")
#             root = myTree.delete(root,score,element,None,None)
#         elif cmd==3:
#             myTree.inOrder(root)
#             print()
#         else:
#             break

