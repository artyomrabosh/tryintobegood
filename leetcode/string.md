# STRING

+ [Valid Anagram](#valid-anagram)
+ [Reverse String](#reverse-string)
+ [Reverse Vowels of a String](#reverse-vowels-of-a-string)
+ [Reverse Words in a String III](#reverse-words-in-a-string-iii)
+ [To Lower Case](#to-lower-case)
<!---->
## Valid Anagram

https://leetcode.com/problems/valid-anagram/

```python
for i in s:
    if i in letters:
        letters[i] += 1
    else:
        letters[i] = 1
for i in t:
    if i in newletters:
        newletters[i] += 1
    else:
        newletters[i] = 1
print(letters)
print(newletters)
if letters == newletters:
    return True
else:
    return False

```

## Reverse String

https://leetcode.com/problems/reverse-string/

```python

```

## Reverse Vowels of a String

https://leetcode.com/problems/reverse-vowels-of-a-string/

```python
while left < right:
    while left < right and s[left].lower() not in "aeoui":
        left += 1
    while left < right and s[right].lower() not in "aeoui":
        right -= 1
    s[left], s[right] = s[right], s[left]
    left += 1
    right -= 1
return "".join(s)

```

## Reverse Words in a String III

https://leetcode.com/problems/reverse-words-in-a-string-iii/

```python
for i in old:
    new += i[::-1]+" "
return(new[:-1])

```

## To Lower Case

https://leetcode.com/problems/to-lower-case/

```python

```

