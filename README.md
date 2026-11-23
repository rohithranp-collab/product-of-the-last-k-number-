# 1352. Product of the Last K Numbers

![Difficulty](https://img.shields.io/badge/Difficulty-Medium-orange)
![Topics](https://img.shields.io/badge/Topics-Design%20%7C%20Prefix%20Product%20%7C%20Math-blue)

## Problem Statement

Design a data structure that accepts a stream of integers and returns the product of the last `k` integers.

Implement the `ProductOfNumbers` class:

- `ProductOfNumbers()` initializes the object with an empty stream.
- `void add(int num)` appends `num` to the stream.
- `int getProduct(int k)` returns the product of the last `k` numbers in the current list. The list is guaranteed to have at least `k` numbers.

The product of any contiguous sequence of numbers always fits in a 32-bit integer.

### Example

```
Input
["ProductOfNumbers","add","add","add","add","add","getProduct","getProduct","getProduct","add","getProduct"]
[[],[3],[0],[2],[5],[4],[2],[3],[4],[8],[2]]

Output
[null,null,null,null,null,null,20,40,0,null,32]
```

### Constraints

- `0 <= num <= 100`
- `1 <= k <= 4 * 10^4`
- At most `4 * 10^4` calls will be made to `add` and `getProduct`.
- The product of the stream at any point fits in a 32-bit integer.

**Follow-up:** Can `add` and `getProduct` both run in `O(1)` time?

---

## Approach: Prefix Products with Reset on Zero

### Intuition

Just as prefix sums answer range-sum queries, **prefix products** answer range-product queries by division:

```
product(last k) = prefix[n] / prefix[n - k]
```

Zeros break this, because once a `0` enters the prefix product, every later prefix is `0` and division becomes impossible. The fix:

1. When a `0` is added, **clear the list of prefix products** (restart with `[1]`).
2. In `getProduct(k)`, if `k` is at least the size of the list, the window of the last `k` numbers must contain the most recent `0`, so the answer is `0`.
3. Otherwise, the answer is `prefix[-1] / prefix[-1 - k]`.

### Algorithm

| Operation | Logic |
|-----------|-------|
| `add(num)` | If `num == 0`, reset `prefix = [1]`. Otherwise append `prefix[-1] * num`. |
| `getProduct(k)` | If `k >= len(prefix)`, return `0`. Else return `prefix[-1] // prefix[-1 - k]`. |

### Walkthrough

Stream: `3, 0, 2, 5, 4`

| Step | add | prefix |
|------|-----|--------|
| init | | `[1]` |
| 1 | 3 | `[1, 3]` |
| 2 | 0 | `[1]` (reset) |
| 3 | 2 | `[1, 2]` |
| 4 | 5 | `[1, 2, 10]` |
| 5 | 4 | `[1, 2, 10, 40]` |

- `getProduct(2)`: `40 / 2 = 20`
- `getProduct(3)`: `40 / 1 = 40`
- `getProduct(4)`: `4 >= len(prefix) = 4`, so the answer is `0`

---

## Complexity

| | Time | Space |
|---|------|-------|
| `add` | O(1) | O(n) |
| `getProduct` | O(1) | O(n) |

---

## Solutions

### Python

```python
class ProductOfNumbers(object):

    def __init__(self):
        self.stream = []
        self.prefix = []
        self.zeros = []  # indices in self.stream where num == 0

    def add(self, num):
        """
        :type num: int
        :rtype: None
        """
        idx = len(self.stream)
        self.stream.append(num)

        if num == 0:
            self.zeros.append(idx)
            # Keep prefix non-zero so future divisions never divide by 0
            prev = self.prefix[-1] if self.prefix else 1
            self.prefix.append(prev)
        else:
            prev = self.prefix[-1] if self.prefix else 1
            self.prefix.append(prev * num)

    def getProduct(self, k):
        """
        :type k: int
        :rtype: int
        """
        n = len(self.stream)
        start = n - k

        # Check if the most recent zero falls at or after `start`
        if self.zeros and self.zeros[-1] >= start:
            return 0

        if start == 0:
            return self.prefix[-1]
        return self.prefix[-1] // self.prefix[start - 1]


## Key Takeaways

- Prefix products turn range-product queries into a single division.
- Zeros are handled by resetting the prefix list, so the division never involves `0`.
- Because `num <= 100` and the product is guaranteed to fit in 32 bits, the prefix products never overflow.

## Links


- [LeetCode Problem](https://leetcode.com/problems/product-of-the-last-k-numbers/)
