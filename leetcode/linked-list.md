

##Reverse Linked List

https://leetcode.com/problems/reverse-linked-list/
```python
def reverseList(self, head: ListNode) -> ListNode:
    prev, new = head, None
    while prev:
       new = ListNode(prev.val, new)
       prev = prev.next
    return new

```


##Middle of the Linked List

https://leetcode.com/problems/middle-of-the-linked-list/
```python
def middleNode(self, head: ListNode) -> ListNode:
    if(head.next is None):
        return head
    next = head.next
    double_next = head.next.next
    while double_next is not None and double_next.next is not None:
        double_next = double_next.next.next
        next = next.next
    return (next)

```


##Merge Two Sorted Lists

https://leetcode.com/problems/merge-two-sorted-lists/
```python
def mergeTwoLists(self, l1: ListNode, l2: ListNode) -> ListNode:
    reversed = None
    while(l1 is not None or l2 is not None):
        if(l1 is None):
            reversed = ListNode(l2.val, reversed)
            l2 = l2.next
        elif(l2 is None):
            reversed = ListNode(l1.val, reversed)
            l1 = l1.next
        else:
            if(l1.val >= l2.val):
                reversed = ListNode(l2.val, reversed)
                l2 = l2.next
            else:
                reversed = ListNode(l1.val, reversed)
                l1 = l1.next
    Merged is None
    while (reversed):
       Merged = ListNode(reversed.val, Merged)
       reversed = reversed.next
    return (Merged)

```


##Palindrome Linked List

https://leetcode.com/problems/palindrome-linked-list/
```python    
def isPalindrome(self, head: ListNode) -> bool:
    if(head is None or head.next is None):
        return True
    next = head.next
    double_next = head.next.next
    while double_next is not None and double_next.next is not None:
        double_next = double_next.next.next
        next = next.next
    q = None

    while next:
       q = ListNode(next.val, q)
       next = next.next
    print(q)
    print(head)
    if(q.next is None):
        if(q.val == head.val):
            return True
        else:
            return False
    while(q is not None):
        if(head.val != q.val):
            return(False)
        head = head.next
        q = q.next
    return(True)

```


##Remove Nth Node From End of List

https://leetcode.com/problems/remove-nth-node-from-end-of-list/
```python
def removeNthFromEnd(self, head: ListNode, n: int) -> ListNode:
    if (head.next is None and n == 1):
        return None
    counter = 1
    len = 0
    len_head = head
    while len_head:
        len += 1
        len_head = len_head.next
    n = len-n
    if(n == 0):
        return head.next
    first = head
    second = head.next
    while (counter < n):
        first = first.next
        second = second.next
        counter += 1
    first.next = second.next
    return head

```
