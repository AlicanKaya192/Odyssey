`publish`: write the data with `Relaxed`, then the flag with `Release`. `wait_for`: wait for the flag with `Acquire`, call `spin_loop`, then read the data. The order matters.
