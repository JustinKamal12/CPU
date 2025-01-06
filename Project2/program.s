.text
.global _start

_start:
    mov X0, 5          # Load immediate value 5 into X0
    mov X1, 10         # Load immediate value 10 into X1
    addr X2, X0, X1    # Add the values of X0 and X1, store result in X2
    addn X3, X2, 20    # Add immediate value 20 to X2, store result in X3
    mul X4, X0, X1     # Multiply X0 and X1, store result in X4
    str X3, [X4, 8]    # Store X3 at memory address X4 + 8
    ldr X5, [X4, 8]    # Load value from memory address X4 + 8 into X5
    cmp X3, X5         # Compare values in X3 and X5
    b.eq equal_label   # Branch to equal_label if X3 == X5
    b end_label        # Unconditional branch to end_label

equal_label:
    mov X6, 1          # Set X6 to 1

end_label:
    mov X7, 0          # Set X7 to 0 (program end)

.data
result: .quad 100        # Declare a memory location labeled 'result' with initial value 0
