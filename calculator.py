from collections.abc import Hashable
from collections import deque

nums_as_strs = [str(num) for num in range(10)]
ops = set("+-*/()")


def in_t_post(expression):
    all_clear = True
    if ' ' in expression:
        expr = expression.split()
    else:
        expr = list(expression)
    infix = []
    for e in expr:
        if len(e) > 1:
            try:
                test_num = int(e)
                infix.append(str(test_num))
            except ValueError:
                if '(' in e or ')' in e:
                    infix += list(e)
                elif '+' in e:
                    infix.append('+')
                elif '-' in e:
                    if len(e) % 2 == 0:
                        infix.append('+')
                    else:
                        infix.append('-')
                elif '*' in e or '/' in e:
                    print('Invalid expression')
                    all_clear = False
                else:
                    infix += e
        else:
            infix.append(e)
    stack = deque()
    postfix = deque()
    priority = {'+': 0, '-': 0, '*': 1, '/': 1}
    for c in infix:
        if c not in ops:
            postfix.append(c)
        elif len(stack) == 0 or stack[-1] == '(' or c == '(':
            stack.append(c)
        elif c == ')':
            if '(' in stack:
                temp = deque()
                popped = stack.pop()
                while popped != '(':
                    temp.append(popped)
                    popped = stack.pop()
                postfix += temp
            else:
                postfix.append('(')
        else:
            if priority[stack[-1]] < priority[c]:
                stack.append(c)
            else:
                postfix.append(stack.pop())
                if len(stack) != 0 and stack[-1] != '(':
                    if priority[stack[-1]] <= priority[c]:
                        postfix.append(stack.pop())
                stack.append(c)
    stack_copy = stack.copy()
    for _s in stack_copy:
        postfix.append(stack.pop())
    if '(' in postfix or ')' in postfix:
        pass
    else:
        if all_clear:
            return list(postfix)


def postfix_eval(p_express):
    num_stack = deque()
    for c in p_express:
        if c not in ops:
            num_stack.append(int(c))
        else:
            val2 = num_stack.pop()
            val1 = num_stack.pop()
            if c == '+':
                num_stack.append(val1 + val2)
            elif c == '-':
                num_stack.append(val1 - val2)
            elif c == '*':
                num_stack.append(val1 * val2)
            else:
                num_stack.append(val1 / val2)
    return num_stack[0]


def var_define(expression):
    str_list = expression.split('=')
    kv_list = [string.strip() for string in str_list]
    go_ahead = True
    mixed = False
    defined = True
    for num in nums_as_strs:
        if num in kv_list[0]:
            go_ahead = False
        if num in kv_list[1]:
            try:
                int(kv_list[1])
            except ValueError:
                mixed = True
    if not mixed:
        try:
            int(kv_list[1])
        except ValueError:
            if not kv_list[1] in saved_vars:
                defined = False

    if isinstance(kv_list[0], Hashable) and isinstance(kv_list[1], Hashable) and go_ahead and not mixed and defined:
        saved_vars[kv_list[0]] = kv_list[1]
    else:
        if not go_ahead or not isinstance(kv_list[0], Hashable):
            print('Invalid identifier')
        else:
            print('Invalid assignment')


def vartval(numbers):
    new_numbers = []
    for num in numbers:
        try:
            new_numbers.append(int(num))
        except ValueError:
            if num in ops:
                new_numbers.append(num)
                continue
            try:
                new_numbers.append(int(saved_vars[num]))
            except ValueError:
                new_numbers.append(int(saved_vars[saved_vars[num]]))
            except KeyError:
                print('Unknown variable')
        except KeyError:
            print('Unknown variable')
    return new_numbers


saved_vars = {}
while True:
    strs = input()
    if strs == "":
        continue
    if '/' in strs and 'e' in strs:
        if strs == "/exit":
            break
        if strs == "/help":
            print("The program calculates the value of the expression. It only accepts digits and operators. Please separate with spaces if using numbers with more than one digit.")
            continue
        else:
            print("Unknown command")
            continue
    if "=" in strs:
        var_define(strs)
        continue
    terms = in_t_post(strs)
    if terms is None:
        print('Invalid Expression')
        nums = range(10)
    else:
        nums = vartval(terms)
    if len(nums) == 1:
        print(nums[0])
        continue
    elif len(nums) == 0:
        continue
    if in_t_post(strs) is not None:
        print(int(postfix_eval(nums)))
print("Bye!")
