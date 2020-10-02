[Merge Intervals](https://leetcode.com/problems/merge-intervals/)

##Merge Intervals
```python
def merge(self, intervals: List[List[int]]) -> List[List[int]]:
    intervals.sort()
    if (len(intervals)>1):
        i=0
        j=1
        solution=[]
        while j<len(intervals):
            if (intervals[j][0]>intervals[i][1]):
                solution.append(intervals[i])
                i=j
            else:
                if intervals[i][1]>intervals[j][1]:
                    intervals[i][1]=intervals[i][1]
                else:
                    intervals[i][1]=intervals[j][1]
            j+=1
        print(intervals[i][1])
        solution.append(intervals[i])
        j+=1 
        return(solution)
    return(intervals)```
