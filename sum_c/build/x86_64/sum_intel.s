	.file	"sum.c"
	.intel_syntax noprefix
	.text
	.section	.rodata.str1.1,"aMS",@progbits,1
.LC0:
	.string	"argc=%d\n"
.LC1:
	.string	"no guess entered, using %d"
.LC2:
	.string	"argv[1]=%s"
	.section	.text.startup,"ax",@progbits
	.p2align 4
	.globl	main
	.type	main, @function
main:
.LFB39:
	.cfi_startproc
	endbr64
	push	rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	mov	edx, edi
	mov	rbp, rsi
	xor	eax, eax
	push	rbx
	.cfi_def_cfa_offset 24
	.cfi_offset 3, -24
	lea	rsi, .LC0[rip]
	mov	ebx, edi
	mov	edi, 2
	sub	rsp, 8
	.cfi_def_cfa_offset 32
	call	__printf_chk@PLT
	cmp	ebx, 1
	jle	.L6
	mov	rdx, QWORD PTR 8[rbp]
	lea	rsi, .LC2[rip]
	mov	edi, 2
	xor	eax, eax
	call	__printf_chk@PLT
	mov	rdi, QWORD PTR 8[rbp]
	mov	edx, 10
	xor	esi, esi
	call	strtol@PLT
.L3:
	add	rsp, 8
	.cfi_remember_state
	.cfi_def_cfa_offset 24
	xor	eax, eax
	pop	rbx
	.cfi_def_cfa_offset 16
	pop	rbp
	.cfi_def_cfa_offset 8
	ret
.L6:
	.cfi_restore_state
	mov	edx, 10000000
	lea	rsi, .LC1[rip]
	mov	edi, 2
	xor	eax, eax
	call	__printf_chk@PLT
	jmp	.L3
	.cfi_endproc
.LFE39:
	.size	main, .-main
	.ident	"GCC: (Ubuntu 13.3.0-6ubuntu2~24.04) 13.3.0"
	.section	.note.GNU-stack,"",@progbits
	.section	.note.gnu.property,"a"
	.align 8
	.long	1f - 0f
	.long	4f - 1f
	.long	5
0:
	.string	"GNU"
1:
	.align 8
	.long	0xc0000002
	.long	3f - 2f
2:
	.long	0x3
3:
	.align 8
4:
