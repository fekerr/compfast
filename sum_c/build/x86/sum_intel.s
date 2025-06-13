	.file	"sum.c"
	.intel_syntax noprefix
# GNU C17 (Ubuntu 13.3.0-6ubuntu2~24.04) version 13.3.0 (x86_64-linux-gnu)
#	compiled by GNU C version 13.3.0, GMP version 6.3.0, MPFR version 4.2.1, MPC version 1.3.1, isl version isl-0.26-GMP

# GGC heuristics: --param ggc-min-expand=100 --param ggc-min-heapsize=131072
# options passed: -masm=intel -m32 -mtune=generic -march=i686 -g -fasynchronous-unwind-tables -fstack-protector-strong -fstack-clash-protection
	.text
.Ltext0:
	.file 0 "/home/fekerr/src/compfast/sum_c" "sum.c"
	.section	.rodata
.LC0:
	.string	"argc=%d\n"
.LC1:
	.string	"no guess entered, using %d"
.LC2:
	.string	"argv[1]=%s"
	.text
	.globl	main
	.type	main, @function
main:
.LFB6:
	.file 1 "sum.c"
	.loc 1 9 33
	.cfi_startproc
	lea	ecx, 4[esp]	#,
	.cfi_def_cfa 1, 0
	and	esp, -16	#,
	push	DWORD PTR -4[ecx]	#
	push	ebp	#
	mov	ebp, esp	#,
	.cfi_escape 0x10,0x5,0x2,0x75,0
	push	esi	#
	push	ebx	#
	push	ecx	#
	.cfi_escape 0xf,0x3,0x75,0x74,0x6
	.cfi_escape 0x10,0x6,0x2,0x75,0x7c
	.cfi_escape 0x10,0x3,0x2,0x75,0x78
	sub	esp, 28	#,
	call	__x86.get_pc_thunk.bx	#
	add	ebx, OFFSET FLAT:_GLOBAL_OFFSET_TABLE_	# tmp82,
	mov	esi, ecx	# tmp98,
# sum.c:11:     int NUMBER = GUESS, i, s;
	.loc 1 11 9
	mov	DWORD PTR -36[ebp], 10000000	# NUMBER,
# sum.c:12:     printf("argc=%d\n", argc);
	.loc 1 12 5
	sub	esp, 8	#,
	push	DWORD PTR [esi]	# argc
	lea	eax, .LC0@GOTOFF[ebx]	# tmp89,
	push	eax	# tmp89
	call	printf@PLT	#
	add	esp, 16	#,
# sum.c:13:     if (argc < 2) {
	.loc 1 13 8
	cmp	DWORD PTR [esi], 1	# argc,
	jg	.L2	#,
# sum.c:14:         printf("no guess entered, using %d", NUMBER);
	.loc 1 14 9
	sub	esp, 8	#,
	push	DWORD PTR -36[ebp]	# NUMBER
	lea	eax, .LC1@GOTOFF[ebx]	# tmp90,
	push	eax	# tmp90
	call	printf@PLT	#
	add	esp, 16	#,
	jmp	.L3	#
.L2:
# sum.c:17:         printf("argv[1]=%s", argv[1]);
	.loc 1 17 34
	mov	eax, DWORD PTR 4[esi]	# tmp91, argv
	add	eax, 4	# _1,
# sum.c:17:         printf("argv[1]=%s", argv[1]);
	.loc 1 17 9
	mov	eax, DWORD PTR [eax]	# _2, *_1
	sub	esp, 8	#,
	push	eax	# _2
	lea	eax, .LC2@GOTOFF[ebx]	# tmp92,
	push	eax	# tmp92
	call	printf@PLT	#
	add	esp, 16	#,
# sum.c:18:         NUMBER = atoi(argv[1]);
	.loc 1 18 27
	mov	eax, DWORD PTR 4[esi]	# tmp93, argv
	add	eax, 4	# _3,
# sum.c:18:         NUMBER = atoi(argv[1]);
	.loc 1 18 18
	mov	eax, DWORD PTR [eax]	# _4, *_3
	sub	esp, 12	#,
	push	eax	# _4
	call	atoi@PLT	#
	add	esp, 16	#,
	mov	DWORD PTR -36[ebp], eax	# NUMBER, tmp94
.L3:
# sum.c:22:     for (s = i = 0; i < NUMBER; ++i) {
	.loc 1 22 16
	mov	DWORD PTR -32[ebp], 0	# i,
# sum.c:22:     for (s = i = 0; i < NUMBER; ++i) {
	.loc 1 22 12
	mov	eax, DWORD PTR -32[ebp]	# tmp95, i
	mov	DWORD PTR -28[ebp], eax	# s, tmp95
# sum.c:22:     for (s = i = 0; i < NUMBER; ++i) {
	.loc 1 22 5
	jmp	.L4	#
.L5:
# sum.c:23:         s += 1;  // Increment sum
	.loc 1 23 11
	add	DWORD PTR -28[ebp], 1	# s,
# sum.c:22:     for (s = i = 0; i < NUMBER; ++i) {
	.loc 1 22 33 discriminator 3
	add	DWORD PTR -32[ebp], 1	# i,
.L4:
# sum.c:22:     for (s = i = 0; i < NUMBER; ++i) {
	.loc 1 22 23 discriminator 1
	mov	eax, DWORD PTR -32[ebp]	# tmp96, i
	cmp	eax, DWORD PTR -36[ebp]	# tmp96, NUMBER
	jl	.L5	#,
# sum.c:27:     return 0;
	.loc 1 27 12
	mov	eax, 0	# _19,
# sum.c:28: }
	.loc 1 28 1
	lea	esp, -12[ebp]	#,
	pop	ecx	#
	.cfi_restore 1
	.cfi_def_cfa 1, 0
	pop	ebx	#
	.cfi_restore 3
	pop	esi	#
	.cfi_restore 6
	pop	ebp	#
	.cfi_restore 5
	lea	esp, -4[ecx]	#,
	.cfi_def_cfa 4, 4
	ret
	.cfi_endproc
.LFE6:
	.size	main, .-main
	.section	.text.__x86.get_pc_thunk.bx,"axG",@progbits,__x86.get_pc_thunk.bx,comdat
	.globl	__x86.get_pc_thunk.bx
	.hidden	__x86.get_pc_thunk.bx
	.type	__x86.get_pc_thunk.bx, @function
__x86.get_pc_thunk.bx:
.LFB7:
	.cfi_startproc
	mov	ebx, DWORD PTR [esp]	#,
	ret
	.cfi_endproc
.LFE7:
	.text
.Letext0:
	.file 2 "/usr/include/stdlib.h"
	.file 3 "/usr/include/stdio.h"
	.section	.debug_info,"",@progbits
.Ldebug_info0:
	.long	0x10c
	.value	0x5
	.byte	0x1
	.byte	0x4
	.long	.Ldebug_abbrev0
	.uleb128 0x6
	.long	.LASF17
	.byte	0x1d
	.long	.LASF0
	.long	.LASF1
	.long	.Ltext0
	.long	.Letext0-.Ltext0
	.long	.Ldebug_line0
	.uleb128 0x1
	.byte	0x4
	.byte	0x7
	.long	.LASF2
	.uleb128 0x1
	.byte	0x4
	.byte	0x5
	.long	.LASF3
	.uleb128 0x7
	.byte	0x4
	.byte	0x5
	.string	"int"
	.uleb128 0x1
	.byte	0x8
	.byte	0x5
	.long	.LASF4
	.uleb128 0x1
	.byte	0x1
	.byte	0x8
	.long	.LASF5
	.uleb128 0x1
	.byte	0x2
	.byte	0x7
	.long	.LASF6
	.uleb128 0x1
	.byte	0x4
	.byte	0x7
	.long	.LASF7
	.uleb128 0x1
	.byte	0x1
	.byte	0x6
	.long	.LASF8
	.uleb128 0x1
	.byte	0x2
	.byte	0x5
	.long	.LASF9
	.uleb128 0x1
	.byte	0x8
	.byte	0x7
	.long	.LASF10
	.uleb128 0x2
	.long	0x71
	.uleb128 0x1
	.byte	0x1
	.byte	0x6
	.long	.LASF11
	.uleb128 0x8
	.long	0x71
	.uleb128 0x2
	.long	0x78
	.uleb128 0x9
	.long	.LASF12
	.byte	0x2
	.byte	0x69
	.byte	0xc
	.long	0x34
	.long	0x98
	.uleb128 0x3
	.long	0x7d
	.byte	0
	.uleb128 0xa
	.long	.LASF13
	.byte	0x3
	.value	0x16b
	.byte	0xc
	.long	0x34
	.long	0xb0
	.uleb128 0x3
	.long	0x7d
	.uleb128 0xb
	.byte	0
	.uleb128 0xc
	.long	.LASF18
	.byte	0x1
	.byte	0x9
	.byte	0x5
	.long	0x34
	.long	.LFB6
	.long	.LFE6-.LFB6
	.uleb128 0x1
	.byte	0x9c
	.long	0x10a
	.uleb128 0x4
	.long	.LASF14
	.byte	0xe
	.long	0x34
	.uleb128 0x2
	.byte	0x91
	.sleb128 0
	.uleb128 0x4
	.long	.LASF15
	.byte	0x1b
	.long	0x10a
	.uleb128 0x2
	.byte	0x91
	.sleb128 4
	.uleb128 0xd
	.long	.LASF16
	.byte	0x1
	.byte	0xb
	.byte	0x9
	.long	0x34
	.uleb128 0x2
	.byte	0x75
	.sleb128 -36
	.uleb128 0x5
	.string	"i"
	.byte	0x19
	.long	0x34
	.uleb128 0x2
	.byte	0x75
	.sleb128 -32
	.uleb128 0x5
	.string	"s"
	.byte	0x1c
	.long	0x34
	.uleb128 0x2
	.byte	0x75
	.sleb128 -28
	.byte	0
	.uleb128 0x2
	.long	0x6c
	.byte	0
	.section	.debug_abbrev,"",@progbits
.Ldebug_abbrev0:
	.uleb128 0x1
	.uleb128 0x24
	.byte	0
	.uleb128 0xb
	.uleb128 0xb
	.uleb128 0x3e
	.uleb128 0xb
	.uleb128 0x3
	.uleb128 0xe
	.byte	0
	.byte	0
	.uleb128 0x2
	.uleb128 0xf
	.byte	0
	.uleb128 0xb
	.uleb128 0x21
	.sleb128 4
	.uleb128 0x49
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x3
	.uleb128 0x5
	.byte	0
	.uleb128 0x49
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x4
	.uleb128 0x5
	.byte	0
	.uleb128 0x3
	.uleb128 0xe
	.uleb128 0x3a
	.uleb128 0x21
	.sleb128 1
	.uleb128 0x3b
	.uleb128 0x21
	.sleb128 9
	.uleb128 0x39
	.uleb128 0xb
	.uleb128 0x49
	.uleb128 0x13
	.uleb128 0x2
	.uleb128 0x18
	.byte	0
	.byte	0
	.uleb128 0x5
	.uleb128 0x34
	.byte	0
	.uleb128 0x3
	.uleb128 0x8
	.uleb128 0x3a
	.uleb128 0x21
	.sleb128 1
	.uleb128 0x3b
	.uleb128 0x21
	.sleb128 11
	.uleb128 0x39
	.uleb128 0xb
	.uleb128 0x49
	.uleb128 0x13
	.uleb128 0x2
	.uleb128 0x18
	.byte	0
	.byte	0
	.uleb128 0x6
	.uleb128 0x11
	.byte	0x1
	.uleb128 0x25
	.uleb128 0xe
	.uleb128 0x13
	.uleb128 0xb
	.uleb128 0x3
	.uleb128 0x1f
	.uleb128 0x1b
	.uleb128 0x1f
	.uleb128 0x11
	.uleb128 0x1
	.uleb128 0x12
	.uleb128 0x6
	.uleb128 0x10
	.uleb128 0x17
	.byte	0
	.byte	0
	.uleb128 0x7
	.uleb128 0x24
	.byte	0
	.uleb128 0xb
	.uleb128 0xb
	.uleb128 0x3e
	.uleb128 0xb
	.uleb128 0x3
	.uleb128 0x8
	.byte	0
	.byte	0
	.uleb128 0x8
	.uleb128 0x26
	.byte	0
	.uleb128 0x49
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x9
	.uleb128 0x2e
	.byte	0x1
	.uleb128 0x3f
	.uleb128 0x19
	.uleb128 0x3
	.uleb128 0xe
	.uleb128 0x3a
	.uleb128 0xb
	.uleb128 0x3b
	.uleb128 0xb
	.uleb128 0x39
	.uleb128 0xb
	.uleb128 0x27
	.uleb128 0x19
	.uleb128 0x49
	.uleb128 0x13
	.uleb128 0x3c
	.uleb128 0x19
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0xa
	.uleb128 0x2e
	.byte	0x1
	.uleb128 0x3f
	.uleb128 0x19
	.uleb128 0x3
	.uleb128 0xe
	.uleb128 0x3a
	.uleb128 0xb
	.uleb128 0x3b
	.uleb128 0x5
	.uleb128 0x39
	.uleb128 0xb
	.uleb128 0x27
	.uleb128 0x19
	.uleb128 0x49
	.uleb128 0x13
	.uleb128 0x3c
	.uleb128 0x19
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0xb
	.uleb128 0x18
	.byte	0
	.byte	0
	.byte	0
	.uleb128 0xc
	.uleb128 0x2e
	.byte	0x1
	.uleb128 0x3f
	.uleb128 0x19
	.uleb128 0x3
	.uleb128 0xe
	.uleb128 0x3a
	.uleb128 0xb
	.uleb128 0x3b
	.uleb128 0xb
	.uleb128 0x39
	.uleb128 0xb
	.uleb128 0x27
	.uleb128 0x19
	.uleb128 0x49
	.uleb128 0x13
	.uleb128 0x11
	.uleb128 0x1
	.uleb128 0x12
	.uleb128 0x6
	.uleb128 0x40
	.uleb128 0x18
	.uleb128 0x7c
	.uleb128 0x19
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0xd
	.uleb128 0x34
	.byte	0
	.uleb128 0x3
	.uleb128 0xe
	.uleb128 0x3a
	.uleb128 0xb
	.uleb128 0x3b
	.uleb128 0xb
	.uleb128 0x39
	.uleb128 0xb
	.uleb128 0x49
	.uleb128 0x13
	.uleb128 0x2
	.uleb128 0x18
	.byte	0
	.byte	0
	.byte	0
	.section	.debug_aranges,"",@progbits
	.long	0x1c
	.value	0x2
	.long	.Ldebug_info0
	.byte	0x4
	.byte	0
	.value	0
	.value	0
	.long	.Ltext0
	.long	.Letext0-.Ltext0
	.long	0
	.long	0
	.section	.debug_line,"",@progbits
.Ldebug_line0:
	.section	.debug_str,"MS",@progbits,1
.LASF4:
	.string	"long long int"
.LASF2:
	.string	"unsigned int"
.LASF18:
	.string	"main"
.LASF7:
	.string	"long unsigned int"
.LASF10:
	.string	"long long unsigned int"
.LASF5:
	.string	"unsigned char"
.LASF11:
	.string	"char"
.LASF3:
	.string	"long int"
.LASF12:
	.string	"atoi"
.LASF16:
	.string	"NUMBER"
.LASF14:
	.string	"argc"
.LASF6:
	.string	"short unsigned int"
.LASF13:
	.string	"printf"
.LASF15:
	.string	"argv"
.LASF17:
	.string	"GNU C17 13.3.0 -masm=intel -m32 -mtune=generic -march=i686 -g -fasynchronous-unwind-tables -fstack-protector-strong -fstack-clash-protection"
.LASF9:
	.string	"short int"
.LASF8:
	.string	"signed char"
	.section	.debug_line_str,"MS",@progbits,1
.LASF1:
	.string	"/home/fekerr/src/compfast/sum_c"
.LASF0:
	.string	"sum.c"
	.ident	"GCC: (Ubuntu 13.3.0-6ubuntu2~24.04) 13.3.0"
	.section	.note.GNU-stack,"",@progbits
