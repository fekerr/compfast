	.file	"sum.c"
# GNU C17 (Ubuntu 13.3.0-6ubuntu2~24.04) version 13.3.0 (x86_64-linux-gnu)
#	compiled by GNU C version 13.3.0, GMP version 6.3.0, MPFR version 4.2.1, MPC version 1.3.1, isl version isl-0.26-GMP

# GGC heuristics: --param ggc-min-expand=100 --param ggc-min-heapsize=131072
# options passed: -m32 -mtune=generic -march=i686 -g -fasynchronous-unwind-tables -fstack-protector-strong -fstack-clash-protection
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
	leal	4(%esp), %ecx	#,
	.cfi_def_cfa 1, 0
	andl	$-16, %esp	#,
	pushl	-4(%ecx)	#
	pushl	%ebp	#
	movl	%esp, %ebp	#,
	.cfi_escape 0x10,0x5,0x2,0x75,0
	pushl	%esi	#
	pushl	%ebx	#
	pushl	%ecx	#
	.cfi_escape 0xf,0x3,0x75,0x74,0x6
	.cfi_escape 0x10,0x6,0x2,0x75,0x7c
	.cfi_escape 0x10,0x3,0x2,0x75,0x78
	subl	$28, %esp	#,
	call	__x86.get_pc_thunk.bx	#
	addl	$_GLOBAL_OFFSET_TABLE_, %ebx	# tmp82,
	movl	%ecx, %esi	#, tmp98
# sum.c:11:     int NUMBER = GUESS, i, s;
	.loc 1 11 9
	movl	$10000000, -36(%ebp)	#, NUMBER
# sum.c:12:     printf("argc=%d\n", argc);
	.loc 1 12 5
	subl	$8, %esp	#,
	pushl	(%esi)	# argc
	leal	.LC0@GOTOFF(%ebx), %eax	#, tmp89
	pushl	%eax	# tmp89
	call	printf@PLT	#
	addl	$16, %esp	#,
# sum.c:13:     if (argc < 2) {
	.loc 1 13 8
	cmpl	$1, (%esi)	#, argc
	jg	.L2	#,
# sum.c:14:         printf("no guess entered, using %d", NUMBER);
	.loc 1 14 9
	subl	$8, %esp	#,
	pushl	-36(%ebp)	# NUMBER
	leal	.LC1@GOTOFF(%ebx), %eax	#, tmp90
	pushl	%eax	# tmp90
	call	printf@PLT	#
	addl	$16, %esp	#,
	jmp	.L3	#
.L2:
# sum.c:17:         printf("argv[1]=%s", argv[1]);
	.loc 1 17 34
	movl	4(%esi), %eax	# argv, tmp91
	addl	$4, %eax	#, _1
# sum.c:17:         printf("argv[1]=%s", argv[1]);
	.loc 1 17 9
	movl	(%eax), %eax	# *_1, _2
	subl	$8, %esp	#,
	pushl	%eax	# _2
	leal	.LC2@GOTOFF(%ebx), %eax	#, tmp92
	pushl	%eax	# tmp92
	call	printf@PLT	#
	addl	$16, %esp	#,
# sum.c:18:         NUMBER = atoi(argv[1]);
	.loc 1 18 27
	movl	4(%esi), %eax	# argv, tmp93
	addl	$4, %eax	#, _3
# sum.c:18:         NUMBER = atoi(argv[1]);
	.loc 1 18 18
	movl	(%eax), %eax	# *_3, _4
	subl	$12, %esp	#,
	pushl	%eax	# _4
	call	atoi@PLT	#
	addl	$16, %esp	#,
	movl	%eax, -36(%ebp)	# tmp94, NUMBER
.L3:
# sum.c:22:     for (s = i = 0; i < NUMBER; ++i) {
	.loc 1 22 16
	movl	$0, -32(%ebp)	#, i
# sum.c:22:     for (s = i = 0; i < NUMBER; ++i) {
	.loc 1 22 12
	movl	-32(%ebp), %eax	# i, tmp95
	movl	%eax, -28(%ebp)	# tmp95, s
# sum.c:22:     for (s = i = 0; i < NUMBER; ++i) {
	.loc 1 22 5
	jmp	.L4	#
.L5:
# sum.c:23:         s += 1;  // Increment sum
	.loc 1 23 11
	addl	$1, -28(%ebp)	#, s
# sum.c:22:     for (s = i = 0; i < NUMBER; ++i) {
	.loc 1 22 33 discriminator 3
	addl	$1, -32(%ebp)	#, i
.L4:
# sum.c:22:     for (s = i = 0; i < NUMBER; ++i) {
	.loc 1 22 23 discriminator 1
	movl	-32(%ebp), %eax	# i, tmp96
	cmpl	-36(%ebp), %eax	# NUMBER, tmp96
	jl	.L5	#,
# sum.c:27:     return 0;
	.loc 1 27 12
	movl	$0, %eax	#, _19
# sum.c:28: }
	.loc 1 28 1
	leal	-12(%ebp), %esp	#,
	popl	%ecx	#
	.cfi_restore 1
	.cfi_def_cfa 1, 0
	popl	%ebx	#
	.cfi_restore 3
	popl	%esi	#
	.cfi_restore 6
	popl	%ebp	#
	.cfi_restore 5
	leal	-4(%ecx), %esp	#,
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
	movl	(%esp), %ebx	#,
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
.LASF17:
	.string	"GNU C17 13.3.0 -m32 -mtune=generic -march=i686 -g -fasynchronous-unwind-tables -fstack-protector-strong -fstack-clash-protection"
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
