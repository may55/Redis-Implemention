# Documentation
This is a basic implementation of Redis with some basic functionalities
like -

**1. GET *(
[[https://redis.io/commands/get]{.underline}](https://redis.io/commands/get)
)***

**2. SET *(
[[https://redis.io/commands/set]{.underline}](https://redis.io/commands/set)
)***

**3. EXPIRE *(
[[https://redis.io/commands/expire]{.underline}](https://redis.io/commands/expire)
)***

**4. ZADD *(***
***[[https://redis.io/commands/zadd]{.underline}](https://redis.io/commands/zadd)
)***

**5. ZRANK *(***
***[[https://redis.io/commands/zrank]{.underline}](https://redis.io/commands/zrank)
)***

**6. ZRANGE *(
[[https://redis.io/commands/zrange]{.underline}](https://redis.io/commands/zrange)
)***

1.  **SET** - SET command takes a key/value pair as an input in format SET \<*key*\> "*value*" , where key and value both are treated as string data type. 
    

      a.  **Implementation -** SET command is implemented using python
        > inbuilt data structure
        > **[dictionary](https://docs.python.org/3/tutorial/datastructures.html#dictionaries).**

      b.  **Time Complexity - O(1),** in set item operation of dictionary.

2.  **GET** - GET command takes a key in format GET \<*key*\> and returns (nil) , if key doesn\'t exist in redis and returns the value of the key if it is string.
   

    a.  **Implementation -** GET command is also implemented using
        > python inbuilt data structure
        > **[dictionary](https://docs.python.org/3/tutorial/datastructures.html#dictionaries).**

    b.  **Time Complexity - O(1),** in get item operation of dictionary.

3.  **EXPIRE** - There's an expiration time for every key/value pair in the redis. By default it is initialized with 31/12/9999. With EXPIRE command that time can be overwritten with any other time. Format is EXPIRE \<*time-in-sec*\> , this makes the expiration time of the key to input time ahead of current time.
    

4.  **ZADD** - ZADD command takes a set name and one or more than one score/element pair, in format ZADD \<*setname*\> \<score1\> \<element1\> ... where data type of score is float and element is string. This returns the number of new score/value pairs added into the set ignoring the ones whose score is updated.
    

    a.  **Implementation -** ZADD command is implemented using ***a self
        > balancing binary search tree (AVL Tree)***, here order of the
        > nodes is on the basis of value of score and then value of
        > element(lexicographically). A python dictionary is also
        > maintained for every set which maps elements to its score.

    b.  **Time Complexity - *O(logn),*** where n is the number of total
        > pairs in the current set.

5.  **ZRANK** - ZRANK command takes a set name and a string element as a input in format ZRANK \<*setname*\> \<element\>, this command tell the rank/index(starting from 0) of the element in the set if the element present or a error if element not found in the input set.
    

    a.  **Implementation -** ZRANK is calculated by fetching the
        > element's score from the dictionary, and then traversing in
        > the tree to the input element and find the number of nodes
        > less than the current *(using attribute n\_count of the tree
        > node which tell number of nodes in the subtree rooted at
        > current node).*

    b.  **Time Complexity - O(logn),** where n is the number of total
        > pairs in the current set.

6.  **ZRANGE** - ZRANGE command takes a set name and a range in format ZRANK \<*setname*\> \<start\> \<end\>, these values can be negative representing the values from last and also out of range of set(handled accordingly), this command return the element string of nodes whose rank in between in input range. And with an attribute WITHSCORES in the command, also output the score of the element.
    

    a.  **Implementation -** ZRANGE is implemented by finding the
        > starting node first and then traversing in inorder within the
        > tree to get nodes till end. Traversing is done in order of
        > (*number of nodes in range)* time, by having a successor
        > attribute in every node of the tree.

    b.  **Time Complexity - O(logn+m),** where n is the number of total
        > pairs in the current set and m in the number of nodes in the
        > range.

## Persistence

Implementation is made persistent by serialising the data structure and
dump them into a file. This file is created every minute and at the end
of the execution. So when redis starts again it loads and deserializes
the data structures.

This serialisation and deserialization is done using python library
**[pickle](https://docs.python.org/3/library/pickle.html).**
