#include <stdio.h>
#include <stdlib.h>

typedef struct Node {
    int data;
    struct Node *next;
} Node;

Node* create_list(int size) {
    Node *head = NULL, *temp = NULL, *prev = NULL;
    for (int i = 0; i < size; i++) {
        temp = (Node*)malloc(sizeof(Node));
        temp->data = rand() % 1000;
        temp->next = NULL;
        if (prev != NULL) {
            prev->next = temp;
        } else {
            head = temp;
        }
        prev = temp;
    }
    return head;
}

void traverse_list(Node *head) {
    Node *temp = head;
    long sum = 0;
    while (temp != NULL) {
        sum += temp->data;
        temp = temp->next;
    }
    printf("Sum: %ld\n", sum);
}

int main() {
    Node *head = create_list(10000);
    traverse_list(head);
    return 0;
}
