#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: young
# date: 2019/11/19
from data_structure.node import Node


class LinkedList:
    def __init__(self, head=None, tail=None):
        self.head = Node(head) if head is not None else None
        self.tail = Node(tail) if tail is not None else self.head

    def __str__(self):
        values, cur = [], self.head
        while cur:
            values.append(cur.data)
            cur = cur.next
        return ' -> '.join(map(str, values))

    def __eq__(self, other_list):
        cur, compare = self.head, other_list.head
        while cur and compare:
            if cur.data != compare.data:
                return False
            cur, compare = cur.next, compare.next
        if cur or compare:
            return False
        return True

    def values_to_end(self, cur=None):
        values, cur = [], cur or self.head
        while cur:
            values.append(cur.data)
            cur = cur.next
        return values

    def insert(self, node_data):
        node = Node(node_data)
        if not self.head:
            self.head = node
        else:
            self.tail.next = node
        self.tail = node
        return self

    def insert_head(self, node_data):
        node = Node(node_data, self.head)
        self.head = node
        self.tail = self.tail or node
        return self

    def insert_at_position(self, node_data, pos):
        assert pos >= 0, 'position need >= 0'
        num, cur = 0, self.head
        while num != pos and cur:
            num += 1
            cur = cur.next
        if cur:
            new = Node(cur.data)
            new.next, cur.next, cur.data = cur.next, new, node_data
            if self.tail == cur:
                self.tail = new
        else:
            new = Node(node_data)
            if not self.head:
                self.head = self.tail = new
            else:
                self.tail.next = new
                self.tail = new
        return self

    def delete(self, pos=None):
        assert self.head, 'list not has item'
        if pos is None:
            if self.head == self.tail:
                item = self.tail
                self.head = self.tail = None
            else:
                cur = self.head
                while cur.next != self.tail:
                    cur = cur.next
                item = self.tail
                cur.next = None
                self.tail = cur
        elif pos == 0:
            if self.head == self.tail:
                self.tail = None
            item = self.head
            self.head = item.next
        else:
            cur, num = self.head, 1
            while pos > num:
                if not cur.next:
                    return None
                cur = cur.next
                num += 1
            item = cur.next
            if item:
                cur.next = item.next
            else:
                return None
        data = item.data
        del item
        return data

    def reverse(self):
        origin, tmp, new = self.head, self.head, None
        self.head, self.tail = self.tail, self.head
        while origin:
            origin, tmp.next = origin.next, new
            tmp, new = origin, tmp
        return self

    def sort(self):
        if self.head is None:
            return None
        values, cur = [], self.head
        while cur:
            values.append(cur.data)
            cur = cur.next
        cur = self.head
        for value in sorted(values):
            cur.data = value
            cur = cur.next
        return self

    def merge_sorted(self, other_list):
        if not other_list:
            return self
        sentry = cur = Node(0)
        first, second = self.head, other_list.head
        while first and second:
            if second.data > first.data:
                cur.next, cur, first = first, first, first.next
            else:
                cur.next, cur, second = second, second, second.next
        self.head = sentry.next
        cur.next = first if first else second
        while cur.next:
            cur = cur.next
        self.tail = cur
        return self

    def delete_sorted_duplicate(self):
        if self.head is None:
            return self
        pre, behind = self.head, self.head.next
        while behind:
            if pre.data == behind.data:
                behind = pre.next = behind.next
            else:
                pre, behind = behind, behind.next
        self.tail = pre
        return self

    def has_cycle(self):
        fast = slow = self.head
        while fast.next and fast.next.next:
            fast, slow = fast.next.next, slow.next
            if fast.real_equal(slow):
                return True
        else:
            return False

    def merge_point(self, other_list):
        length1 = length2 = 0
        move = self.head
        while move:
            move = move.next
            length1 += 1
        move = other_list.head
        while move:
            move = move.next
            length2 += 1
        move1, move2 = self.head, other_list.head
        if length1 > length2:
            while length2 != length1:
                move1 = move1.next
                length1 -= 1
        else:
            while length2 != length1:
                move2 = move2.next
                length2 -= 1
        while move1.data != move2.data:
            move1, move2 = move1.next, move2.next
        return move1.data


if __name__ == '__main__':
    linked = LinkedList(1)
    for i in range(2, 9):
        linked.insert(i)
    assert str(linked) == '1 -> 2 -> 3 -> 4 -> 5 -> 6 -> 7 -> 8'
    linked.insert_head(0)
    assert linked.values_to_end() == list(range(9))
    assert (linked.head.data, linked.tail.data) == (0, 8)

    linked.delete()
    assert str(linked) == '0 -> 1 -> 2 -> 3 -> 4 -> 5 -> 6 -> 7'
    linked.delete(pos=7)
    assert str(linked) == '0 -> 1 -> 2 -> 3 -> 4 -> 5 -> 6'
    linked.delete(pos=7)
    assert str(linked) == '0 -> 1 -> 2 -> 3 -> 4 -> 5 -> 6'
    del linked
    linked = LinkedList(1)
    linked.delete()
    assert str(linked) == ''
    linked = LinkedList()
    for i in range(2):
        linked.insert(i)
    linked.delete(pos=0)
    assert str(linked) == '1'
    linked.delete(pos=0)
    assert str(linked) == ''

    linked.insert_at_position(0, 1)
    assert str(linked) == '0'
    linked.insert_at_position(2, 1)
    assert str(linked) == '0 -> 2'
    linked.insert_at_position(1, 1)
    assert str(linked) == '0 -> 1 -> 2'

    linked = linked.reverse()
    assert str(linked) == '2 -> 1 -> 0'
    other = LinkedList(2)
    assert linked != other
    for i in range(1, -1, -1):
        other.insert(i)
    assert linked == other
    other.tail.data = 1
    assert linked != other

    linked.sort()
    assert str(linked) == '0 -> 1 -> 2'
    other.insert_head(9)
    linked.merge_sorted(other.sort())
    assert str(linked) == '0 -> 1 -> 1 -> 1 -> 2 -> 2 -> 9'
    assert (linked.head.data, linked.tail.data) == (0, 9)
    other = LinkedList(4)
    other.tail.next = linked.head.next.next.next.next
    assert linked.merge_point(other) == 2
    other.tail.next = linked.head.next.next.next
    assert linked.merge_point(other) == 1

    linked.insert(9)
    assert linked.has_cycle() is False
    linked.delete_sorted_duplicate()
    assert str(linked) == '0 -> 1 -> 2 -> 9'
    assert (linked.head.data, linked.tail.data) == (0, 9)
    sentry = linked.head.next.next
    linked.tail.next = sentry
    assert linked.has_cycle() is True
    linked.tail.next = None


