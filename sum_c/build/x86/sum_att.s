	.file	"sum.c"
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
	leal	4(%esp), %ecx
	.cfi_def_cfa 1, 0
	andl	$-16, %esp
	pushl	-4(%ecx)
	pushl	%ebp
	movl	%esp, %ebp
	.cfi_escape 0x10,0x5,0x2,0x75,0
	pushl	%edi
	pushl	%esi
	pushl	%ebx
	.cfi_escape 0x10,0x7,0x2,0x75,0x7c
	.cfi_escape 0x10,0x6,0x2,0x75,0x78
	.cfi_escape 0x10,0x3,0x2,0x75,0x74
	call	__x86.get_pc_thunk.bx
	addl	$_GLOBAL_OFFSET_TABLE_, %ebx
	pushl	%ecx
	.cfi_escape 0xf,0x3,0x75,0x70,0x6
	subl	$12, %esp
	movl	(%ecx), %edi
	movl	4(%ecx), %esi
	pushl	%edi
	leal	.LC0@GOTOFF(%ebx), %eax
	pushl	%eax
	pushl	$2
	call	__printf_chk@PLT
	addl	$16, %esp
	cmpl	$1, %edi
	jle	.L6
	pushl	%eax
	leal	.LC2@GOTOFF(%ebx), %eax
	pushl	4(%esi)
	pushl	%eax
	pushl	$2
	call	__printf_chk@PLT
	addl	$12, %esp
	pushl	$10
	pushl	$0
	pushl	4(%esi)
	call	strtol@PLT
	addl	$16, %esp
.L3:
	leal	-16(%ebp), %esp
	xorl	%eax, %eax
	popl	%ecx
	.cfi_remember_state
	.cfi_restore 1
	.cfi_def_cfa 1, 0
	popl	%ebx
	.cfi_restore 3
	popl	%esi
	.cfi_restore 6
	popl	%edi
	.cfi_restore 7
	popl	%ebp
	.cfi_restore 5
	leal	-4(%ecx), %esp
	.cfi_def_cfa 4, 4
	ret
.L6:
	.cfi_restore_state
	leal	.LC1@GOTOFF(%ebx), %eax
	pushl	%edx
	pushl	$10000000
	pushl	%eax
	pushl	$2
	call	__printf_chk@PLT
	addl	$16, %esp
	jmp	.L3
	.cfi_endproc
.LFE39:
	.size	main, .-main
	.section	.text.__x86.get_pc_thunk.bx,"axG",@progbits,__x86.get_pc_thunk.bx,comdat
	.globl	__x86.get_pc_thunk.bx
	.hidden	__x86.get_pc_thunk.bx
	.type	__x86.get_pc_thunk.bx, @function
__x86.get_pc_thunk.bx:
.LFB40:
	.cfi_startproc
	movl	(%esp), %ebx
	ret
	.cfi_endproc
.LFE40:
	.ident	"GCC: (Ubuntu 13.3.0-6ubuntu2~24.04) 13.3.0"
	.section	.note.GNU-stack,"",@progbits
