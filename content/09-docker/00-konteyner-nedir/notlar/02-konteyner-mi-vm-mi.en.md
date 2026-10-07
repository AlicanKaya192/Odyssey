A container and a virtual machine are two different answers to the same
question: "how do I separate a program from the rest of the computer?" Let
us put them side by side.

## Comparison

| | Virtual machine | Container |
|---|---|---|
| What is imitated? | A whole computer | Only the program's surroundings |
| Operating system inside | A full operating system with its own kernel | None; the host's kernel is shared |
| Size | Usually a few GB | Often tens to hundreds of MB |
| Start-up time | Minutes | Less than a second |
| How many fit on a server | A few to ten | Hundreds |
| Isolation | Very strong | Strong, but the kernel is shared |

## Why is it so small?

When a virtual machine starts, the operating system inside it boots from
scratch too: drivers, services, memory management. When a container starts,
only **one program** starts; the rest of the operating system is already
running on the host.

The "Linux files" inside a container (e.g. inside `python:3.13-slim`) are not
an operating system but the **commands and libraries** the program needs:
`ls`, `sh`, a few C libraries. The kernel is not among them.

## Why is there still a virtual machine on Windows?

A container uses the host's kernel. Linux containers need a **Linux kernel**,
and the Windows kernel is not Linux. So Docker Desktop runs a small Linux
virtual machine in the background (with WSL 2), and all containers run
inside it, sharing its kernel.

So on Windows there is one small virtual machine with the containers inside
it. Not a hundred virtual machines for a hundred containers.

## Which one when?

Choose a **container**:

- if you want a program to run the same on other computers,
- if you will run several small services side by side,
- if fast starting and stopping matter.

Choose a **virtual machine**:

- if you want to try a whole other operating system (running Windows on
  Linux, for example),
- if you need very strict isolation (code you do not trust),
- if you need a system with a desktop.

In practice the two are often used together: a server rented in the cloud is
a virtual machine, and containers run on top of it.
