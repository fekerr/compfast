use std::fs::File;
use std::io::{BufRead, BufReader};
use libc::{sched_getcpu, c_uint};
use std::arch::asm;
use std::convert::TryInto;

fn rdtsc() -> u64 {
    let lo: u32;
    let hi: u32;
    unsafe {
        asm!("rdtsc", out("eax") lo, out("edx") hi);
    }
    ((hi as u64) << 32) | (lo as u64)
}

fn example_function(iterations: u64) {
    let mut _sum: u64 = 0; // Mark as unused with `_`
    for i in 0..iterations {
        _sum += i;
    }
}

fn get_cpu_frequency() -> Result<f64, &'static str> {
    let file = File::open("/proc/cpuinfo").map_err(|_| "Failed to open /proc/cpuinfo")?;
    let reader = BufReader::new(file);

    for line in reader.lines() {
        let line = line.map_err(|_| "Failed to read line")?;
        if line.starts_with("cpu MHz") {
            let parts: Vec<&str> = line.split(':').collect();
            if let Some(freq_str) = parts.get(1) {
                let freq = freq_str.trim().parse::<f64>().map_err(|_| "Failed to parse frequency")?;
                return Ok(freq * 1e6); // Convert MHz to Hz
            }
        }
    }
    Err("Failed to find CPU frequency")
}

fn get_cpu_core() -> Result<u32, &'static str> {
    unsafe {
        let core_id: c_uint = sched_getcpu().try_into().unwrap();
        if core_id == !0 {
            Err("Failed to get CPU core")
        } else {
            Ok(core_id)
        }
    }
}

fn print_cpu_info() -> Result<(), &'static str> {
    let file = File::open("/proc/cpuinfo").map_err(|_| "Failed to open /proc/cpuinfo")?;
    let reader = BufReader::new(file);

    println!("CPU Information:");
    for line in reader.lines() {
        let line = line.map_err(|_| "Failed to read line")?;
        if line.contains("processor") || line.contains("model name") ||
            line.contains("cpu cores") || line.contains("core id") {
            println!("{}", line);
        }
    }
    Ok(())
}

fn main() {
    match get_cpu_frequency() {
        Ok(cpu_frequency) => {
            println!("CPU Frequency: {:.2} GHz", cpu_frequency / 1e9);

            match get_cpu_core() {
                Ok(core) => println!("Running on CPU core: {}", core),
                Err(e) => println!("{}", e),
            }

            if let Err(e) = print_cpu_info() {
                println!("{}", e);
            }

            let iterations: u64 = 1_000_000; // Initial number of iterations
            let start = rdtsc();
            example_function(iterations);
            let end = rdtsc();

            let elapsed_seconds = (end - start) as f64 / cpu_frequency;
            println!("Elapsed cycles: {}", end - start);
            println!("Elapsed time: {:.6} seconds", elapsed_seconds);

            let iterations_for_1s = (iterations as f64 / elapsed_seconds) as u64;
            println!("Estimated iterations for 1 second runtime: {}", iterations_for_1s);
        },
        Err(e) => println!("{}", e),
    }
}

