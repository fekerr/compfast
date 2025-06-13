	.file	"sum_rdtsc.c"
	.intel_syntax noprefix
# GNU C17 (Ubuntu 13.3.0-6ubuntu2~24.04) version 13.3.0 (x86_64-linux-gnu)
#	compiled by GNU C version 13.3.0, GMP version 6.3.0, MPFR version 4.2.1, MPC version 1.3.1, isl version isl-0.26-GMP

# GGC heuristics: --param ggc-min-expand=100 --param ggc-min-heapsize=131072
# options passed: -masm=intel -m64 -mtune=generic -march=x86-64 -g -fasynchronous-unwind-tables -fstack-protector-strong -fstack-clash-protection -fcf-protection
	.text
.Ltext0:
	.file 0 "/home/fekerr/src/compfast/rdtsc" "sum_rdtsc.c"
	.type	rdtsc, @function
rdtsc:
.LFB0:
	.file 1 "sum_rdtsc.c"
	.loc 1 9 32
	.cfi_startproc
	push	rbp	#
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	mov	rbp, rsp	#,
	.cfi_def_cfa_register 6
# sum_rdtsc.c:11:     __asm__ __volatile__ ("rdtsc" : "=a" (lo), "=d" (hi));
	.loc 1 11 5
#APP
# 11 "sum_rdtsc.c" 1
	rdtsc
# 0 "" 2
#NO_APP
	mov	DWORD PTR -8[rbp], eax	# lo, lo
	mov	DWORD PTR -4[rbp], edx	# hi, hi
# sum_rdtsc.c:12:     return ((uint64_t)hi << 32) | lo;
	.loc 1 12 13
	mov	eax, DWORD PTR -4[rbp]	# _1, hi
# sum_rdtsc.c:12:     return ((uint64_t)hi << 32) | lo;
	.loc 1 12 26
	sal	rax, 32	# _1,
	mov	rdx, rax	# _2, _1
# sum_rdtsc.c:12:     return ((uint64_t)hi << 32) | lo;
	.loc 1 12 33
	mov	eax, DWORD PTR -8[rbp]	# _3, lo
	or	rax, rdx	# _6, _2
# sum_rdtsc.c:13: }
	.loc 1 13 1
	pop	rbp	#
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE0:
	.size	rdtsc, .-rdtsc
	.globl	exampleFunction
	.type	exampleFunction, @function
exampleFunction:
.LFB1:
	.loc 1 16 38
	.cfi_startproc
	endbr64
	push	rbp	#
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	mov	rbp, rsp	#,
	.cfi_def_cfa_register 6
	mov	DWORD PTR -20[rbp], edi	# iterations, iterations
# sum_rdtsc.c:17:     volatile int sum = 0;
	.loc 1 17 18
	mov	DWORD PTR -8[rbp], 0	# sum,
.LBB2:
# sum_rdtsc.c:18:     for (int i = 0; i < iterations; ++i) {
	.loc 1 18 14
	mov	DWORD PTR -4[rbp], 0	# i,
# sum_rdtsc.c:18:     for (int i = 0; i < iterations; ++i) {
	.loc 1 18 5
	jmp	.L4	#
.L5:
# sum_rdtsc.c:19:         sum += i;
	.loc 1 19 13
	mov	edx, DWORD PTR -8[rbp]	# sum.0_1, sum
	mov	eax, DWORD PTR -4[rbp]	# tmp84, i
	add	eax, edx	# _2, sum.0_1
	mov	DWORD PTR -8[rbp], eax	# sum, _2
# sum_rdtsc.c:18:     for (int i = 0; i < iterations; ++i) {
	.loc 1 18 37 discriminator 3
	add	DWORD PTR -4[rbp], 1	# i,
.L4:
# sum_rdtsc.c:18:     for (int i = 0; i < iterations; ++i) {
	.loc 1 18 23 discriminator 1
	mov	eax, DWORD PTR -4[rbp]	# tmp85, i
	cmp	eax, DWORD PTR -20[rbp]	# tmp85, iterations
	jl	.L5	#,
.LBE2:
# sum_rdtsc.c:21: }
	.loc 1 21 1
	nop
	nop
	pop	rbp	#
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE1:
	.size	exampleFunction, .-exampleFunction
	.section	.rodata
.LC1:
	.string	"r"
.LC2:
	.string	"/proc/cpuinfo"
.LC3:
	.string	"fopen"
.LC5:
	.string	"cpu MHz : %lf"
	.text
	.globl	get_cpu_frequency
	.type	get_cpu_frequency, @function
get_cpu_frequency:
.LFB2:
	.loc 1 24 28
	.cfi_startproc
	endbr64
	push	rbp	#
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	mov	rbp, rsp	#,
	.cfi_def_cfa_register 6
	sub	rsp, 160	#,
# sum_rdtsc.c:24: double get_cpu_frequency() {
	.loc 1 24 28
	mov	rax, QWORD PTR fs:40	# tmp100, MEM[(<address-space-1> long unsigned int *)40B]
	mov	QWORD PTR -8[rbp], rax	# D.4165, tmp100
	xor	eax, eax	# tmp100
# sum_rdtsc.c:27:     double freq = 0.0;
	.loc 1 27 12
	pxor	xmm0, xmm0	# tmp87
	movsd	QWORD PTR -160[rbp], xmm0	# freq, tmp87
# sum_rdtsc.c:29:     fp = fopen("/proc/cpuinfo", "r");
	.loc 1 29 10
	lea	rax, .LC1[rip]	# tmp88,
	mov	rsi, rax	#, tmp88
	lea	rax, .LC2[rip]	# tmp89,
	mov	rdi, rax	#, tmp89
	call	fopen@PLT	#
	mov	QWORD PTR -152[rbp], rax	# fp, tmp90
# sum_rdtsc.c:30:     if (fp == NULL) {
	.loc 1 30 8
	cmp	QWORD PTR -152[rbp], 0	# fp,
	jne	.L9	#,
# sum_rdtsc.c:31:         perror("fopen");
	.loc 1 31 9
	lea	rax, .LC3[rip]	# tmp91,
	mov	rdi, rax	#, tmp91
	call	perror@PLT	#
# sum_rdtsc.c:32:         return -1;
	.loc 1 32 16
	movsd	xmm0, QWORD PTR .LC4[rip]	# _4,
	jmp	.L12	#
.L11:
# sum_rdtsc.c:36:         if (sscanf(buffer, "cpu MHz : %lf", &freq) == 1) {
	.loc 1 36 13
	lea	rdx, -160[rbp]	# tmp92,
	lea	rax, -144[rbp]	# tmp93,
	lea	rcx, .LC5[rip]	# tmp94,
	mov	rsi, rcx	#, tmp94
	mov	rdi, rax	#, tmp93
	mov	eax, 0	#,
	call	__isoc99_sscanf@PLT	#
# sum_rdtsc.c:36:         if (sscanf(buffer, "cpu MHz : %lf", &freq) == 1) {
	.loc 1 36 12 discriminator 1
	cmp	eax, 1	# _1,
	je	.L14	#,
.L9:
# sum_rdtsc.c:35:     while (fgets(buffer, sizeof(buffer), fp)) {
	.loc 1 35 12
	mov	rdx, QWORD PTR -152[rbp]	# tmp95, fp
	lea	rax, -144[rbp]	# tmp96,
	mov	esi, 128	#,
	mov	rdi, rax	#, tmp96
	call	fgets@PLT	#
# sum_rdtsc.c:35:     while (fgets(buffer, sizeof(buffer), fp)) {
	.loc 1 35 12 is_stmt 0 discriminator 1
	test	rax, rax	# _2
	jne	.L11	#,
	jmp	.L10	#
.L14:
# sum_rdtsc.c:37:             break;
	.loc 1 37 13 is_stmt 1
	nop
.L10:
# sum_rdtsc.c:41:     fclose(fp);
	.loc 1 41 5
	mov	rax, QWORD PTR -152[rbp]	# tmp97, fp
	mov	rdi, rax	#, tmp97
	call	fclose@PLT	#
# sum_rdtsc.c:42:     return freq * 1e6; // Convert MHz to Hz
	.loc 1 42 17
	movsd	xmm1, QWORD PTR -160[rbp]	# freq.1_3, freq
	movsd	xmm0, QWORD PTR .LC6[rip]	# tmp98,
	mulsd	xmm0, xmm1	# _4, freq.1_3
.L12:
# sum_rdtsc.c:43: }
	.loc 1 43 1
	mov	rax, QWORD PTR -8[rbp]	# tmp101, D.4165
	sub	rax, QWORD PTR fs:40	# tmp101, MEM[(<address-space-1> long unsigned int *)40B]
	je	.L13	#,
	call	__stack_chk_fail@PLT	#
.L13:
	leave
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE2:
	.size	get_cpu_frequency, .-get_cpu_frequency
	.globl	get_cpu_core
	.type	get_cpu_core, @function
get_cpu_core:
.LFB3:
	.loc 1 46 20
	.cfi_startproc
	endbr64
	push	rbp	#
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	mov	rbp, rsp	#,
	.cfi_def_cfa_register 6
# sum_rdtsc.c:50:     return -1; // Return -1 if sched_getcpu is not available
	.loc 1 50 12
	mov	eax, -1	# _1,
# sum_rdtsc.c:52: }
	.loc 1 52 1
	pop	rbp	#
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE3:
	.size	get_cpu_core, .-get_cpu_core
	.section	.rodata
.LC7:
	.string	"CPU Information:"
.LC8:
	.string	"processor"
.LC9:
	.string	"model name"
.LC10:
	.string	"cpu cores"
.LC11:
	.string	"core id"
.LC12:
	.string	"%s"
	.text
	.globl	print_cpu_info
	.type	print_cpu_info, @function
print_cpu_info:
.LFB4:
	.loc 1 55 23
	.cfi_startproc
	endbr64
	push	rbp	#
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	mov	rbp, rsp	#,
	.cfi_def_cfa_register 6
	sub	rsp, 288	#,
# sum_rdtsc.c:55: void print_cpu_info() {
	.loc 1 55 23
	mov	rax, QWORD PTR fs:40	# tmp105, MEM[(<address-space-1> long unsigned int *)40B]
	mov	QWORD PTR -8[rbp], rax	# D.4171, tmp105
	xor	eax, eax	# tmp105
# sum_rdtsc.c:59:     fp = fopen("/proc/cpuinfo", "r");
	.loc 1 59 10
	lea	rax, .LC1[rip]	# tmp87,
	mov	rsi, rax	#, tmp87
	lea	rax, .LC2[rip]	# tmp88,
	mov	rdi, rax	#, tmp88
	call	fopen@PLT	#
	mov	QWORD PTR -280[rbp], rax	# fp, tmp89
# sum_rdtsc.c:60:     if (fp == NULL) {
	.loc 1 60 8
	cmp	QWORD PTR -280[rbp], 0	# fp,
	jne	.L18	#,
# sum_rdtsc.c:61:         perror("fopen");
	.loc 1 61 9
	lea	rax, .LC3[rip]	# tmp90,
	mov	rdi, rax	#, tmp90
	call	perror@PLT	#
	jmp	.L17	#
.L18:
# sum_rdtsc.c:65:     printf("CPU Information:\n");
	.loc 1 65 5
	lea	rax, .LC7[rip]	# tmp91,
	mov	rdi, rax	#, tmp91
	call	puts@PLT	#
# sum_rdtsc.c:66:     while (fgets(buffer, sizeof(buffer), fp)) {
	.loc 1 66 11
	jmp	.L20	#
.L23:
# sum_rdtsc.c:67:         if (strstr(buffer, "processor") || strstr(buffer, "model name") ||
	.loc 1 67 13
	lea	rax, -272[rbp]	# tmp92,
	lea	rdx, .LC8[rip]	# tmp93,
	mov	rsi, rdx	#, tmp93
	mov	rdi, rax	#, tmp92
	call	strstr@PLT	#
# sum_rdtsc.c:67:         if (strstr(buffer, "processor") || strstr(buffer, "model name") ||
	.loc 1 67 12 discriminator 1
	test	rax, rax	# _1
	jne	.L21	#,
# sum_rdtsc.c:67:         if (strstr(buffer, "processor") || strstr(buffer, "model name") ||
	.loc 1 67 44 discriminator 1
	lea	rax, -272[rbp]	# tmp94,
	lea	rdx, .LC9[rip]	# tmp95,
	mov	rsi, rdx	#, tmp95
	mov	rdi, rax	#, tmp94
	call	strstr@PLT	#
# sum_rdtsc.c:67:         if (strstr(buffer, "processor") || strstr(buffer, "model name") ||
	.loc 1 67 41 discriminator 1
	test	rax, rax	# _2
	jne	.L21	#,
# sum_rdtsc.c:68:             strstr(buffer, "cpu cores") || strstr(buffer, "core id")) {
	.loc 1 68 13
	lea	rax, -272[rbp]	# tmp96,
	lea	rdx, .LC10[rip]	# tmp97,
	mov	rsi, rdx	#, tmp97
	mov	rdi, rax	#, tmp96
	call	strstr@PLT	#
# sum_rdtsc.c:67:         if (strstr(buffer, "processor") || strstr(buffer, "model name") ||
	.loc 1 67 73 discriminator 2
	test	rax, rax	# _3
	jne	.L21	#,
# sum_rdtsc.c:68:             strstr(buffer, "cpu cores") || strstr(buffer, "core id")) {
	.loc 1 68 44
	lea	rax, -272[rbp]	# tmp98,
	lea	rdx, .LC11[rip]	# tmp99,
	mov	rsi, rdx	#, tmp99
	mov	rdi, rax	#, tmp98
	call	strstr@PLT	#
# sum_rdtsc.c:68:             strstr(buffer, "cpu cores") || strstr(buffer, "core id")) {
	.loc 1 68 41 discriminator 1
	test	rax, rax	# _4
	je	.L20	#,
.L21:
# sum_rdtsc.c:69:             printf("%s", buffer);
	.loc 1 69 13
	lea	rax, -272[rbp]	# tmp100,
	mov	rsi, rax	#, tmp100
	lea	rax, .LC12[rip]	# tmp101,
	mov	rdi, rax	#, tmp101
	mov	eax, 0	#,
	call	printf@PLT	#
.L20:
# sum_rdtsc.c:66:     while (fgets(buffer, sizeof(buffer), fp)) {
	.loc 1 66 12
	mov	rdx, QWORD PTR -280[rbp]	# tmp102, fp
	lea	rax, -272[rbp]	# tmp103,
	mov	esi, 256	#,
	mov	rdi, rax	#, tmp103
	call	fgets@PLT	#
# sum_rdtsc.c:66:     while (fgets(buffer, sizeof(buffer), fp)) {
	.loc 1 66 12 is_stmt 0 discriminator 1
	test	rax, rax	# _5
	jne	.L23	#,
# sum_rdtsc.c:73:     fclose(fp);
	.loc 1 73 5 is_stmt 1
	mov	rax, QWORD PTR -280[rbp]	# tmp104, fp
	mov	rdi, rax	#, tmp104
	call	fclose@PLT	#
.L17:
# sum_rdtsc.c:74: }
	.loc 1 74 1
	mov	rax, QWORD PTR -8[rbp]	# tmp106, D.4171
	sub	rax, QWORD PTR fs:40	# tmp106, MEM[(<address-space-1> long unsigned int *)40B]
	je	.L24	#,
	call	__stack_chk_fail@PLT	#
.L24:
	leave
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE4:
	.size	print_cpu_info, .-print_cpu_info
	.section	.rodata
.LC13:
	.string	"Failed to get CPU frequency\n"
.LC15:
	.string	"CPU Frequency: %.2f GHz\n"
	.align 8
.LC16:
	.string	"CPU core information not available."
.LC17:
	.string	"Running on CPU core: %d\n"
.LC18:
	.string	"Elapsed cycles: %lu\n"
.LC19:
	.string	"Elapsed time: %.6f seconds\n"
	.align 8
.LC20:
	.string	"Estimated iterations for 1 second runtime: %d\n"
	.text
	.globl	main
	.type	main, @function
main:
.LFB5:
	.loc 1 76 12
	.cfi_startproc
	endbr64
	push	rbp	#
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	mov	rbp, rsp	#,
	.cfi_def_cfa_register 6
	sub	rsp, 48	#,
# sum_rdtsc.c:78:     double cpu_frequency = get_cpu_frequency();
	.loc 1 78 28
	mov	eax, 0	#,
	call	get_cpu_frequency	#
	movq	rax, xmm0	# tmp91,
	mov	QWORD PTR -32[rbp], rax	# cpu_frequency, tmp91
# sum_rdtsc.c:80:     if (cpu_frequency < 0) {
	.loc 1 80 8
	pxor	xmm0, xmm0	# tmp92
	comisd	xmm0, QWORD PTR -32[rbp]	# tmp92, cpu_frequency
	jbe	.L34	#,
# sum_rdtsc.c:81:         fprintf(stderr, "Failed to get CPU frequency\n");
	.loc 1 81 9
	mov	rax, QWORD PTR stderr[rip]	# stderr.2_1, stderr
	mov	rcx, rax	#, stderr.2_1
	mov	edx, 28	#,
	mov	esi, 1	#,
	lea	rax, .LC13[rip]	# tmp93,
	mov	rdi, rax	#, tmp93
	call	fwrite@PLT	#
# sum_rdtsc.c:82:         return 1;
	.loc 1 82 16
	mov	eax, 1	# _8,
	jmp	.L28	#
.L34:
# sum_rdtsc.c:85:     printf("CPU Frequency: %.2f GHz\n", cpu_frequency / 1e9);
	.loc 1 85 5
	movsd	xmm0, QWORD PTR -32[rbp]	# tmp94, cpu_frequency
	movsd	xmm1, QWORD PTR .LC14[rip]	# tmp95,
	divsd	xmm0, xmm1	# tmp94, tmp95
	movq	rax, xmm0	# _2, tmp94
	movq	xmm0, rax	#, _2
	lea	rax, .LC15[rip]	# tmp96,
	mov	rdi, rax	#, tmp96
	mov	eax, 1	#,
	call	printf@PLT	#
# sum_rdtsc.c:87:     int core = get_cpu_core();
	.loc 1 87 16
	mov	eax, 0	#,
	call	get_cpu_core	#
	mov	DWORD PTR -44[rbp], eax	# core, tmp97
# sum_rdtsc.c:88:     if (core == -1) {
	.loc 1 88 8
	cmp	DWORD PTR -44[rbp], -1	# core,
	jne	.L29	#,
# sum_rdtsc.c:89:         printf("CPU core information not available.\n");
	.loc 1 89 9
	lea	rax, .LC16[rip]	# tmp98,
	mov	rdi, rax	#, tmp98
	call	puts@PLT	#
	jmp	.L30	#
.L29:
# sum_rdtsc.c:91:         printf("Running on CPU core: %d\n", core);
	.loc 1 91 9
	mov	eax, DWORD PTR -44[rbp]	# tmp99, core
	mov	esi, eax	#, tmp99
	lea	rax, .LC17[rip]	# tmp100,
	mov	rdi, rax	#, tmp100
	mov	eax, 0	#,
	call	printf@PLT	#
.L30:
# sum_rdtsc.c:94:     print_cpu_info();
	.loc 1 94 5
	mov	eax, 0	#,
	call	print_cpu_info	#
# sum_rdtsc.c:96:     int iterations = 1000000; // Initial number of iterations
	.loc 1 96 9
	mov	DWORD PTR -40[rbp], 1000000	# iterations,
# sum_rdtsc.c:97:     start = rdtsc();
	.loc 1 97 13
	mov	eax, 0	#,
	call	rdtsc	#
	mov	QWORD PTR -24[rbp], rax	# start, tmp101
# sum_rdtsc.c:98:     exampleFunction(iterations);
	.loc 1 98 5
	mov	eax, DWORD PTR -40[rbp]	# tmp102, iterations
	mov	edi, eax	#, tmp102
	call	exampleFunction	#
# sum_rdtsc.c:99:     end = rdtsc();
	.loc 1 99 11
	mov	eax, 0	#,
	call	rdtsc	#
	mov	QWORD PTR -16[rbp], rax	# end, tmp103
# sum_rdtsc.c:101:     double elapsed_seconds = (double)(end - start) / cpu_frequency;
	.loc 1 101 43
	mov	rax, QWORD PTR -16[rbp]	# tmp104, end
	sub	rax, QWORD PTR -24[rbp]	# _3, start
# sum_rdtsc.c:101:     double elapsed_seconds = (double)(end - start) / cpu_frequency;
	.loc 1 101 30
	test	rax, rax	# _3
	js	.L31	#,
	pxor	xmm0, xmm0	# _4
	cvtsi2sd	xmm0, rax	# _4, _3
	jmp	.L32	#
.L31:
	mov	rdx, rax	# tmp106, _3
	shr	rdx	# tmp106
	and	eax, 1	# tmp107,
	or	rdx, rax	# tmp106, tmp107
	pxor	xmm0, xmm0	# tmp105
	cvtsi2sd	xmm0, rdx	# tmp105, tmp106
	addsd	xmm0, xmm0	# _4, tmp105
.L32:
# sum_rdtsc.c:101:     double elapsed_seconds = (double)(end - start) / cpu_frequency;
	.loc 1 101 12
	divsd	xmm0, QWORD PTR -32[rbp]	# tmp108, cpu_frequency
	movsd	QWORD PTR -8[rbp], xmm0	# elapsed_seconds, tmp108
# sum_rdtsc.c:102:     printf("Elapsed cycles: %" PRIu64 "\n", (end - start));
	.loc 1 102 5
	mov	rax, QWORD PTR -16[rbp]	# tmp109, end
	sub	rax, QWORD PTR -24[rbp]	# _5, start
	mov	rsi, rax	#, _5
	lea	rax, .LC18[rip]	# tmp110,
	mov	rdi, rax	#, tmp110
	mov	eax, 0	#,
	call	printf@PLT	#
# sum_rdtsc.c:103:     printf("Elapsed time: %.6f seconds\n", elapsed_seconds);
	.loc 1 103 5
	mov	rax, QWORD PTR -8[rbp]	# tmp111, elapsed_seconds
	movq	xmm0, rax	#, tmp111
	lea	rax, .LC19[rip]	# tmp112,
	mov	rdi, rax	#, tmp112
	mov	eax, 1	#,
	call	printf@PLT	#
# sum_rdtsc.c:105:     int iterations_for_1s = (int)(iterations / elapsed_seconds);
	.loc 1 105 46
	pxor	xmm0, xmm0	# _6
	cvtsi2sd	xmm0, DWORD PTR -40[rbp]	# _6, iterations
	divsd	xmm0, QWORD PTR -8[rbp]	# _7, elapsed_seconds
# sum_rdtsc.c:105:     int iterations_for_1s = (int)(iterations / elapsed_seconds);
	.loc 1 105 9
	cvttsd2si	eax, xmm0	# tmp113, _7
	mov	DWORD PTR -36[rbp], eax	# iterations_for_1s, tmp113
# sum_rdtsc.c:106:     printf("Estimated iterations for 1 second runtime: %d\n", iterations_for_1s);
	.loc 1 106 5
	mov	eax, DWORD PTR -36[rbp]	# tmp114, iterations_for_1s
	mov	esi, eax	#, tmp114
	lea	rax, .LC20[rip]	# tmp115,
	mov	rdi, rax	#, tmp115
	mov	eax, 0	#,
	call	printf@PLT	#
# sum_rdtsc.c:108:     return 0;
	.loc 1 108 12
	mov	eax, 0	# _8,
.L28:
# sum_rdtsc.c:109: }
	.loc 1 109 1
	leave
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE5:
	.size	main, .-main
	.section	.rodata
	.align 8
.LC4:
	.long	0
	.long	-1074790400
	.align 8
.LC6:
	.long	0
	.long	1093567616
	.align 8
.LC14:
	.long	0
	.long	1104006501
	.text
.Letext0:
	.file 2 "/usr/lib/gcc/x86_64-linux-gnu/13/include/stddef.h"
	.file 3 "/usr/include/x86_64-linux-gnu/bits/types.h"
	.file 4 "/usr/include/x86_64-linux-gnu/bits/types/struct_FILE.h"
	.file 5 "/usr/include/x86_64-linux-gnu/bits/types/FILE.h"
	.file 6 "/usr/include/x86_64-linux-gnu/bits/stdint-uintn.h"
	.file 7 "/usr/include/stdio.h"
	.file 8 "/usr/include/string.h"
	.section	.debug_info,"",@progbits
.Ldebug_info0:
	.long	0x543
	.value	0x5
	.byte	0x1
	.byte	0x8
	.long	.Ldebug_abbrev0
	.uleb128 0xf
	.long	.LASF67
	.byte	0x1d
	.long	.LASF0
	.long	.LASF1
	.quad	.Ltext0
	.quad	.Letext0-.Ltext0
	.long	.Ldebug_line0
	.uleb128 0x7
	.long	.LASF9
	.byte	0x2
	.byte	0xd6
	.byte	0x17
	.long	0x3a
	.uleb128 0x3
	.byte	0x8
	.byte	0x7
	.long	.LASF2
	.uleb128 0x3
	.byte	0x4
	.byte	0x7
	.long	.LASF3
	.uleb128 0x10
	.byte	0x8
	.uleb128 0x3
	.byte	0x1
	.byte	0x8
	.long	.LASF4
	.uleb128 0x3
	.byte	0x2
	.byte	0x7
	.long	.LASF5
	.uleb128 0x3
	.byte	0x1
	.byte	0x6
	.long	.LASF6
	.uleb128 0x3
	.byte	0x2
	.byte	0x5
	.long	.LASF7
	.uleb128 0x11
	.byte	0x4
	.byte	0x5
	.string	"int"
	.uleb128 0x12
	.long	0x66
	.uleb128 0x3
	.byte	0x8
	.byte	0x5
	.long	.LASF8
	.uleb128 0x7
	.long	.LASF10
	.byte	0x3
	.byte	0x2d
	.byte	0x1b
	.long	0x3a
	.uleb128 0x7
	.long	.LASF11
	.byte	0x3
	.byte	0x98
	.byte	0x19
	.long	0x72
	.uleb128 0x7
	.long	.LASF12
	.byte	0x3
	.byte	0x99
	.byte	0x1b
	.long	0x72
	.uleb128 0x5
	.long	0xa7
	.uleb128 0xb
	.long	0x9d
	.uleb128 0x3
	.byte	0x1
	.byte	0x6
	.long	.LASF13
	.uleb128 0x13
	.long	0xa7
	.uleb128 0x14
	.long	.LASF68
	.byte	0xd8
	.byte	0x4
	.byte	0x31
	.byte	0x8
	.long	0x21d
	.uleb128 0x1
	.long	.LASF14
	.byte	0x33
	.byte	0x7
	.long	0x66
	.byte	0
	.uleb128 0x1
	.long	.LASF15
	.byte	0x36
	.byte	0x9
	.long	0x9d
	.byte	0x8
	.uleb128 0x1
	.long	.LASF16
	.byte	0x37
	.byte	0x9
	.long	0x9d
	.byte	0x10
	.uleb128 0x1
	.long	.LASF17
	.byte	0x38
	.byte	0x9
	.long	0x9d
	.byte	0x18
	.uleb128 0x1
	.long	.LASF18
	.byte	0x39
	.byte	0x9
	.long	0x9d
	.byte	0x20
	.uleb128 0x1
	.long	.LASF19
	.byte	0x3a
	.byte	0x9
	.long	0x9d
	.byte	0x28
	.uleb128 0x1
	.long	.LASF20
	.byte	0x3b
	.byte	0x9
	.long	0x9d
	.byte	0x30
	.uleb128 0x1
	.long	.LASF21
	.byte	0x3c
	.byte	0x9
	.long	0x9d
	.byte	0x38
	.uleb128 0x1
	.long	.LASF22
	.byte	0x3d
	.byte	0x9
	.long	0x9d
	.byte	0x40
	.uleb128 0x1
	.long	.LASF23
	.byte	0x40
	.byte	0x9
	.long	0x9d
	.byte	0x48
	.uleb128 0x1
	.long	.LASF24
	.byte	0x41
	.byte	0x9
	.long	0x9d
	.byte	0x50
	.uleb128 0x1
	.long	.LASF25
	.byte	0x42
	.byte	0x9
	.long	0x9d
	.byte	0x58
	.uleb128 0x1
	.long	.LASF26
	.byte	0x44
	.byte	0x16
	.long	0x236
	.byte	0x60
	.uleb128 0x1
	.long	.LASF27
	.byte	0x46
	.byte	0x14
	.long	0x23b
	.byte	0x68
	.uleb128 0x1
	.long	.LASF28
	.byte	0x48
	.byte	0x7
	.long	0x66
	.byte	0x70
	.uleb128 0x1
	.long	.LASF29
	.byte	0x49
	.byte	0x7
	.long	0x66
	.byte	0x74
	.uleb128 0x1
	.long	.LASF30
	.byte	0x4a
	.byte	0xb
	.long	0x85
	.byte	0x78
	.uleb128 0x1
	.long	.LASF31
	.byte	0x4d
	.byte	0x12
	.long	0x51
	.byte	0x80
	.uleb128 0x1
	.long	.LASF32
	.byte	0x4e
	.byte	0xf
	.long	0x58
	.byte	0x82
	.uleb128 0x1
	.long	.LASF33
	.byte	0x4f
	.byte	0x8
	.long	0x240
	.byte	0x83
	.uleb128 0x1
	.long	.LASF34
	.byte	0x51
	.byte	0xf
	.long	0x250
	.byte	0x88
	.uleb128 0x1
	.long	.LASF35
	.byte	0x59
	.byte	0xd
	.long	0x91
	.byte	0x90
	.uleb128 0x1
	.long	.LASF36
	.byte	0x5b
	.byte	0x17
	.long	0x25a
	.byte	0x98
	.uleb128 0x1
	.long	.LASF37
	.byte	0x5c
	.byte	0x19
	.long	0x264
	.byte	0xa0
	.uleb128 0x1
	.long	.LASF38
	.byte	0x5d
	.byte	0x14
	.long	0x23b
	.byte	0xa8
	.uleb128 0x1
	.long	.LASF39
	.byte	0x5e
	.byte	0x9
	.long	0x48
	.byte	0xb0
	.uleb128 0x1
	.long	.LASF40
	.byte	0x5f
	.byte	0xa
	.long	0x2e
	.byte	0xb8
	.uleb128 0x1
	.long	.LASF41
	.byte	0x60
	.byte	0x7
	.long	0x66
	.byte	0xc0
	.uleb128 0x1
	.long	.LASF42
	.byte	0x62
	.byte	0x8
	.long	0x269
	.byte	0xc4
	.byte	0
	.uleb128 0x7
	.long	.LASF43
	.byte	0x5
	.byte	0x7
	.byte	0x19
	.long	0xb3
	.uleb128 0x15
	.long	.LASF69
	.byte	0x4
	.byte	0x2b
	.byte	0xe
	.uleb128 0xc
	.long	.LASF44
	.uleb128 0x5
	.long	0x231
	.uleb128 0x5
	.long	0xb3
	.uleb128 0x8
	.long	0xa7
	.long	0x250
	.uleb128 0x9
	.long	0x3a
	.byte	0
	.byte	0
	.uleb128 0x5
	.long	0x229
	.uleb128 0xc
	.long	.LASF45
	.uleb128 0x5
	.long	0x255
	.uleb128 0xc
	.long	.LASF46
	.uleb128 0x5
	.long	0x25f
	.uleb128 0x8
	.long	0xa7
	.long	0x279
	.uleb128 0x9
	.long	0x3a
	.byte	0x13
	.byte	0
	.uleb128 0x5
	.long	0xae
	.uleb128 0xb
	.long	0x279
	.uleb128 0x5
	.long	0x21d
	.uleb128 0xb
	.long	0x283
	.uleb128 0x16
	.long	.LASF70
	.byte	0x7
	.byte	0x97
	.byte	0xe
	.long	0x283
	.uleb128 0x7
	.long	.LASF47
	.byte	0x6
	.byte	0x1b
	.byte	0x14
	.long	0x79
	.uleb128 0xa
	.long	.LASF48
	.byte	0x7
	.value	0x16b
	.byte	0xc
	.long	0x66
	.long	0x2bd
	.uleb128 0x2
	.long	0x279
	.uleb128 0xd
	.byte	0
	.uleb128 0xa
	.long	.LASF49
	.byte	0x8
	.value	0x15e
	.byte	0xe
	.long	0x9d
	.long	0x2d9
	.uleb128 0x2
	.long	0x279
	.uleb128 0x2
	.long	0x279
	.byte	0
	.uleb128 0x17
	.long	.LASF50
	.byte	0x7
	.byte	0xb8
	.byte	0xc
	.long	0x66
	.long	0x2ef
	.uleb128 0x2
	.long	0x283
	.byte	0
	.uleb128 0xa
	.long	.LASF51
	.byte	0x7
	.value	0x28e
	.byte	0xe
	.long	0x9d
	.long	0x310
	.uleb128 0x2
	.long	0xa2
	.uleb128 0x2
	.long	0x66
	.uleb128 0x2
	.long	0x288
	.byte	0
	.uleb128 0x18
	.long	.LASF60
	.byte	0x7
	.value	0x1d4
	.byte	0xc
	.long	.LASF71
	.long	0x66
	.long	0x331
	.uleb128 0x2
	.long	0x279
	.uleb128 0x2
	.long	0x279
	.uleb128 0xd
	.byte	0
	.uleb128 0x19
	.long	.LASF72
	.byte	0x7
	.value	0x36e
	.byte	0xd
	.long	0x344
	.uleb128 0x2
	.long	0x279
	.byte	0
	.uleb128 0xa
	.long	.LASF52
	.byte	0x7
	.value	0x108
	.byte	0xe
	.long	0x283
	.long	0x360
	.uleb128 0x2
	.long	0x27e
	.uleb128 0x2
	.long	0x27e
	.byte	0
	.uleb128 0xe
	.long	.LASF63
	.byte	0x4c
	.byte	0x5
	.long	0x66
	.quad	.LFB5
	.quad	.LFE5-.LFB5
	.uleb128 0x1
	.byte	0x9c
	.long	0x3e4
	.uleb128 0x4
	.long	.LASF53
	.byte	0x4d
	.byte	0xe
	.long	0x299
	.uleb128 0x2
	.byte	0x91
	.sleb128 -40
	.uleb128 0x6
	.string	"end"
	.byte	0x4d
	.byte	0x15
	.long	0x299
	.uleb128 0x2
	.byte	0x91
	.sleb128 -32
	.uleb128 0x4
	.long	.LASF54
	.byte	0x4e
	.byte	0xc
	.long	0x3e4
	.uleb128 0x2
	.byte	0x91
	.sleb128 -48
	.uleb128 0x4
	.long	.LASF55
	.byte	0x57
	.byte	0x9
	.long	0x66
	.uleb128 0x2
	.byte	0x91
	.sleb128 -60
	.uleb128 0x4
	.long	.LASF56
	.byte	0x60
	.byte	0x9
	.long	0x66
	.uleb128 0x2
	.byte	0x91
	.sleb128 -56
	.uleb128 0x4
	.long	.LASF57
	.byte	0x65
	.byte	0xc
	.long	0x3e4
	.uleb128 0x2
	.byte	0x91
	.sleb128 -24
	.uleb128 0x4
	.long	.LASF58
	.byte	0x69
	.byte	0x9
	.long	0x66
	.uleb128 0x2
	.byte	0x91
	.sleb128 -52
	.byte	0
	.uleb128 0x3
	.byte	0x8
	.byte	0x4
	.long	.LASF59
	.uleb128 0x1a
	.long	.LASF61
	.byte	0x1
	.byte	0x37
	.byte	0x6
	.quad	.LFB4
	.quad	.LFE4-.LFB4
	.uleb128 0x1
	.byte	0x9c
	.long	0x427
	.uleb128 0x6
	.string	"fp"
	.byte	0x38
	.byte	0xb
	.long	0x283
	.uleb128 0x3
	.byte	0x91
	.sleb128 -296
	.uleb128 0x4
	.long	.LASF62
	.byte	0x39
	.byte	0xa
	.long	0x427
	.uleb128 0x3
	.byte	0x91
	.sleb128 -288
	.byte	0
	.uleb128 0x8
	.long	0xa7
	.long	0x437
	.uleb128 0x9
	.long	0x3a
	.byte	0xff
	.byte	0
	.uleb128 0x1b
	.long	.LASF73
	.byte	0x1
	.byte	0x2e
	.byte	0x5
	.long	0x66
	.quad	.LFB3
	.quad	.LFE3-.LFB3
	.uleb128 0x1
	.byte	0x9c
	.uleb128 0xe
	.long	.LASF64
	.byte	0x18
	.byte	0x8
	.long	0x3e4
	.quad	.LFB2
	.quad	.LFE2-.LFB2
	.uleb128 0x1
	.byte	0x9c
	.long	0x4a3
	.uleb128 0x6
	.string	"fp"
	.byte	0x19
	.byte	0xb
	.long	0x283
	.uleb128 0x3
	.byte	0x91
	.sleb128 -168
	.uleb128 0x4
	.long	.LASF62
	.byte	0x1a
	.byte	0xa
	.long	0x4a3
	.uleb128 0x3
	.byte	0x91
	.sleb128 -160
	.uleb128 0x4
	.long	.LASF65
	.byte	0x1b
	.byte	0xc
	.long	0x3e4
	.uleb128 0x3
	.byte	0x91
	.sleb128 -176
	.byte	0
	.uleb128 0x8
	.long	0xa7
	.long	0x4b3
	.uleb128 0x9
	.long	0x3a
	.byte	0x7f
	.byte	0
	.uleb128 0x1c
	.long	.LASF66
	.byte	0x1
	.byte	0x10
	.byte	0x6
	.quad	.LFB1
	.quad	.LFE1-.LFB1
	.uleb128 0x1
	.byte	0x9c
	.long	0x50d
	.uleb128 0x1d
	.long	.LASF56
	.byte	0x1
	.byte	0x10
	.byte	0x1a
	.long	0x66
	.uleb128 0x2
	.byte	0x91
	.sleb128 -36
	.uleb128 0x6
	.string	"sum"
	.byte	0x11
	.byte	0x12
	.long	0x6d
	.uleb128 0x2
	.byte	0x91
	.sleb128 -24
	.uleb128 0x1e
	.quad	.LBB2
	.quad	.LBE2-.LBB2
	.uleb128 0x6
	.string	"i"
	.byte	0x12
	.byte	0xe
	.long	0x66
	.uleb128 0x2
	.byte	0x91
	.sleb128 -20
	.byte	0
	.byte	0
	.uleb128 0x1f
	.long	.LASF74
	.byte	0x1
	.byte	0x9
	.byte	0x18
	.long	0x299
	.quad	.LFB0
	.quad	.LFE0-.LFB0
	.uleb128 0x1
	.byte	0x9c
	.uleb128 0x6
	.string	"lo"
	.byte	0xa
	.byte	0x12
	.long	0x41
	.uleb128 0x2
	.byte	0x91
	.sleb128 -24
	.uleb128 0x6
	.string	"hi"
	.byte	0xa
	.byte	0x16
	.long	0x41
	.uleb128 0x2
	.byte	0x91
	.sleb128 -20
	.byte	0
	.byte	0
	.section	.debug_abbrev,"",@progbits
.Ldebug_abbrev0:
	.uleb128 0x1
	.uleb128 0xd
	.byte	0
	.uleb128 0x3
	.uleb128 0xe
	.uleb128 0x3a
	.uleb128 0x21
	.sleb128 4
	.uleb128 0x3b
	.uleb128 0xb
	.uleb128 0x39
	.uleb128 0xb
	.uleb128 0x49
	.uleb128 0x13
	.uleb128 0x38
	.uleb128 0xb
	.byte	0
	.byte	0
	.uleb128 0x2
	.uleb128 0x5
	.byte	0
	.uleb128 0x49
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x3
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
	.uleb128 0x4
	.uleb128 0x34
	.byte	0
	.uleb128 0x3
	.uleb128 0xe
	.uleb128 0x3a
	.uleb128 0x21
	.sleb128 1
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
	.uleb128 0x5
	.uleb128 0xf
	.byte	0
	.uleb128 0xb
	.uleb128 0x21
	.sleb128 8
	.uleb128 0x49
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x6
	.uleb128 0x34
	.byte	0
	.uleb128 0x3
	.uleb128 0x8
	.uleb128 0x3a
	.uleb128 0x21
	.sleb128 1
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
	.uleb128 0x7
	.uleb128 0x16
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
	.byte	0
	.byte	0
	.uleb128 0x8
	.uleb128 0x1
	.byte	0x1
	.uleb128 0x49
	.uleb128 0x13
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x9
	.uleb128 0x21
	.byte	0
	.uleb128 0x49
	.uleb128 0x13
	.uleb128 0x2f
	.uleb128 0xb
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
	.uleb128 0x37
	.byte	0
	.uleb128 0x49
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0xc
	.uleb128 0x13
	.byte	0
	.uleb128 0x3
	.uleb128 0xe
	.uleb128 0x3c
	.uleb128 0x19
	.byte	0
	.byte	0
	.uleb128 0xd
	.uleb128 0x18
	.byte	0
	.byte	0
	.byte	0
	.uleb128 0xe
	.uleb128 0x2e
	.byte	0x1
	.uleb128 0x3f
	.uleb128 0x19
	.uleb128 0x3
	.uleb128 0xe
	.uleb128 0x3a
	.uleb128 0x21
	.sleb128 1
	.uleb128 0x3b
	.uleb128 0xb
	.uleb128 0x39
	.uleb128 0xb
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
	.uleb128 0xf
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
	.uleb128 0x10
	.uleb128 0xf
	.byte	0
	.uleb128 0xb
	.uleb128 0xb
	.byte	0
	.byte	0
	.uleb128 0x11
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
	.uleb128 0x12
	.uleb128 0x35
	.byte	0
	.uleb128 0x49
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x13
	.uleb128 0x26
	.byte	0
	.uleb128 0x49
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x14
	.uleb128 0x13
	.byte	0x1
	.uleb128 0x3
	.uleb128 0xe
	.uleb128 0xb
	.uleb128 0xb
	.uleb128 0x3a
	.uleb128 0xb
	.uleb128 0x3b
	.uleb128 0xb
	.uleb128 0x39
	.uleb128 0xb
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x15
	.uleb128 0x16
	.byte	0
	.uleb128 0x3
	.uleb128 0xe
	.uleb128 0x3a
	.uleb128 0xb
	.uleb128 0x3b
	.uleb128 0xb
	.uleb128 0x39
	.uleb128 0xb
	.byte	0
	.byte	0
	.uleb128 0x16
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
	.uleb128 0x3f
	.uleb128 0x19
	.uleb128 0x3c
	.uleb128 0x19
	.byte	0
	.byte	0
	.uleb128 0x17
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
	.uleb128 0x18
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
	.uleb128 0x6e
	.uleb128 0xe
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
	.uleb128 0x19
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
	.uleb128 0x3c
	.uleb128 0x19
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x1a
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
	.uleb128 0x1b
	.uleb128 0x2e
	.byte	0
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
	.uleb128 0x49
	.uleb128 0x13
	.uleb128 0x11
	.uleb128 0x1
	.uleb128 0x12
	.uleb128 0x7
	.uleb128 0x40
	.uleb128 0x18
	.uleb128 0x7a
	.uleb128 0x19
	.byte	0
	.byte	0
	.uleb128 0x1c
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
	.uleb128 0x11
	.uleb128 0x1
	.uleb128 0x12
	.uleb128 0x7
	.uleb128 0x40
	.uleb128 0x18
	.uleb128 0x7a
	.uleb128 0x19
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x1d
	.uleb128 0x5
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
	.uleb128 0x1e
	.uleb128 0xb
	.byte	0x1
	.uleb128 0x11
	.uleb128 0x1
	.uleb128 0x12
	.uleb128 0x7
	.byte	0
	.byte	0
	.uleb128 0x1f
	.uleb128 0x2e
	.byte	0x1
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
	.uleb128 0x11
	.uleb128 0x1
	.uleb128 0x12
	.uleb128 0x7
	.uleb128 0x40
	.uleb128 0x18
	.uleb128 0x7a
	.uleb128 0x19
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
.LASF73:
	.string	"get_cpu_core"
.LASF52:
	.string	"fopen"
.LASF65:
	.string	"freq"
.LASF68:
	.string	"_IO_FILE"
.LASF60:
	.string	"sscanf"
.LASF25:
	.string	"_IO_save_end"
.LASF7:
	.string	"short int"
.LASF9:
	.string	"size_t"
.LASF74:
	.string	"rdtsc"
.LASF35:
	.string	"_offset"
.LASF67:
	.string	"GNU C17 13.3.0 -masm=intel -m64 -mtune=generic -march=x86-64 -g -fasynchronous-unwind-tables -fstack-protector-strong -fstack-clash-protection -fcf-protection"
.LASF19:
	.string	"_IO_write_ptr"
.LASF14:
	.string	"_flags"
.LASF21:
	.string	"_IO_buf_base"
.LASF59:
	.string	"double"
.LASF26:
	.string	"_markers"
.LASF16:
	.string	"_IO_read_end"
.LASF39:
	.string	"_freeres_buf"
.LASF51:
	.string	"fgets"
.LASF55:
	.string	"core"
.LASF70:
	.string	"stderr"
.LASF34:
	.string	"_lock"
.LASF8:
	.string	"long int"
.LASF48:
	.string	"printf"
.LASF31:
	.string	"_cur_column"
.LASF72:
	.string	"perror"
.LASF30:
	.string	"_old_offset"
.LASF4:
	.string	"unsigned char"
.LASF54:
	.string	"cpu_frequency"
.LASF6:
	.string	"signed char"
.LASF47:
	.string	"uint64_t"
.LASF3:
	.string	"unsigned int"
.LASF44:
	.string	"_IO_marker"
.LASF33:
	.string	"_shortbuf"
.LASF71:
	.string	"__isoc99_sscanf"
.LASF18:
	.string	"_IO_write_base"
.LASF42:
	.string	"_unused2"
.LASF15:
	.string	"_IO_read_ptr"
.LASF53:
	.string	"start"
.LASF22:
	.string	"_IO_buf_end"
.LASF61:
	.string	"print_cpu_info"
.LASF13:
	.string	"char"
.LASF57:
	.string	"elapsed_seconds"
.LASF63:
	.string	"main"
.LASF37:
	.string	"_wide_data"
.LASF38:
	.string	"_freeres_list"
.LASF50:
	.string	"fclose"
.LASF40:
	.string	"__pad5"
.LASF10:
	.string	"__uint64_t"
.LASF62:
	.string	"buffer"
.LASF5:
	.string	"short unsigned int"
.LASF2:
	.string	"long unsigned int"
.LASF20:
	.string	"_IO_write_end"
.LASF12:
	.string	"__off64_t"
.LASF28:
	.string	"_fileno"
.LASF27:
	.string	"_chain"
.LASF46:
	.string	"_IO_wide_data"
.LASF41:
	.string	"_mode"
.LASF11:
	.string	"__off_t"
.LASF24:
	.string	"_IO_backup_base"
.LASF66:
	.string	"exampleFunction"
.LASF56:
	.string	"iterations"
.LASF29:
	.string	"_flags2"
.LASF64:
	.string	"get_cpu_frequency"
.LASF45:
	.string	"_IO_codecvt"
.LASF17:
	.string	"_IO_read_base"
.LASF49:
	.string	"strstr"
.LASF32:
	.string	"_vtable_offset"
.LASF36:
	.string	"_codecvt"
.LASF23:
	.string	"_IO_save_base"
.LASF43:
	.string	"FILE"
.LASF58:
	.string	"iterations_for_1s"
.LASF69:
	.string	"_IO_lock_t"
	.section	.debug_line_str,"MS",@progbits,1
.LASF1:
	.string	"/home/fekerr/src/compfast/rdtsc"
.LASF0:
	.string	"sum_rdtsc.c"
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
