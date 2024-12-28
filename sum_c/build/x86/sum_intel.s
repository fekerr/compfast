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
	lea	ecx, 4[esp]
	.cfi_def_cfa 1, 0
	and	esp, -16
	push	DWORD PTR -4[ecx]
	push	ebp
	mov	ebp, esp
	.cfi_escape 0x10,0x5,0x2,0x75,0
	push	edi
	push	esi
	push	ebx
	.cfi_escape 0x10,0x7,0x2,0x75,0x7c
	.cfi_escape 0x10,0x6,0x2,0x75,0x78
	.cfi_escape 0x10,0x3,0x2,0x75,0x74
	call	__x86.get_pc_thunk.bx
	add	ebx, OFFSET FLAT:_GLOBAL_OFFSET_TABLE_
	push	ecx
	.cfi_escape 0xf,0x3,0x75,0x70,0x6
	sub	esp, 12
	mov	edi, DWORD PTR [ecx]
	mov	esi, DWORD PTR 4[ecx]
	push	edi
	lea	eax, .LC0@GOTOFF[ebx]
	push	eax
	push	2
	call	__printf_chk@PLT
	add	esp, 16
	cmp	edi, 1
	jle	.L6
	push	eax
	lea	eax, .LC2@GOTOFF[ebx]
	push	DWORD PTR 4[esi]
	push	eax
	push	2
	call	__printf_chk@PLT
	add	esp, 12
	push	10
	push	0
	push	DWORD PTR 4[esi]
	call	strtol@PLT
	add	esp, 16
.L3:
	lea	esp, -16[ebp]
	xor	eax, eax
	pop	ecx
	.cfi_remember_state
	.cfi_restore 1
	.cfi_def_cfa 1, 0
	pop	ebx
	.cfi_restore 3
	pop	esi
	.cfi_restore 6
	pop	edi
	.cfi_restore 7
	pop	ebp
	.cfi_restore 5
	lea	esp, -4[ecx]
	.cfi_def_cfa 4, 4
	ret
.L6:
	.cfi_restore_state
	lea	eax, .LC1@GOTOFF[ebx]
	push	edx
	push	10000000
	push	eax
	push	2
	call	__printf_chk@PLT
	add	esp, 16
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
	mov	ebx, DWORD PTR [esp]
	ret
	.cfi_endproc
.LFE40:
	.ident	"GCC: (Ubuntu 13.3.0-6ubuntu2~24.04) 13.3.0"
	.section	.note.GNU-stack,"",@progbits
