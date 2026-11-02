If you suspect malware on a computer, the order matters. Things done in a
panic that look right (switching the machine off at once, deleting files)
sometimes destroy the traces. An organisation has a written **incident
response plan** for this; the details are in the System Security module. A
short order for an individual user:

## 1. Isolate

Disconnect the computer from the network (cable, wireless). Then the
malware cannot spread to other machines or send data out. Switching the
computer off at once is not necessary: traces in memory can be useful in
the investigation.

## 2. Report

If you are in an organisation, tell the security team at once. Waiting
because "it might be nothing" gives the incident time to grow. Write down
what you saw, when you saw it and what you did before (which attachment you
opened, which site you visited).

## 3. Change passwords from another device

If there may be a keylogger or spyware, change the passwords **not from
that computer** but from a clean device. E-mail and the password manager
first, then the other accounts.

## 4. Clean or reinstall

Simple adware can be removed with a security tool. But if a rootkit or a
backdoor is possible, the safest way is to wipe the disk and **install the
system from scratch**; a hidden piece can remain in a system said to be
"cleaned".

## 5. Restore from a clean backup

Make sure the backup being restored was taken **before** the infection.
Otherwise the malware comes back with the backup.

## 6. Find the door and close it

How did it get in? An unpatched program, an opened attachment, a weak
password? If the door is not closed, the incident repeats. The lesson
learned is recorded.

## Do not

- Do not write to the addresses in a ransom note, do not make a "test"
  payment.
- Do not open the suspicious file "to see what it is", or send it to
  others.
- Do not try to clean it quietly without telling anyone.
