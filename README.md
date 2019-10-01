# Zemu Client - Binary Tracing in the Cloud

This is the *preview* version of the Zemu cloud client for generating dynamic binary traces. It provides `strace`-like functionality for Linux/IoT binaries (x86, ARM and preliminary MIPS support), as well as an instruction-level `overlay` for execution visualization in IDA Pro.

## Setup

Paste your API key into `zemu.py`. For example, replace:

```
API_KEY = os.environ.get(
    'ZEMU_API_KEY', 'PASTE_YOUR_API_KEY_HERE')
```

with your API key:

```
API_KEY = os.environ.get(
    'ZEMU_API_KEY', 'c929270f53a0c27162659c932746fbe3')
```

## Usage

Python is required. Example usage and output:

```
python zemu.py strace static_elf_arm_helloworld

Zemu Copyright (c) 2019 Zeropoint Dynamics, LLC

Submitting.................done.
Queued. Awaiting results...done.

[main] [0x4b7ec] brk ( addr=0x0 ) -> 90000048
[main] [0x4b7ec] brk ( addr=0x90000d50 ) -> 90000d50
[main] [0x108d8] set_tls ( env=0x90000510 ) -> void
[main] [0x4b0ec] uname ( buf=0xff08fbe0 ) -> 0
[main] [0x55214] readlink ( pathname=0x719f8 ("/proc/self/exe"), buf=0xff08ed20, bufsiz=0x1000 ) -> 18
[main] [0x4b7ec] brk ( addr=0x90021d50 ) -> 90021d50
[main] [0x4b7ec] brk ( addr=0x90022000 ) -> 90022000
[main] [0x531fc] access ( pathname=0x71620 ("/etc/ld.so.nohwcap"), mode=0x0 ) -> -1
[main] [0x284ec] fstat64 ( fd=0x1, statbuf=0xff08fc80 ) -> 0
[main] [0x28820] write ( fd=0x1, buf=0x60b60 ("hello world!"), count=0xc ) -> c
[main] [0x28820] write ( fd=0x1, buf=0x90000fa8 ("
"), count=0x1 ) -> 1
[main] [0x27cd4] exit_group ( status=0x0 ) -> void
```
