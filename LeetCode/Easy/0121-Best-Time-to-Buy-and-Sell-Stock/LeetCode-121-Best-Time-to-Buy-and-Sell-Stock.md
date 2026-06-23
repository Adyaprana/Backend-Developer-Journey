# Day 18 - LeetCode #121: Best Time to Buy and Sell Stock

## Overview

Today I solved **LeetCode #121 - Best Time to Buy and Sell Stock**.

This problem introduced me to an important interview pattern:

* Tracking Minimum Value
* Greedy Thinking
* Sliding Window / One Pass Optimization

Initially, I solved the problem using a Brute Force approach with nested loops. Although the solution was correct, it resulted in **Time Limit Exceeded (TLE)** on LeetCode.

I then learned how to optimize the solution using a single pass through the array while keeping track of:

* Lowest price seen so far
* Maximum profit seen so far

---

# Problem Statement

You are given an array:

```python
prices
```

where:

```python
prices[i]
```

represents the stock price on day `i`.

You may:

* Buy one stock once
* Sell one stock once

The sell day must come after the buy day.

Return the maximum profit possible.

If no profit is possible, return:

```python
0
```

---

# Example 1

Input:

```python
prices = [7,1,5,3,6,4]
```

Buy:

```python
1
```

Sell:

```python
6
```

Profit:

```python
6 - 1 = 5
```

Output:

```python
5
```

---

# Example 2

Input:

```python
prices = [7,6,4,3,1]
```

Prices continuously decrease.

No profitable transaction exists.

Output:

```python
0
```

---

# Constraints

```text
1 <= prices.length <= 10^5
0 <= prices[i] <= 10^4
```

---

# Approach 1: Brute Force

## Thought Process

For every possible buying day:

* Check every possible selling day after it.
* Calculate profit.
* Keep track of the largest profit found.

---

## Logic

For each index:

```python
i
```

Try selling on every index:

```python
j > i
```

Profit:

```python
prices[j] - prices[i]
```

Update maximum profit if a larger profit is found.

---

## Brute Force Code

```python
def maxProfit(prices):

    profit = 0

    for i in range(len(prices)):

        for j in range(i + 1, len(prices)):

            current_profit = prices[j] - prices[i]

            if current_profit > profit:
                profit = current_profit

    return profit
```

---

## Dry Run

Input:

```python
prices = [7,1,5,3,6,4]
```

Buy at:

```python
7
```

Check:

```python
1
5
3
6
4
```

Profits:

```python
-6
-2
-4
-1
-3
```

---

Buy at:

```python
1
```

Check:

```python
5
3
6
4
```

Profits:

```python
4
2
5
3
```

Best profit becomes:

```python
5
```

Continue checking all remaining pairs.

Final answer:

```python
5
```

---

## Complexity

Time Complexity:

```text
O(n²)
```

Space Complexity:

```text
O(1)
```

---

## Why Brute Force Fails

LeetCode allows large inputs.

If:

```text
n = 100,000
```

Then:

```text
n² = 10,000,000,000
```

operations.

This causes:

```text
Time Limit Exceeded (TLE)
```

---

# Approach 2: Optimal One-Pass Solution

## Key Insight

Instead of checking every buy-sell pair:

Ask:

```text
What is the lowest stock price seen so far?
```

and

```text
What is the maximum profit seen so far?
```

---

## Variables

### min_price

Stores the cheapest stock price encountered.

### max_profit

Stores the best profit found.

---

# Optimal Code

```python
def maxProfit(prices):

    max_profit = 0

    min_price = prices[0]

    for price in prices:

        if price < min_price:
            min_price = price

        profit = price - min_price

        if profit > max_profit:
            max_profit = profit

    return max_profit
```

---

# Dry Run

Input:

```python
prices = [7,1,5,3,6,4]
```

Start:

```python
min_price = 7
max_profit = 0
```

---

### Day 1

Price:

```python
7
```

Minimum:

```python
7
```

Profit:

```python
7 - 7 = 0
```

---

### Day 2

Price:

```python
1
```

Update minimum:

```python
min_price = 1
```

Profit:

```python
1 - 1 = 0
```

---

### Day 3

Price:

```python
5
```

Profit:

```python
5 - 1 = 4
```

Update:

```python
max_profit = 4
```

---

### Day 4

Price:

```python
3
```

Profit:

```python
3 - 1 = 2
```

No update.

---

### Day 5

Price:

```python
6
```

Profit:

```python
6 - 1 = 5
```

Update:

```python
max_profit = 5
```

---

### Day 6

Price:

```python
4
```

Profit:

```python
4 - 1 = 3
```

No update.

---

Final Answer:

```python
5
```

---

# Why This Works

At every step:

* We know the cheapest buying price so far.
* We calculate the profit if we sell today.
* We keep only the best profit.

No nested loops are needed.

---

# Example With No Profit

Input:

```python
prices = [7,6,4,3,1]
```

Minimum prices become:

```python
7
6
4
3
1
```

Profits:

```python
0
0
0
0
0
```

Maximum profit remains:

```python
0
```

Return:

```python
0
```

---

# Complexity Comparison

| Approach         | Time  | Space |
| ---------------- | ----- | ----- |
| Brute Force      | O(n²) | O(1)  |
| Optimal One Pass | O(n)  | O(1)  |

---

# Concepts Learned

During this problem I learned:

* Arrays
* Greedy Thinking
* One Pass Algorithm
* Tracking Minimum Value
* Maximum Profit Calculation
* Time Complexity Optimization
* Space Complexity Analysis

---

# Results

Problem Solved:

LeetCode #121 - Best Time to Buy and Sell Stock

Approaches Learned:

* Brute Force ✅
* One Pass Greedy Solution ✅

Status:

* Accepted on LeetCode ✅
* Passed All Test Cases ✅

---

# Reflection

The biggest lesson from this problem was:

> We do not always need to compare every possible pair.

By tracking the minimum price seen so far and the maximum profit seen so far, we can solve the entire problem in a single pass.

This reduced the complexity from:

```text
O(n²)
```

to:

```text
O(n)
```

which is a massive improvement for large inputs.
