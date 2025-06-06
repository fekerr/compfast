	.file	"sum.c"
	.intel_syntax noprefix
# GNU C17 (Ubuntu 13.3.0-6ubuntu2~24.04) version 13.3.0 (x86_64-linux-gnu)
#	compiled by GNU C version 13.3.0, GMP version 6.3.0, MPFR version 4.2.1, MPC version 1.3.1, isl version isl-0.26-GMP

# GGC heuristics: --param ggc-min-expand=100 --param ggc-min-heapsize=131072
# options passed: -masm=intel -m64 -mtune=generic -march=x86-64 -g -fasynchronous-unwind-tables -fstack-protector-strong -fstack-clash-protection -fcf-protection
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
	endbr64	
	push	rbp	#
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	mov	rbp, rsp	#,
	.cfi_def_cfa_register 6
	sub	rsp, 32	#,
	mov	DWORD PTR -20[rbp], edi	# argc, argc
	mov	QWORD PTR -32[rbp], rsi	# argv, argv
# sum.c:11:     int NUMBER = GUESS, i, s;
	.loc 1 11 9
	mov	DWORD PTR -12[rbp], 10000000	# NUMBER,
# sum.c:12:     printf("argc=%d\n", argc);
	.loc 1 12 5
	mov	eax, DWORD PTR -20[rbp]	# tmp88, argc
	mov	esi, eax	#, tmp88
	lea	rax, .LC0[rip]	# tmp89,
	mov	rdi, rax	#, tmp89
	mov	eax, 0	#,
	call	printf@PLT	#
# sum.c:13:     if (argc < 2) {
	.loc 1 13 8
	cmp	DWORD PTR -20[rbp], 1	# argc,
	jg	.L2	#,
# sum.c:14:         printf("no guess entered, using %d", NUMBER);
	.loc 1 14 9
	mov	eax, DWORD PTR -12[rbp]	# tmp90, NUMBER
	mov	esi, eax	#, tmp90
	lea	rax, .LC1[rip]	# tmp91,
	mov	rdi, rax	#, tmp91
	mov	eax, 0	#,
	call	printf@PLT	#
	jmp	.L3	#
.L2:
# sum.c:17:         printf("argv[1]=%s", argv[1]);
	.loc 1 17 34
	mov	rax, QWORD PTR -32[rbp]	# tmp92, argv
	add	rax, 8	# _1,
# sum.c:17:         printf("argv[1]=%s", argv[1]);
	.loc 1 17 9
	mov	rax, QWORD PTR [rax]	# _2, *_1
	mov	rsi, rax	#, _2
	lea	rax, .LC2[rip]	# tmp93,
	mov	rdi, rax	#, tmp93
	mov	eax, 0	#,
	call	printf@PLT	#
# sum.c:18:         NUMBER = atoi(argv[1]);
	.loc 1 18 27
	mov	rax, QWORD PTR -32[rbp]	# tmp94, argv
	add	rax, 8	# _3,
# sum.c:18:         NUMBER = atoi(argv[1]);
	.loc 1 18 18
	mov	rax, QWORD PTR [rax]	# _4, *_3
	mov	rdi, rax	#, _4
	call	atoi@PLT	#
	mov	DWORD PTR -12[rbp], eax	# NUMBER, tmp95
.L3:
# sum.c:22:     for (s = i = 0; i < NUMBER; ++i) {
	.loc 1 22 16
	mov	DWORD PTR -8[rbp], 0	# i,
# sum.c:22:     for (s = i = 0; i < NUMBER; ++i) {
	.loc 1 22 12
	mov	eax, DWORD PTR -8[rbp]	# tmp96, i
	mov	DWORD PTR -4[rbp], eax	# s, tmp96
# sum.c:22:     for (s = i = 0; i < NUMBER; ++i) {
	.loc 1 22 5
	jmp	.L4	#
.L5:
# sum.c:23:         s += 1;  // Increment sum
	.loc 1 23 11
	add	DWORD PTR -4[rbp], 1	# s,
# sum.c:22:     for (s = i = 0; i < NUMBER; ++i) {
	.loc 1 22 33 discriminator 3
	add	DWORD PTR -8[rbp], 1	# i,
.L4:
# sum.c:22:     for (s = i = 0; i < NUMBER; ++i) {
	.loc 1 22 23 discriminator 1
	mov	eax, DWORD PTR -8[rbp]	# tmp97, i
	cmp	eax, DWORD PTR -12[rbp]	# tmp97, NUMBER
	jl	.L5	#,
# sum.c:27:     return 0;
	.loc 1 27 12
	mov	eax, 0	# _19,
# sum.c:28: }
	.loc 1 28 1
	leave	
	.cfi_def_cfa 7, 8
	ret	
	.cfi_endproc
.LFE6:
	.size	main, .-main
.Letext0:
	.file 2 "/usr/include/stdlib.h"
	.file 3 "/usr/include/stdio.h"
	.section	.debug_info,"",@progbits
.Ldebug_info0:
	.long	0x11c
	.value	0x5
	.byte	0x1
	.byte	0x8
	.long	.Ldebug_abbrev0
	.uleb128 0x6
	.long	.LASF17
	.byte	0x1d
	.long	.LASF0
	.long	.LASF1
	.quad	.Ltext0
	.quad	.Letext0-.Ltext0
	.long	.Ldebug_line0
	.uleb128 0x1
	.byte	0x8
	.byte	0x7
	.long	.LASF2
	.uleb128 0x7
	.byte	0x4
	.byte	0x5
	.string	"int"
	.uleb128 0x1
	.byte	0x8
	.byte	0x5
	.long	.LASF3
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
	.uleb128 0x2
	.long	0x72
	.uleb128 0x1
	.byte	0x1
	.byte	0x6
	.long	.LASF10
	.uleb128 0x8
	.long	0x72
	.uleb128 0x1
	.byte	0x8
	.byte	0x7
	.long	.LASF11
	.uleb128 0x2
	.long	0x79
	.uleb128 0x9
	.long	.LASF12
	.byte	0x2
	.byte	0x69
	.byte	0xc
	.long	0x35
	.long	0xa0
	.uleb128 0x3
	.long	0x85
	.byte	0
	.uleb128 0xa
	.long	.LASF13
	.byte	0x3
	.value	0x16b
	.byte	0xc
	.long	0x35
	.long	0xb8
	.uleb128 0x3
	.long	0x85
	.uleb128 0xb
	.byte	0
	.uleb128 0xc
	.long	.LASF18
	.byte	0x1
	.byte	0x9
	.byte	0x5
	.long	0x35
	.quad	.LFB6
	.quad	.LFE6-.LFB6
	.uleb128 0x1
	.byte	0x9c
	.long	0x11a
	.uleb128 0x4
	.long	.LASF14
	.byte	0xe
	.long	0x35
	.uleb128 0x2
	.byte	0x91
	.sleb128 -36
	.uleb128 0x4
	.long	.LASF15
	.byte	0x1b
	.long	0x11a
	.uleb128 0x2
	.byte	0x91
	.sleb128 -48
	.uleb128 0xd
	.long	.LASF16
	.byte	0x1
	.byte	0xb
	.byte	0x9
	.long	0x35
	.uleb128 0x2
	.byte	0x91
	.sleb128 -28
	.uleb128 0x5
	.string	"i"
	.byte	0x19
	.long	0x35
	.uleb128 0x2
	.byte	0x91
	.sleb128 -24
	.uleb128 0x5
	.string	"s"
	.byte	0x1c
	.long	0x35
	.uleb128 0x2
	.byte	0x91
	.sleb128 -20
	.byte	0
	.uleb128 0x2
	.long	0x6d
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
	.sleb128 8
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
	.uleb128 0x7
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
	.uleb128 0x7
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
	.long	0x2c
	.value	0x2
	.long	.Ldebug_info0
	.byte	0x8
	.byte	0
	.value	0
	.value	0
	.quad	.Ltext0
	.quad	.Letext0-.Ltext0
	.quad	0
	.quad	0
	.section	.debug_line,"",@progbits
.Ldebug_line0:
	.section	.debug_str,"MS",@progbits,1
.LASF4:
	.string	"long long int"
.LASF7:
	.string	"unsigned int"
.LASF18:
	.string	"main"
.LASF2:
	.string	"long unsigned int"
.LASF11:
	.string	"long long unsigned int"
.LASF5:
	.string	"unsigned char"
.LASF10:
	.string	"char"
.LASF3:
	.string	"long int"
.LASF12:
	.string	"atoi"
.LASF17:
	.string	"GNU C17 13.3.0 -masm=intel -m64 -mtune=generic -march=x86-64 -g -fasynchronous-unwind-tables -fstack-protector-strong -fstack-clash-protection -fcf-protection"
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
