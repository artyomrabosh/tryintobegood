# TREE

+ [Binary Tree Inorder Traversal](#binary-tree-inorder-traversal)
<!---->
## Binary Tree Inorder Traversal

https://leetcode.com/problems/binary-tree-inorder-traversal/

```python
if(node is None):
    return
self.traverse(node.left,order)
order.append(node.val)
self.traverse(node.right,order)
inorderTraversal(self, root: TreeNode) -> List[int]:
res=[]
self.traverse(root,res)
return res

```

